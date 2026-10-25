---
layout:     post
title:      "C2 custom (parte 1)"
date:       2025-01-03 09:00:00 +0100
categories: [cyber-security, hacking, ita]
image:      /assets/images-posts/coding.png
---
È un'esigenza di servizio che soddisfa una mia personale curiosità. Ho dei requisiti specifici da soddisfare:

- Traffico solo in HTTP/HTTPS e solo sulle relative porte standard 80/443
- Payload lato client in Powershell e Python
- Dimensioni payload estremamente ridotte

In questo post ragiono "ad alta voce" mentre scrivo il prototipo di cui pubblico il codice su github: <https://github.com/roccosicilia/http_c2>.

## Prototipo (in python)

La componente **C2** (il server) si deve limitare a ricevere i comandi che si vogliono impartire sul sistema target e metterli a disposizione del client che verrà a riederli via HTTP. Il payload da far girare sul **TARGET** deve chiedere, ad intervalli regolari (o irregolari) che comanda va impartito alla macchina target, eseguirlo ed inviare l'output al **C2** server.

<img src="{{ '/assets/images-posts/image-4.png' | relative_url }}" alt="image 4" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Per interagire con il C2 in modo semplice ho pensato di usare un piccolo "client" per inviare al server i comandi da impartire. In questo primissimo prototipo l'output dei comandi viene visualizzato nei log del server.

## Test in lab

Vi lascio un video in cui racconto brevemente perché mi sono messo a giocare con questo prototipo che ha finalità puramente accademiche:

Il codice del prototipo è in questo path della repo: <https://github.com/roccosicilia/http_c2/tree/main/HTTP_custom>. Il file [server.py](https://github.com/roccosicilia/http_c2/blob/main/HTTP_custom/server.py) si riferisce, ovviamente, alla componente server da avviare sulla macchina che si vuole usare come C2.

<img src="{{ '/assets/images-posts/image-1.png' | relative_url }}" alt="image 1" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Server in esecuzione nel mio LAB.

Il file [payload_win.py](https://github.com/roccosicilia/http_c2/blob/main/HTTP_custom/payload_win.py) è lo script da far eseguire alla macchina target ed è la parte che probabilmente subirà più manipolazioni in quanto questo script deve necessariamente passare inosservato ai sistemi di Detection lato endpoint. È un semplicissimo python script che genera GET e POST, quindi di per se non fa nulla di male e, come appurato in diversi contesti, non dovrebbe essere identificato come minaccia ne a livello di analisi statica ne all'esecuzione. Mentre scrivo lo script viene eseguito serenamente su un host windows con i sistemi di Detection di base attivi (Defender).

<img src="{{ '/assets/images-posts/image-2.png' | relative_url }}" alt="image 2" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Target VM.

**Non affrontiamo ora il tema della Detection**, ma uno degli obiettivi è quello di restare quanto più possibile invisibili. Per fare un'esempio: scenari simili in powershell verrebbero immediatamente intercettati da WinDefender. Ci limitiamo a considerare che la componente "agent" appare innocua all'avvio dello script e ciò che potrebbe insospettire l'EDR è ciò che avviene dopo, ad esempio analizzando i comandi che vengono impartiti all'endpoint.

Nel file [cli.py](https://github.com/roccosicilia/http_c2/blob/main/HTTP_custom/cli.py) per ora ho predisposto un semplice menu con due scelte: una per uscire dal programma ed una per inserire manualmente un comando da impartire sul target.

<img src="{{ '/assets/images-posts/http_c2_test.png' | relative_url }}" alt="http_c2_test" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Esempio di esecuzione di un comando nel mio LAB.

Probabilmente è l'anima *smanettona* che lo richiede, ma mi piace tenere separata la componente puramente client per interagire da "cli" con il server. Una giusta evoluzione potrebbe essere quella di portare l'output sul client ed aggiungere qualche opzione/funzione al menu.

## Perché il modello funziona?

Le infrastrutture Command and Control (che abbreviamo con C2) sono abbastanza complesse, soprattutto quando sono ricche di funzionalità, ma il principio di base è molto semplice e sfrutta i modelli con cui progettiamo e realizziamo le reti e i possibili entry point delle aziende/organizzazioni. Scomporre ai minimi termini questo tipo di infrastruttura ci permette - credo - di visualizzare meglio i motivi che le rendono così efficaci.

Partirei dalla delivery del payload che spesso è un pezzo di software estremamente ridotto che deve solo preoccuparsi di installarsi sulla macchina target e contattare il C2 per ricevere istruzioni. La via più "semplice" è fare in modo che un utente della rete riceva il nostro pacchetto regalo e lo esegua sulla propria workstation.

Nel mondo vero questo avviene, purtroppo, molto frequentemente: dalla tipica email con allegato il payload camuffato da altro al messaggio contraffatto di un collega/amico/conoscente che ti chiedere di scaricare un documento infetto. Qualche anno fa, giusto per fare un esempio reale, durante un security test il team con cui lavoravo aveva individuato una falla nel portale HR del target tramite cui era possibile eseguire upload arbitrari di file camuffati da CV dei candidati. Ipotizzando che quei file sarebbe stati scaricati ed aperti dal personale interno si decise di presentare delle candidature fittizie allegando il nostro payload camuffato da CV. Il giochetto funzionò.

Già in questa prima fase operativa ci sono (dovrebbero esserci) delle barriere da oltrepassare: email con link sospetti potrebbero essere analizzate dai sistemi di email security, file scaricati sulla workstation potrebbero essere analizzati staticamente dagli anti-malware, i nuovi processi potrebbe eseguire azioni sospette intercettate dell'EDR, le connessioni verso il C2 potrebbero insospettire l'IDS del firewall. Il potenziale lato difesa c'è, ma molto dipende dalla configurazione di questi sistemi e da chi li sta presidiando; considerando che queste tecniche sono ancora utilizzate e funzionanti è molto probabile che sul grado di confidenza con le capacità di detection dei sistemi dobbiamo ancora lavorarci parecchio.

Va anche considerato che non sempre gli endpoint sono nella condizione di essere protetti: un utente che opera remotamente rispetto alla propria sede molto probabilmente non può beneficiare di tutti i sistemi di sicurezza che sono presenti presso gli uffici, soprattuto in relazione alla navigazione. Per inciso, ci sono soluzioni anche per questo scenario ma la loro applicazione è abbastanza limitata, nella maggior parte dei casi un utente che usa il proprio laptop da casa mantiene le protezioni a livello email security ed endpoint security ma parte delle protezioni a livello rete non ci sono.

---

Se gli argomenti che porto su questo blog e sui miei canali ti interessato puoi iscriverti al blog lasciano la tua email:

Per sostenere il mio progetto di divulgazione ed accedere a contenuti dedicati ai supporter puoi [iscriverti al mio canale Patreon](https://patreon.com/roccosicilia).

---

Il secondo punto di attenzione è ciò che avviene una volta che il paylaod ha fatto quello che doveva fare, ovvero installarsi sulla macchina target. Tralascio in questo post i vari trucchi che si possono usare e su cui torno nei prossimi capitoli, per ora ci basta riflettere sulle azioni che il software compie e gli strumenti che abbiamo per intercettarle.

Questa fase è per me la più affascinante e individuo due famiglie di "comportamenti":

- eseguire attività per le quali non c'è detection
- eseguire attività assimilabili al comportamento della rete

Nel prototipo in lavorazione vorrei lavorare sulla seconda opzioni: se una rete è popolata da utenti è relativamente semplice ipotizzare che tipo di azioni sicuramente vengono eseguite. Ad esempio durante la navigazione web eseguire delle GET di contenuti o delle POST di dati per una login è assolutamente normale. Quindi un software che si limita, almeno a livello rete, ad eseguire GET e POST non dovrebbe insospettire più di tanto.

Più complesso è rimanere "nascosti" quando si eseguono operazioni sull'endpoint, il nostro amico EDR è il più grande alleato che il team di difesa ha a disposizione e, come mi avrete sentito spesso dire, viene usato ancora molto male.

## Next step

Lascio qui il link ad un breve video con le anticipazioni sul progetto che ho pubblicato su github: <https://www.patreon.com/posts/c2-custom-119154565>.

[<img src="{{ '/assets/images-posts/image-3.png' | relative_url }}" alt="image 3" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />](https://www.patreon.com/posts/c2-custom-119154565)

Video-anticipazione con qualche dettaglio tecnico.

Come accennavo il prototipo nasce per una mia esigenza operativa, quindi nei prossimi giorni inserirò nuove funzionalità utili ai miei scopi e sfrutterò l'occasione per approfondire il tema C2.
