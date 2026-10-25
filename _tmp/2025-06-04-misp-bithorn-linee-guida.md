---
layout:     post
title:      "MISP (BitHorn): linee guida"
date:       2025-06-04 23:30:00 +0200
categories: [cyber-security, hacking, ita]
image:      /assets/images-posts/screenshot-2025-06-04-at-22.26.20.png
---
In questi giorni sto ragionando sulle linee guida da proporre alla community, nel senso "MISPoso" del termine, per inserire nuovi eventi all'interno dell'istanza che gestisco/gestiamo: <https://misp.bithorn.org>.

## Concetto di *evento*

Chi fa ricerca in ambito Threat Intelligence o lavora in contesti di difesa avrà probabilmente più occasioni per creare un evento. Il concetto di base prevede la registrazione delle informazioni di un certo evento (es: un incidente o un report) in un "contenitore". In questi casi il ricercatore potrà creare un evento nella piattaforma MISP con i relativi oggetti e attributi.

## Aggregati

Solitamente, come appena detto, ad uno specifico contesto corrisponde un evento: due incident == due eventi distinti, un incident ed un'analisi di un malware == due eventi distinti. Ma nel nostro progetto vorrei prevedere una eccezione.

Aggregare attributi in un singolo evento MISP è accettabile se hanno senso insieme: possiamo quindi mettere più indicatori (IP, domini, hash, ecc.) nello stesso evento se fanno parte dello stesso incidente (come detto), della stessa campagna, **o arrivano dallo stesso report o fonte di intelligence**. Quindi l’aggregazione solo perché sono tutti IP non è una buona idea, ma se si stanno analizzando tutti gli IP usati da Shodan.io per eseguire le scansioni allora ha senso creare un evento unico.

## Sighting / Segnalazione

La gestione di questo parametro degli attributi/artefatti è ciò che ha fatto nascere il progetto ***eg0n*** ora esteso ad una integrazione con MISP. Purtroppo anche MISP su questo tema ha delle rigidità a livello di integrazione. Ad ogni modo per la community è fondamentale anche poter ricevere dei feedback sulla presenza di specifici IoCs all'interno delle reti o dei sistemi di chi ha attivato un processo di hunting all'interno del proprio team.

È fondamentale che la segnalazione non sia "a sentimento": decidere di confermare un IoC significa averlo osservato sui propri logs/sistemi di detection. Sull'attribuzione delle segnalazioni definiremo un processo di verifica/qualifica, ma resta una parametro "della community".

## Prossimamente ne parliamo ...

<img src="{{ '/assets/images-posts/image.png' | relative_url }}" alt="image" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Ho aperto un sondaggio sul [server Discord](https://discord.com/channels/980421363078664222/980421363078664225/1379490553498046586) per trovare una data comoda alla maggior parte degli interessati al progetto ed organizzare un piccolo virtual-meeting per discutere delle linee guida e del progetto.

L'occasione è anche perfetta per fare una piccola panoramica della struttura sino ad ora attivata e dei task che stiamo ipotizzando di mettere in roadmap. Il sondaggio **resta aperto fino alla sera dell'08.06.2025**.

Al momento è disponibile la repo dedicata al progetto in cui raccoglieremo documentazione, scripts, integrazioni e tutto quello che la community produrrà: <https://github.com/b1th0rn/bh-misp>.
