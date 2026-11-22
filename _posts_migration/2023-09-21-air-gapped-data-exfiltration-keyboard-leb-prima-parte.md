---
layout:     post
title:      "Air-gapped Data Exfiltration: keyboard leb (prima parte)"
date:       2023-09-21 17:30:00 +0200
categories: [hacking, ita]
image:
---
Tutto parte da [questa fantastica lettura](https://arxiv.org/pdf/1907.05851.pdf). L'ipotesi di laboratorio è che sia possibile utilizzare i led di una tastiera USB per trasmettere dati ad un sistema ricevente operando così da canale per un'azione di data exfiltration. E' uno di quei temi che ti capita di leggere ma che raramente si ha occasione di mettere in pratica, da qui la volontà di studiare e provare la tecnica in laboratorio.

https://youtu.be/NI5WjDpKkbg

Video DEMO

## Contesto

Ho in mente alcune situazioni in cui la tecnica potrebbe essere effettivamente applicabile con successo dal punto di vista della resa e dell'efficienza. Esistono diversi contesti in cui pensare di eseguire un attacco *classico* per ottenere l'exfiltration di dati risulta molto oneroso: la presenza di sistemi di detection limita le azioni del Threat Actor (e del Red Team) e trovare un punto di accesso digitale sfruttabile potrebbe richiedere molto tempo, al contrario potrebbe essere relativamente semplice accedere fisicamente al sito del target. Esistono inoltre contesti in cui il sistema target è effettivamente isolato dalla rete e quindi c'è poco da fare. In questi casi potrebbe essere più efficace valutare tecniche di esfiltrazione che siano poco visibili dai classici strumenti di detection e che possano sfruttare la presenza fisica all'interno della struttura target.

Per comprendere meglio lo scenario è bene tenere a mente come mai esistono sistemi separati dalla rete internet. Si tratta di una misura di sicurezza, relativamente estrema, per assicurarsi che nessuno possa sfruttare la rele locale o la rete internet per compromettere una macchina o un sistema posto di fatto in isolamento. [Qui una spiegazione](https://en.wikipedia.org/wiki/Air_gap_(networking)) abbastanza esaustiva.

Supponiamo che il target sia una workstation all'interno di un edificio che, per ragioni operative è accessibile da personale esterno: è teoricamente possibile sfruttare una delle procedure che consentano ad una figura terza di avvicinarsi al sistema. Qualche esempio: una workstation operativa posta in un complesso industriale, un terminale di servizio appartenente ad una rete isolata. Spesso i locali aziendali vengono resi accessibili a visatatori in occasione di colloqui di lavori, dialoghi con fornitori e clienti, attività di manutenzione che coinvolgano terze parti; la possibilità che un Threat Actor sfrutti queste occasioni per compromettere un sitema isolato è reale anche se meno frequente rispetto agli scenari più classisi.

## Modello di attacco

Nello scenario che discuteremo l'accesso alla macchina target è limitato a pochi secondi in cui saremo liberi di eseguire un'azione a livello fisico, abbiamo invece a disposizione più tempo - diciamo 60 secondi - per registrare il segnale utilizzando uno smartphone a circa 1 mt di distanza. La macchina è una normale workstation con sistema operativo Microsoft Windows 10 a cui sono collegati un mouse ed una tastiera USB.

L'obiettivo dell'azione fisica è inserire nella macchina target una USB Rubber Ducky configurata con una sequenza di comandi in Powershell che chiederà una informazione al sistema operativo e la trasmetterà, opportunamente elaborata, utilizzando i led della tastiera USB. Il malware deve quindi convertire l'informazione in una sequenza binaria che verrà trasmessa tramite segnali luminosi. L'attacker deve riuscire a registrare la sequenza luminoda con in proprio smartphone ed allontanarsi dal sistema vittima, se possibile recuperando la USB Rubber Ducky.

Il segnale, una volta registrato in una sequenza video, vede essere rielaborato per ricostruire l'informazione originale. Ovviamente questa ultima fase è da eseguirsi una volta lasciato l'edificio target.

## Lettura e trasmissione dei dati

In questo primo post prendiamo in considerazone la fase di lettura del dato e trasmissione. Ipotizzando un sistema isolato a livello di rete o appartenente ad una rete di per se isolata dall'esterno, dobbiamo necessariamente agire direttamente sulla macchina target. In realtà lo stesso concetto è estendibile a reti particolarmente presidiate: non è raro osservare sbilanciamenti tra quanto viene fatto per controllare l'accesso digitale al dato e quanto **non** viene fatto per controllare l'accesso fisico al dato. Sul tema dell'accesso fisico alle strutture ed alle risorse è necessario aprire un capitolo a parte, i questa occasione è sufficiente considerare che in molti contesti è relativamente semplice introdurre device da collegare ad una postazione PC (come una Rubber Ducky) o da collegare alla rete (come una Raspberry) nonostante l'elevato livello di detection.

Come detto la mia scelta ricade sulla Rubber Ducky con i relativi limiti:

- per quanto veloce è di fatto da considerare il tempo di "digitazione" da parte dello script
- tutto il payload/script deve far uso di chiamate *semplici* per non "svegliare" l'eventuale EDR
- la sessione della workstation deve essere unlocked
- il gioco funziona con le tastiere USB, eventuali tastiere integrate potrebbero non funzionare con lo stesso payload

Per generare un evento di "pressione" di un tasto esiste una funzione molto comoda:

```
(New-Object -ComObject WScript.Shell).SendKeys('{NUMLOCK}')
```

Questo blocco di codice (PowerShell) genera la pressione software del tasto Num Lock della tastiera, uno dei tasti che solitamente ha un LED dedicato per segnalarne il "lock" come anche CapsLock e ScrollLock.

Ipoteticamente abbiamo quindi tre LED pilotabili, possiamo quindi trasmettere, ad esempio, tutti le cifre da 0 a 7 (000, 001, 010, 011, 100, 101, 110, 111) dove 000 è rappresentato da tutti i LED spenti e 111 è rappresentato da tutti i LED accesi. Per risolvere un problema tecnico dobbiamo però accontentarci di usare 2 bit per la trasmissione ed 1 bit (il terzo LED) ci farà da clock. Tutto quello che trasmetteremo dovrà essere registrato in un video per poi essere *campionato*, ma va considerato che sarebbe poco usabile, da un punto di vista funzionale, campionare il video in base al tempo in quanto la sequenza di accensioni e spegnimenti dei LED potrebbe presentare delle imperfezioni: in pratica è da escludere che la durata delle trasmissioni sia precisa ed uguale per tutte le trasmissioni. Utilizzando il terzo LED come clock abbiamo un riferimento chiaro dello scorrere del tempo.

Faccio un esempio: se devo trasmettere la sequenza 11 - 10 - 01 le "fasi" saranno qualcosa di simile:

<img src="{{ '/assets/images-posts/image-1.png' | relative_url }}" alt="image 1" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

sequenza luminosa

- In t1 i LED partono da una situazione di "riposo" anche se a livello di script lo status dei LED prima della trasmissione non deve essere necessariamente questo
- In t2 i LED L1 e L2 vengono accesi in corrispondenza del valore "11", viene acceso anche L3 per segnalare che il dato visualizzato è quello da campionare
- In t3 il LED L3 si spegne per segnalare la fine della trasmissione precedente
- In t4 il LED L1 viene acceso ed il LED L2 viene spento in corrispondenza del valore "10", viene acceso anche il LED L3 per segnalare che il dato visualizzato e quello da campionare
- In t5 il LED L3 si spegne per segnalare la fine della trasmissione precedente
- In t6 il LED L1 viene spento ed il LED L2 viene acceso in corrispondenza del valore "01", viene acceso anche il LED L3 per segnalare che il dato visualizzato e quello da campionare

La trasmissione procede quindi 2 bit alla volta fino al termine della sequenza binaria che abbiamo passato al "trasmettitore".

Ora che abbiamo un metodo di trasmissione capace di spedire dati in binario possiamo valutare che tipo di informazioni mandare. Come vedremo meglio nel secondo articolo di questa serie, la precisione della lettura dei dati campionati dipende dalla velocità con cui i LED cambiano di stato: eseguire cambiamenti troppo rapidi potrebbe rendere difficile la lettura del video. Quindi abbiamo un trasmissione che andrà rallentata rispetto al potenziale tecnico e un canale a 2 bit, di conseguenza dobbiamo valutare una trasmissione nell'ordine delle centinaia di bit per restare nei 60 secondi.

<img src="{{ '/assets/images-posts/image-2.png' | relative_url }}" alt="image 2" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Anteprima del codice per la trasmissione

Lo script, che a livello di lavoratorio vediamo nel formato .ps1 ma che può facilmente essere confertito in una sequenza di comandi per una Rubber Ducky, deve quindi compiere tre azioni:

- eseguire un comando che generi un output (es: leggere un file o eseguire un comando in CLI)
- portare l'output in formato binario in una byte array così da ottenere una lista di 0 e 1
- trasmettere la sequenza modificando lo stato dei LED 2 bit alla volta

Praticamente abbiamo una lettura, una conversione e due cicli. Qui una versione funzionante dello script: <https://github.com/roccosicilia/my-papers/blob/main/paper-AirGapped/rubber.ps1>

Nota tecnica: lo script introduce un ritardo nelle azioni di gestione del clock utilizzando il cambio di stato del LED relativo allo ScrollLock, questo ritardo dovrà essere gestiti in funzione della qualità della camera che registrerà la seguenza (argomento della seconda parte).

Per la trasmissione dei dati è tutto. Sulla mia pagina Patreon sono archiviate le live durante le qualinabbiamo discusso ed implementato quento raccontato: [https://www.patreon.com/roccosicilia](https://www.patreon.com/roccosicilia/posts?filters%5Btag%5D=air+gapped). Tra qualche giorno pubblicherò l'articolo in merito all'azione di ricezione e decodifica delle informazioni.
