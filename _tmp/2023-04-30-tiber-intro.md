---
layout:     post
title:      "TIBER-*: intro"
date:       2023-04-30 23:00:00 +0200
categories: [cyber-security, ita, vlog-podcast]
image:
---
Il mondo dell'information security ha con il tempo sviluppato modelli e framework per strutturare molti processi di gestione del rischio cyber. Alcuni sono diventati un punto di riferimento assoluto (vedi NIST o ISO 27001/27002, [lascio qui il link](https://www.bitsight.com/blog/7-cybersecurity-frameworks-to-reduce-cyber-risk) una lista con qualche descrizione utile) e spesso vengono adottati anche solo parzialmente o vengo utilizzati come "fonte di ispirazione" dei temi che si occupano della gestione della sicurezza delle informazioni e dei sistemi.

TIBER, che per la cronaca è l'acronimo di ***Threat Intelligence Based Ethical Red-Teaming***, è un altro framework che la ECB (European Central Bank) - che in Italia amiamo tradurre con Banca Centrale Europea o BCE - ha abottado con lo scopo di fornire uno strumento di testing e miglioramento dealla resilienza cybernetica tramite l'esecuzione di simulazioni di attacco. Semplificando all'estremo utilizzo una della mie frasi tipiche: per far saltar fuori il problema devi mettere alla prova l'intera struttura a sollecitazioni reali.

In un certo senso ci stiamo dicendo che i Vulnerability Assessment ed i Penetration Test restano utili e necessari ma non bastano più. O meglio, questa è la conclusione a cui sono giunti gli ideatori del modello qualche anno fa, chi lavora nel settore ne è ben conscio da molto più tempo.

Con questo post vorrei iniziare a raccontare il contenuto del framework "TIBER-EU" e della relativa "Guida Nazionale TIBER-IT" e forse anche qualche elemento della versione tedesca "TIBER-DE". Inizierei dalla documentazione disponibile e dai cui io stesso ho iniziato, qualche tempo fa, lo studio di questo framework.

<img src="{{ '/assets/images-posts/tiber-docs.png' | relative_url }}" alt="tiber docs" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

documentazione di riferimento

Sul sito della ECB [è disponibile una intro al framework](https://www.ecb.europa.eu/paym/cyber-resilience/tiber-eu/html/index.en.html) con alcune F.A.Q. ma i primi veri documento da prendere in considerazione sono:

- il documento che descrive il [TIBER-EU Framework](https://www.ecb.europa.eu/pub/pdf/other/ecb.tiber_eu_framework.en.pdf) a cura della ECB
- la [Services Procurement Guidelines](https://www.ecb.europa.eu/pub/pdf/ecb.tiber_eu_services_procurement_guidelines.en.pdf) in riferimento alla scelta dei team esterni incaricati dei servizi di Threat Intelligence e Red Teaming
- la [White Team Guidance](https://www.ecb.europa.eu/pub/pdf/other/ecb.tibereu.en.pdf) in riferimento al team interno che dovrà gestire i test

Questi documenti danno una buona panoramica del modello a cui è da aggiungere un documento relativo alle [Purple Team Best Practice](https://www.ecb.europa.eu/pub/pdf/other/ecb.tiber_eu_purple_best_practices.20220809~0b677a75c7.en.pdf).

Direi che per iniziare è sufficiente questo. Partiremo quindi da come è strutturato il framework per poi andare a vedere nel dettaglio come è stato implementato per l'Italia e, visto che lavorativamente è probabile che che mi capiti, per la Germania. Guarderemo quindi rispettivamente la documentazione relativa alla [TIBET-IT](https://www.bancaditalia.it/compiti/sispaga-mercati/tiber-it/Guida_Nazionale_TIBER-IT.pdf) ed alla [TIBER-DE](https://www.bundesbank.de/resource/blob/848920/f6a89c2754759b4843811ac97a7314cb/mL/tiber-implementierung-data.pdf).

Ai principali documenti citati se ne aggiungo molti alti di approfondimento (alcuni sono citati nello schema allegato) che prenderemo in considerazione strada facendo. Pronti?

## Gli obiettivi del framework

Di base la volontà è di fornire un metodo standard e di validità europea agli enti finanziari (ma il modello è estendibile a chiunque) per verificare le capacità di individuazione e gestione delle minacce cyber tramite l'implementazione di security test condotti in modo da simulare scenari di attacco reali. A tal proposito si fa riferimento a due concessi chiave che il framework integra: la Threat Intelligence ed il Red Teaming.

Un framework comune consentirebbe agli enti di utilizzare metriche simili per valutare e riconoscere il livello di resilienza cyber delle varie entità, semplificando le verifiche tra enti di differenti stati e riducendo gli oneri burocratici che deriverebbero dall'utilizzo di modelli divverenti all'interno dell'EU.

Pur proponendo un modello comune il framework consente ai singoli stati/giurisdizioni una certa flessibilità nell'implementazione del modello TIBER. In questo momento gli stati che hanno adottato il framework sono: Belgio, Danimarca, Finlandia, Germania, Irlanda, Italia, Lussenburgo, Olanda, Norvegia, Portogallo, Romania, Spagna e Svezia. Di fatto esistono enti che non operano sul territorio di un singolo stato, anche in questo caso un framework comune aiuterà i grandi gruppi ad implementare test coerenti nonostante il contesto internazionale.

## Cosa cambia rispetto alle metodologie già adottate?

La principale evoluzione sta nel prevedere un modello di testing che, a livello europeo, preveda di eseguire delle simulazioni di attacco realistiche i cui esiti, opportunamente descritti nei report, saranno utilizzati per valutare la postura di sicurezza dell'ente. Le attività di Red Teaming non si limitano alla verifica ed allo sfruttamento di una o più falle: vengono eseguite approfondite ricerche sul target per valutare la strategia e le tecniche da utilizzare per l'attacco che potrebbe essere eseguito non solo a livello "digitale". Il Red Team prende in considerazione anche la possibilità di accedere alle infrastruttura fisicamente ed utilizza tecniche di social engineering per ingannare, se possibile, i membri dell'organizzazione target.

Questa tipologia di test permette di prendere in considerazione molti più aspetti dell'organizzazione in merito alla gestione delle minacce informatiche: competenze, processi, consapevolezza, status dei servizi di detection e prevention, ecc.

## Perché ho deciso di scrivere/parlare di questo framework

Mi occupo di sicurezza informatica e molto spesso proprio di Red Teaming, l'argomento è quindi per me molto in focus con ciò che faccio e che già da anni ho decido di condividere tramite il mio personale blog. TIBER porta all'ettenzione delle aziende strutturate un modello e delle metodologie di security test che per molte figure del settore rappresentano al momento l'unico modo per quantificare in modo accurato il rischio cyber e gli impatti correlati a specifici scenari di attacco.

L'argomento forse non è affascianante come un Buffer Overflow ma mi da modo di approfondire e discutere molti aspetti della sicurezza offensiva.
