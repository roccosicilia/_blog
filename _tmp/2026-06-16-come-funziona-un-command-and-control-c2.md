---
layout:     post
title:      "Come funziona un Command and Control (C2)"
date:       2026-06-16 12:00:00 +0200
categories: [cyber-security, hacking, ita]
image:      /assets/images-posts/in-questo-post-parlo-di-threat-intelligence-e-threat-hunting.png
---
1. [Introduzione](https://roccosicilia.com/2026/06/16/come-funziona-un-command-and-control-c2/#introduzione)
2. [Funzionamento di base](https://roccosicilia.com/2026/06/16/come-funziona-un-command-and-control-c2/#funzionamento-di-base)
3. [Stageless vs. Staged](https://roccosicilia.com/2026/06/16/come-funziona-un-command-and-control-c2/#stageless-vs-staged)
4. [Canale di comunicazione](https://roccosicilia.com/2026/06/16/come-funziona-un-command-and-control-c2/#canale-di-comunicazione)
5. [Lab si esempio](https://roccosicilia.com/2026/06/16/come-funziona-un-command-and-control-c2/#lab-si-esempio)
6. [Detection](https://roccosicilia.com/2026/06/16/come-funziona-un-command-and-control-c2/#detection)
7. [Conclusione](https://roccosicilia.com/2026/06/16/come-funziona-un-command-and-control-c2/#conclusione)

---

Chi segue il blog o il canale YouTube da un po' è a conoscenza dei miei obiettivi divulgativi: storicamente ho sempre scritto e parlato dei temi che riguardavano il mio quotidiano ma da qualche mese sto cercando di proporre temi che siano utili a chi ha iniziato da poco il proprio percorso nel mondo dell'info. security. Quindi, come su [Substack](https://roccosicilia.substack.com/subscribe) è apparsa una serie dedicata alle basi, qui appariranno post dedicati a temi un po' più complessi spiegati al meglio delle mie capacità e senza andare a spaccare il bit. Ovviamente le occasioni di approfondimenti non mancheranno soprattutto se ci sono domande o richieste specifiche.

Sul mio canale YouTube ho pubblicato un video-recap:

https://www.youtube.com/watch?v=ggZ5biRMH8k

## Introduzione

I threat actor hanno sempre avuto bisogno di uno strumento per comunicare con i sistemi compromessi. Anni fa, agli albori dell'internet come oggi la conosciamo, si usavano dei malware che erano in grado di attivare delle backdoor sui sistema delle vittime.

<img src="{{ '/assets/images-posts/image-1.png' | relative_url }}" alt="image 1" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Ci si riferiva a questi software con il termine Trojan Horse, programmi che installavano ed avviavano un servizio in ascolto su una specifica porta della macchina della vittima a cui l'attaccante si poteva poi collegare con un client.

Ovviamente parliamo di un mondo piuttosto diverso da quello attuale: le connessioni domestiche erano prevalentemente di tipo dial-up e il provider assegnava l’indirizzo IP direttamente al modem della workstation. I sistemi erano quindi quasi sempre esposti direttamente alla rete con un IP pubblico raggiungibile, cosa che oggi, nelle connettività domestiche ed aziendali, non faremmo mai a meno che non sia necessario per qualche servizio specifico ma solitamente usiamo design di rete completamente differenti. Ad ogni modo questo consentiva di esporre il servizio della backdoor direttamente in internet e l'attaccante ci si poteva comodamente collegare per prendere possesso del sistema.

Se trovi utili i contenuti che condiviso e vuoi restare aggiornato puoi sostenere il mio progetto di divulgazione [iscrivendoti al mio Substack](https://roccosicilia.substack.com/subscribe). Per gli abbonati metto a disposizione articoli e video di approfondimento.

L'esigenza è rimasta ma le reti sono profondamente cambiate: le workstation non vengono più esposte pubblicamente (più o meno) e anche i più banali router dei provider domestici sono dotati di firewall minimali in grado di operare una qualche gestione/filtro del traffico.

<img src="{{ '/assets/images-posts/image-2.png' | relative_url }}" alt="image 2" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Shodan, filtro *os:"Windows 10"*

Installare un servizio in ascolto sulla workstation vittima non ha più senso e la tecnica di attacco si è dovuta evolvere. Oggi gli attaccanti utilizzano infrastrutture Command and Control per comunicare con le macchine compromesse senza essere intercettati dai sistemi di detection ed il loro funzionamento è abbastanza complesso e merita di essere analizzato.

Questi strumenti sono molto utilizzati per mantenere una persistenza all'interno della rete target, impartire comandi ed estrarre informazioni. Sono un elemento fondamentale per la riuscita di attacchi informatici sofisticati e, nonostante gli strumenti di difesa di cui disponiamo, riescono a rimanere silenziosamente attivi sui sistemi target per settimane o mesi.

[<img src="{{ '/assets/images-posts/image-3.png' | relative_url }}" alt="image 3" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />](https://blog.talosintelligence.com/writing-a-bugsleep-c2-server/)

Uno dei tanti [articoli di approfondimento](https://blog.talosintelligence.com/writing-a-bugsleep-c2-server/) di cui vi consiglio una lettura.

Le infrastruttura C2 sono studiate approfonditamente dai vendor, dai team di ricerca e dai professionisti del settore, qualche contenuto lo trovate anche nel mio blog e sul mio canale YouTube. Comprenderne il funzionamento è fondamentale.

## Funzionamento di base

La meccanica alla base del funzionamento è molto semplice e si basa su un assunto nel design delle reti LAN che ancora regge e che tocchiamo solo in parte in questo post. Una caratteristica di molte reti è la presenza di filtri molto rigidi per il traffico in ingresso e molto meno rigidi per il traffico n uscita. È molto frequente non accettare che sistemi esterni contattino direttamente le workstation o i server della nostra rete (ovviamente), mentre è molto più frequente accettare che i propri sistemi interni contattino servizi esterni con differenti protocolli.

Su base di questa ipotesi il malware che deve "colpire" il sistema target deve fare una cosa semplice: aprire una sessione di comunicazione dalla macchina vittima verso il sistema controllato dall'attaccante e fare in modo che questo canale di comunicazione sia utilizzabile dall'attaccante per impartire comandi locali. Per ottenere questo risultato il malware che si utilizza compie una serie di azioni specifiche: viene attivato un loop in il malware si "sveglia", contatta il servizio in ascolto sul C2, gli chiede se ci sono task da eseguire, esegue il task (comando locale), invia il risultato e torna a "dormire".

<img src="{{ '/assets/images-posts/image-4.png' | relative_url }}" alt="image 4" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Esempio super-semplice e funzionante.

Questo comportamento, che qui ho molto semplificato, è chiamato *beacon* e presenta alcune caratteristiche tecniche molto importanti.

Un elemento su cui ragionare è l'intervallo di *sleep*: ogni quanto deve essere reiterata l'azione? Su questo tema va anche detto che un loop regolare è tecnicamente più facile da intercettare rispetto ad un intervallo irregolare, solitamente si introduce un *jitter* al fine di rendere pseudo-casuale il tempo di sleep. C'è anche da considerare, in caso di traffico http/https, gli elementi caratteristici della richiesta http come lo user-agent ed altri elementi che contribuiscono all'analisi del *fingerprinting* del software che sta eseguendo la richiesta.

Sul *fingerprinting* ho in mente di fare un approfondimento per JA3 e JA4 in relazione alla detection a livello rete/firewall.

Stiamo ovviamente tralasciando la delivery del payload, tema che dal funzionamento del C2 in se ma penso sia utile illustrare lo staging.

## Stageless vs. Staged

Ovviamente non c'è una metodologia in assoluto migliore rispetto all'altra, come sempre dipende dai contesti operativi.

Personalmente preferisci utilizzare payload super-minimal e stageless, quindi un unico file o scrips eseguito direttamente via CLI (fileless) con il minimo indispensabile per aprire la comunicazione. Ovviamente portarsi ulteriori componenti a bordo macchina è comodo e spesso i threat actor utilizzano un primo stage che ha il solo compito di attivare il download delle componenti malevole.

In generale avere sulla macchina target un programma minimale rende più difficile la detection, se poi lo facciamo girare direttamente in memoria i sistemi AV/EDR hanno ancora meno elementi da utilizzare per analizzare staticamente il payload che si sta utilizzando.

## Canale di comunicazione

Ho già fatto cenno ad HTTP come protocollo spesso utilizzato ma non è certo l'unico. Tra i più apprezzati troviamo anche DNS in quanto, come HTTP, è solitamente lasciato aperto e poco controllato.

In ogni caso il trucco è generare richieste che assomiglino a qualcosa di lecito, è quindi indispensabile personalizzare al massimo la struttura della richiesta così da renderla simile ad un'operazione legittima come un Windows Update o un processo di comunicazione verso uno dei tanti sistemi cloud storage se si utilizza HTTP/HTTPS. In caso di altri protocolli sarà comunque necessario "imitare" qualcosa di lecito.

Molti Red Team (ma anche molti threat actor) utilizzano noti framework per le attività di test. Va considerato che da tempi SOC e sistemi di detection hanno iniziato ad introdurre regole specifiche per questi tools cosa che, lato security test, invalida le verifiche eseguite salvo applicare molte personalizzazioni alla configurazione del tool. La buona notizia è che anche i threat actor devo ingegnarsi per usare questi strumenti.

## Lab si esempio

L'esempio pratico è sempre un valido aiuto per comprendere il funzionamento del meccanismo di base e qui provo a mostrarvi qualcosa di molto semplice e replicabile utilizzando un tool molto semplice da utilizzare e configurare: [Sliver](https://github.com/bishopfox/sliver).

In questa occasione vorrei non approfondire i dettagli di questa tipologia di tools, avremo sicuramente occasione di farlo nei post/video di approfondimento. Per avere un'idea di quello che succede possiamo concentrarci sulla creazione di un payload per Windows:

<img src="{{ '/assets/images-posts/image-7.png' | relative_url }}" alt="image 7" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Inoltre prepariamo un Wireshark sulla macchina linux filtrando il traffico per l'IP della macchina target:

<img src="{{ '/assets/images-posts/image-6.png' | relative_url }}" alt="image 6" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Ora possiamo avviare il paylaod di esempio sulla macchina target:

<img src="{{ '/assets/images-posts/image-8.png' | relative_url }}" alt="image 8" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Nota a margine: per eseguire il test è solitamente opportuno disattivare la *real time protection* di Microsoft Windows, in questa occasione non ci soffermiamo sul tema dell'evasion che sto trattando in una [serie di blog post dedicata](https://roccosicilia.com/tag/edr-evasion/).

Quello che dovremmo osservare è la sessione attivarsi sul terminale di Sliver ed il processo partire sulla macchina target, mentre su Wireshark osserveremo il traffico verso il C2 in assenza di comandi, quindi il solo beaconing.

<img src="{{ '/assets/images-posts/image-9.png' | relative_url }}" alt="image 9" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

A questo punto possiamo interagire con la sessione tramite la CLI di Sliver, ma questo è un'altro tema:

<img src="{{ '/assets/images-posts/Screenshot-2026-06-16-at-10.31.53.png' | relative_url }}" alt="Screenshot 2026 06 16 at 10.31.53" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Piccolo focus su quello che si vede attraverso l'analisi del traffico. In questo test si vede abbastanza bene come il traffico relativo ai comandi ed alle risposte venga cifrato e suddiviso in pacchetto più piccoli per poi essere inviato al C2:

<img src="{{ '/assets/images-posts/image-10.png' | relative_url }}" alt="image 10" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Da Wireshark si possono esaminare i singoli pacchetti, ovviamente non è possibile osservarne il contenuto grazie alla cifratura.

## Detection

Intercettare questo tipo di strumenti/minacce è complesso. Lato endpoint gli EDR possono sicuramente fare molto sul piano dell'analisi dei processi. Andare a caccia di elementi statici non aiuta particolarmente: molti strumenti consentono un altro gradi di personalizzazione del payload ed esiste la possibilità, estremamente concreta oggi anche grazie all'utilizzo degli LLM, di costruire payload custom che non hanno nulla da invidiare agli strumenti "di mercato".

Un approccio interessante, anche se limitato, è l'analisi della periodicità dei beacon: un processo che in modo regolare esegue una richiesta HTTPS (o DNS) potrebbe rappresentare un comportamento anomalo in molte reti. Va comunque considerato che anche su questo il threat actor può intervenire con il citato *jitter*.

Per alcuni protocolli utilizzati in contesti di tunneling (DNS e ICMP) l'analisi stessa delle richieste potrebbe dare informazioni utili ad una detection, vanno ovviamente implementare regole dedicate a livello IDP/IPS o avere a disposizione tecnologie di detection mature che implementino nativamente questi controlli.

Il tema TLS fingerprinting è forse quello che potrebbe dare maggiore soddisfazione. È un argomento che merita uno spazio a se ed in questa occasione è giusto citarlo almeno per consentire a chi ha firewall di buona qualità di verificare la disponibilità della funzione.

## Conclusione

Come ho detto ad inizio post l'obiettivo di questi articoli è introdurre temi complessi restando "leggeri" e dando comunque la mia disponibilità ad approfondire. Alcuni dettagli saranno oggetto di articoli/video in futuro ma se avete una specifica esigenza o curiosità potete sempre [mettervi in contatto con me](https://roccosicilia.com/about/).
