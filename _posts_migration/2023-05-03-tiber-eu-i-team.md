---
layout:     post
title:      "TIBER-EU: i team"
date:       2023-05-03 18:00:00 +0200
categories: [cyber-security, ita]
image:
---
Durante la lettura del documento che illustra il framework tutto mi è diventato più chiaro quando sono state mappate le competenze dei team che hanno un ruolo attivo nel processo di testing. Ho quindi pensato di partire dagli attori coinvolti per poi parlare del processo in se.

Per ora è sufficiente sapere che il framework propone una metodologia per eseguire dei test sulla sicurezza dell'organizzazione e questi test hanno la particolarità di simulare, in ogni aspetto, il comportamento di un threat actor. In tal senso la separazione in team è indispensabile in quanto ci sono informazioni che non devono essere distribuite.

Il framework identifica sei stakeholders:

- il Tiber Cyber Team (TCT) ed il relativo Team Test Manager (TTM)
- il White Team (WT) ed il relativo White Team Lead (WTL)
- il Blue Team (BT)
- il Threat Intelligence (TI) provider
- il Red Team (RT) provider
- eventuali agenzie governative di intelligence o enti nazionali attivi sul fronte della cyber security

Partiamo da ***Tiber Cyber Team*** che comprende le autorità nazionali che hanno deciso di aderire al fremework e sono responsabili della realizzazione della guida nazionale per l'implementazione dello stesso. In Italia questa competenza è assegnata a tre enti: **Banca d'Italia, Consob e IVASS**. E' infatti di loro competenza la stesusa ed il mantenimento del documento Guida nazionale TIBER-IT (che prenderemo in considerazione in futuro) e sono anche il riferimento per tutti i **White Team Leads** per eventuali richieste di supporto a livello di supervisione.

Il **White Team** ed il relativo responsabile, denominato **White Team Lead**, è un gruppo di lavoro interno all'organizzazione che desidera utilizzare il framework. Si tratta del team incaricato di coordinare i test interagendo internamente ed esternamente, è infatti l'interfaccia verso il Threat Intelligence provider ed il Red Team provider. Elemento molto importante: **il White Team è l'unico team interno all'ente oggetto dei test a conoscenza dell'attività di verifica**. Le informazioni circa i test non devono cincolare all'interno dell'organizzazione in quanto falserebbero l'esito dei controlli.

Il **Blue Team** è costituito da tutto lo staff dell'organizzazione che non fa parte del **White Team**. Il framework non identifica il Blue Team con un gruppo specifico in quanto, deduco io, tutta l'organizzazione è potenzialmente interessata e coinvolta in un'azione di contrasto ad un minaccia cyber. Solutamente questa "label" viene data a chi opera attivamente le attività di gestione delle minacce a livello tecnico, in questo caso è l'intera organizzazione che ne fa potenzialmente parte.

Il **Threat Intelligence** provider ha l'onere di eseguire le attività di Threat Intelligence e di documentare le informazioni prodotte nella forma del **Targeted Threat Intelligence Report** (spesso abbreviato in TTI Report o TTIR). Con questo report il team identifica i potenziali scenari di attacco per l'organizzazione sulla base delle informazioni raccolte. In questa fase il **Threat Intelligence** provider collabora in modo molto stretto con il **Red Team** provider in quanto questa fase operativa si sovrappone alle attività di ricognizione del Red Team.

Il **Red Team** provider è incaricato di implementare materialmente gli scenari di attacco descritti nel TTI Report. Le attività verranno documentate nel Red Team Test Report con il dettaglio di qualto eseguito, i relativi esiti ed eventuali suggerimenti per migliorare i controlli dell'organizzazione.

Fanno parte degli stakeholders anche eventuali agenzie nazionali di intelligence o cyber security. Su questo fronte non mi avventurerò in approfondimenti.

---

Non ci sono pochi attori all'opera, è evidente una struttura pensata al fine di rendere realistici i test e mantenere un certo livello di controllo sulle attività. Come ho accennato ad inizio post ho preferito prima chiarire quali sono le figure coinvolte mentre nel prossimo post sul tema TIBER-EU si spostiamo sulla metodologia e vediamo se fasi previste per un test completo.
