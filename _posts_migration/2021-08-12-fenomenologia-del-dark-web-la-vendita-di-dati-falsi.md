---
layout:     post
title:      "Fenomenologia del Dark Web: la vendita di dati falsi"
date:       2021-08-12 09:51:28 +0200
categories: [cyber-security, ita]
image:
---
In relazione ad un recente e noto attacco informatico ad un ente pubblico italiano ho avuto modo, come molti professionisti e ricercatori del settore, di svolgere qualche analisi per comprende le dinamiche, imparare qualcosa di nuovo e, se possibile, migliorarsi ed aiutare altri a migliorare.

Ieri sera (11/08) ho dedicato un po' di tempo alla lettura di alcuni canali e siti non fruibili nel di superficie e ho trovato un paio di conversazioni interessanti che qui vorrei analizzare almeno in parte.

In entrambi i casi un utente apriva una richiesta di trading manifestando interesse per i dati potenzialmente sottratti durante il noto attacco. Le conversazioni che ho analizzato iniziano a partire dal 3 agosto e gli scambi sono ancora in corso. Il modello è abbastanza tipico: qualcuno chiede, qualcuno risponde e vengono scambiati dei dati parziali a dimostrazione dell'effettivo possesso delle informazioni.

Ho controllato qualche set di dati tutt'ora disponibili su piattaforme di libero accesso (se si ha il link ovviamente) come Pastebin al fine di verificare la potenziale autenticità delle informazioni. Mi sono limitato ad alcuni controlli semplici che qui espongo.

## Profili social

Buona parte dei nominativi ha una o più corrispondenze con profili social sulle principali piattaforme. Ho concentrato alcuni check su LinkedIn per ipotizzare una verosimile età anagrafica e un'area geografica di riferimento.

## Codice fiscale

Con il semplice calcolo "inverso" del codice fiscale esposto è possibile verificare banalmente il nome, data e luogo di nascita. I codici fiscali analizzati avevano effettivamente tutti delle corrispondenze da cui si deduce una possibile autenticità o l'utilizzo di un algoritmo per la generazione dei dati ben fatto (non è cosa difficile).

## Mobile

L'estratto dei dati riportava anche un riferimento mobile sul quale è possibile eseguire una semplice ricerca a livello di presenza su piattaforme come WhatsApp e Telegram. Molti profili (non tutti) risultano presenti ed i numeri sono effettivamente reali, tutta da dimostrare la corrispondenza con il nominativo immediatamente verificabile sono in pochissimi casi.

## Google è tuo "amico"

Ho incrociato i risultati con qualche ricerca a livello web con qualche query strutturata e ne emerge che moltissimi dei dati riportati sono di fatto pubblici, in particolare i numeri di telefono.

<img src="{{ '/assets/images-posts/regione_lazio_trading.png' | relative_url }}" alt="regione_lazio_trading" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Una delle conversazioni su RaidF.

Sommando tutte le informazioni è lecito pensare che questi data set siano stato costruiti ad arte con azioni di scraping, fenomeno che trovo estremamente interessante e da approfondire. Da un lato potrebbe essere il banale tentativo di truffare il truffatore vendendo un falso DB, ma è anche un interessante segnale di "rumore" che può mettere in allarme la vittima in una situazione complicata come quella del ricatto.

Personalmente questo modello mi incuriosisce molto e sarebbe interessante misurare quanti di questi falsi dati vengono scambiati. Interessante anche la facilità con cui è possibile costruire un falso DB verosimile.

In ogni caso questo tipo di scambi è bene monitorarli **e soprattutto verificarli** (mi sono stati segnalati fior di servizi giornalistici non proprio accurati) anche per comprendere come si è evoluto l'attacco. E' un'analisi che aiuta a definire nuove strategie di difesa con l'obiettivo di ridurre il rischio e, dovendo comunque fare i conti con l'eventualità dell'attacco, imparare a gestirlo al meglio.
