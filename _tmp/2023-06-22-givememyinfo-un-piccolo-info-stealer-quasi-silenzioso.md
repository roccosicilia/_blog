---
layout:     post
title:      "GiveMeMyInfo: un piccolo info-stealer (quasi) silenzioso"
date:       2023-06-22 13:00:00 +0200
categories: [cyber-security, hacking, ita]
image:
---
## Contesto

Mi capita di dove lavorare in scenari estremamente maturi dal punto di vista della postura di sicurezza, non e' raro dover quindi creare qualcosa di un po' custom per verificare se i sistemi di sicurezza sono stati opportunamente configurati e se le precedure di detection siano adeguate in relazione alle moderne tecniche di attacco. Questa premessa probabilmente vale per tutti i post in cui parlo di Red Teaming e sicurezza offensiva.

Vi lascio il link al video di introduzione al tema:

https://youtu.be/X2RBf-3SMOo

VLOG: Covert Channel Detection

Nei giorni scorsi ho iniziato ad "industrializzare" alcune mie p-o-c che ho utilizzato anche in contesti operativi per eseguire attivita' di Command and Control (C2) ed esfiltrazione di dati. Il modello di base e' molto semplice e deve rispettare queste semplici regole:

- Assolutamente vietato depositare file a bordo della macchina compromessa
- Utilizzo di canali di comunicazione simili a quelli del target
- Restare in un contesto utente (senza privilegi di amministratore della macchina)

I vincoli sono auto-imposti a seguito di diversi assessment a livello di presidi di sicurezza: i target con cui opero ha attivato un servizio MDR che controlla eventi provenienti dai sistemi client e server grazie a soluzioni EDR (tra le piu' note) e a livello rete grazie a piattaforme Firewall UTM che gestiscono in traffico sia verso internet che tra le reti interne. L'azione mira quindi a stabilire se un device della rete e' potenzialmente compromissibile e a che livello si potrebbe spingere il threat actor; tra le varie flag vi e' quella di portare all'esterno informazioni inerenti la configurazione della rete e dei sistemi.

## Struttura dell'attacco

Tralascio in questo post le fasi iniziali visto che il focus e' il tool, o meglio i comandi, di info-stealing. Come detto vorrei evitare di depositare file sulla macchina target, ho quindi ipotizzato di utilizzare una tecnica ben collautata, un classico:

- sulla macchina targer viene configurato un Task schedulato che ogni *N* secondi esegue un comando di comunicazione con un C2
- il C2 e' rappresentato da una istanza di un servizio cloud (es: PasteBin) in cui il client target trovera' i comandi da eseguire localmente
- tutti gli output dei comandi verranno inviati al C2 sotto forma di NewPaste di PasteBin o verso altre piattaforme

Flusso abbastanza semplice, i comandi al target vengono impartiti modificando in contrenuto del *Paste di input* ed il risultato viene posizionato in dei *Paste di output*.

In questa prima versione ho creato un piccolo script, destinato a crescere a livello di opzioni, per generare il comando powershell necessario a compromettere la macchina target. Il funzionamento e' molto semplice ed al momento prevedo due output base: il comando da passare il CLI e la versione per Rubber Ducky.

<img src="{{ '/assets/images-posts/task-demo.png' | relative_url }}" alt="task demo" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Comando per conf. task

Una volta "installato" il task il Red Team deve solo preoccuparsi di impartire i comandi corretti tramite un contenuto disponibile a livello cloud, come il *paste* su PasteBin o simili, e farsi recapitare l'output in una destinazione comoda. Anche per questa operazione ho creato uno script che, partendo dal comando da impartire localmente al sistema, completa la stringa con i comandi necessari ad esfiltrare l'output. Tutto rigorosamente in powershell e senza l'ausiolio di file sul sistema o apertura di socket specifiche.

<img src="{{ '/assets/images-posts/c2-exfil.png' | relative_url }}" alt="c2 exfil" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Comando per raccolta info

In questo esempio il canale per i dati in uscita e' differenti (GitHub Gists) rispetto al canale utilizzato per leggere il comando: separare il canale di controllo dal canale di esfiltrazione e' una pratica abbastanza frequente e puo' complicare la detection. In questo caso, se i sistemi di controllo non intervengono in nessun passaggio, avremo ottenuto un metodo per impartire comandi complessi ogni 60 secondi alla macchina compromessa.

## ToDo

Ci sono due principali aspetti che vorrei migliorare.

Il primo e' funzionale: vorrei definire un set di canali da utilizzare abbastanza variegato. Durante una recente discussione sul canale Telegram BitHorn si citavano giustamente le piattaforme cloud come GDrive, OneDrive e simili come elementi comodi e particolarmente utilizzati e quindi facili da "nascondere", probabilmente non altrettanto facili da utilizzare un in contesto fileless.

Il secondo e' operativo: per migliorare l'interazione vorrei implementare un piccolo client che si occipi, definiti i canali, di leggere e scrivere sulla piattaforme cloud selezionate per l'azione cosi' di semplificare l'utilizzo dello strumento. Il comportamento resterebbe invariato. E' da considerare che il cliente non sarebbe utilizzabile per tutti i canaliti potenzialmente sfruttabili.

## Punti di attenzione

Sul canale Telegram abbiamo recentemente discusso molto sulle possibilita' di detection di queste tecniche che per quanto silenti generano eventi cressificabili come anomali. Molto dipendere dalla configurazione dei sistemi e dalle capacita' di analisi di chi osserva l'evento: una ssione HTTPS verso PasteBin generata da un comando PowerShell potrebbe essere classificata come malevola in molti contesti e la stessa identica azione vero GitHub potrebbe passare inosservata. Ci sono molte variabili da considerare cosa che rende queste tecniche abastanza insidiose ma non impossibili da intercettare. [Vi rimando comunque al gruppo](https://t.me/+a7sF3JQV4bMzY2Nk) dove sono stati discussi spunti molto interessanti.

In relazione alla divulgazione del codice ho recentemente deciso di essere un po' piu' cauto con alcuni strumenti. La repository resta quindi privata ma chiunque voglia collaborare eseguire dei test puo' segnalarmelo direttamente o tramite il [canale dedicato ai miei progetti](https://discord.com/channels/980421363078664222/1025153592266592396).
