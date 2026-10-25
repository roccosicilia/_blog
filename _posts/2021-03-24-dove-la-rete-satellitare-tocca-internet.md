---
layout:     post
title:      "Dove la rete satellitare “tocca” Internet."
date:       2021-03-24 09:00:00 +0100
categories: [cyber-security]
image:
---

Come avevo accennato in un podcast di qualche giorno fa, uno dei temi di ricerca che sto portando avanti ha a che fare con le comunicazioni satellitari, o per meglio dire riguarda le tecnologie che ci consentono di comunicare con e tramite i sistemi satellitari.

Potrebbe sembrare un tema distante ma in questa epoca storica è in corso una vera e propria rivoluzione in merito a ciò che stiamo mandando in orbita bassa e a come possiamo utilizzare questi oggetti. Qualche nota di contestualizzazione è doverosa per comprendere il tema.

## Scenario

Per prima cosa va detto che i satelliti moderni posso essere anche molto piccoli: esistono diverse aziende che producono e lanciano mini satelliti delle dimensioni di pochi centimetri ed equipaggiati con non poca tecnologia per la rilevazione e la comunicazione a terra (personalmente seguo il [progetto CubeSat](https://it.wikipedia.org/wiki/CubeSat) nato presso l’Università Politecnica della California). Parallelamente grazie a progetti come il celeberrimo SpaceX (e ne stanno arrivando altri) i costi per mandare asset in orbita si stanno riducendo enormemente.

<img src="{{ '/assets/images-posts/sat.webp' | relative_url }}" alt="Satellite" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

L’ovvia conseguenza è un aumento del “traffico” in orbita bassa, ovvero in quella regione attorno al nostro pianeta in cui vengono tipicamente collocate le costellazioni di satelliti per le comunicazioni, il tracciamento della posizione e rilevamenti di ogni tipo, per uso civile, commerciale e militare.

Da quando i satelliti sono diventati uno strumento anche ad uso civile, se un’azienda ha bisogno di eseguire un determinato tipo di rilevamento o deve comunicare, ad esempio, con la propria flotta navale/aerea/stellare (Starfleet, cit.) si può rivolgere ad un ente che si occupa di lanciare e gestire i propri satelliti tramite cui eroga un servizio e, nei limiti della tecnologia e degli strumenti disponibili, l’azienda cliente è messa in condizione di fruire dei servizi offerti.

Il nuovo modello che sta emergendo frammenta ulteriormente le competenze, consentendo — per come la vedo io — un miglioramento in termini di usabilità ed accesso a questo tipo di tecnologia. Il modello si presenta più o meno così:

- chi ne capisce di satelliti si dedica alla progettazione e realizzazione di strumenti ricchi di tecnologia ma molto piccoli e leggeri
- chi ne capisce di razzi e vettori si dedica a progettare ed implementare un servizio di trasporto in orbita bassa
- chi ne capisce di telecomunicazioni si dedica a costruire una rete di comunicazione satellitare che sia in grado di dialogare con molte tipologie di satellite e mette a disposizione le interfacce

A questo punto le aziende il cui modello di business dipende o sfrutta una tecnologia che necessita di una rete satellitare possono rivolgersi ad una serie di interlocutori specializzati che gli consentiranno di acquisire una tecnologia come i CubeSat, di spararla in orbita e di collegarla a sistemi a terra che consentano l’accesso ai dati/servizi di cui hanno bisogno, senza doverti preoccupare dell’immensa infrastruttura che c’è dietro e con investimenti molto inferiori rispetto a solo 10 anni fa.

Un bel tassello di questo complesso puzzle lo mette a disposizione Amazon con il servizio AWS Ground Station che da la possibilità ad un’azienda di interconnettere un proprio satellite alle “stazioni a terra” di Amazon che gestiranno la comunicazione con l’orbita bassa. Inoltre il servizio mette a disposizione gli strumenti per collezionare i dati ed eseguire le eventuali analisi. Anche su questo fronte credo si possa ipotizzare che Amazon non sarà certo l’unica a muoversi in questo campo.

## Dal punto di vista del White Hat

Premetto che questo tipo di tecnologia mi affascina enormemente, tanto quanto mi affascina l’hacking, la fisica e l’esplorazione spaziale. Sono frontiere che vengono quotidianamente abbattute, sono nuovo opportunità per la specie se sapremo utilizzarle.

Chi lavora e fa ricerca nel campo della sicurezza cyber e ha un po’ di esperienza, al solo pensiero di prendere un oggetto che orbita attorno al pianeta e che rileva dati potenzialmente molto delicati e metterlo in comunicazione, seppur tramite più layer fisici e logici, con la rete internet attraverso un servizio cloud… probabilmente è svenuto prima di aver letto tutta la frase.

Non c’è nulla di sbagliato nelle intenzioni, **esiste però qualche trilione di fattori da considerare** per implementare e renderle fruibili queste infrastrutture in modo sicuro. Qualche tempo fa ho azzardato una previsione — non ricordo se l’ho scritta o detta — in relazione ai sistemi di comunicazione satellitare identificando come **potenziale punto debole la Ground Station**. Prendendo visione di come si stanno rendendo accessibili queste tecnologie mi viene qualche dubbio anche sulle possibilità di configurazione ed integrazione delle piattaforme cloud, non per fattori legati alla tecnologia, bensì in riferimento alla capacità di costruire adeguate policy di sicurezza.

Lo scenario e così complesso e la tecnologia così potente da richiedere una riflessione subito, ben prima che diventi qualcosa di largamente utilizzato. A questo tema sicuramente dedicherò qualche laboratorio di approfondimento e ne parlerò nei prossimi podcast. Mi piacerebbe sentire la campana di qualcuno del settore aerospaziale (militare e/o civile).