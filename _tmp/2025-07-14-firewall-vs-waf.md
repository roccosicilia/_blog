---
layout:     post
title:      "Firewall vs. WAF"
date:       2025-07-14 18:00:00 +0200
categories: [cyber-security, hacking, ita, study-with-me]
image:      /assets/images-posts/create-a-highly-detailed-high-resolution-image-that-visually-contrasts-a.png
---
Mi avventuro in questo tema per mettere "nero su bianco" alcune considerazioni tecniche in relazione alla scelta di utilizzare un Firewall o un Web Application Firewall. Il motivo principale è una diffusa modesta comprensione degli strumenti.

Mentre il firewall, con riferimento ai moderni sistemi in grado di lavorare anche a livello 7 (L7), sono strumenti tendenzialmente *general purpose*, i web application firewall sono progettati per un ambito specifico: la protezione di applicazioni web (il nome non è casuale). Sto scrivendo l'ovvio, me ne rendo conto, ma per molte persone che dovrebbe saperne di IT questa differenza non è chiara, complice l'evoluzione degli strumenti e la cattiva abitudine di non approfondire abbastanza il funzionamento degli strumenti che il mercato offre.

A livello di funzionalità di protezione L7 i moderni firewall sono dotati di funzionalità che consentono anche di proteggere le applicazioni web da molte tipologie di attacchi. Al netto di quello che potrebbe raccontare il commerciale di turno è in fatto che un firewall ben configurato e con le funzionalità corrette attive sa perfettamente riconosce una tentativo di SQL injection o un Path Traversal Attack. Si tratta di attivare funzionalità specifiche in un contesto che prevede anche molti altri tipi di attacco.

Solitamente il livello di duttilità dei firewall su temi molto verticali come le applicazioni web o altri protocolli molto specifici è limitata. Va infatti considerato che questi sistemi devono anche occuparsi di molte altre tipologie di traffico, sono spesso punto di atterraggio di diversi servizi come le VPN, gestiscono migliaia di regole di traffico tra le reti interne e le reti esterne, per farla breve sono sistemi che hanno un ampissimo set di funzionalità di detection e sono chiamati ad eseguire policy di blocco o allarme in caso di anomalie. Di conseguenza il produttore non può permettersi di "spaccare il bit" a livello di configurabilità su ogni singolo protocollo, si devono fare dei compromessi.

---

Ho parlato di WAF anche all'interno dei miei video-appunti sulle attività di PenTesting in questo video:

[<img src="{{ '/assets/images-posts/screenshot-2025-07-14-at-19.08.04.png' | relative_url }}" alt="screenshot 2025 07 14 at 19.08.04" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />](https://www.patreon.com/posts/ejpt-03-passive-134116623)

eJPT.03 - Passive Information Gathering

---

Il web application firewall è uno strumento che, per quanto riguarda il mondo degli applicativi web, non fa compromessi - o meglio, ne fa infinitamente meno - per quanto riguarda il livello di dettaglio e configurabilità che si può adottare. Di fatto lo strumento stesso è concepito in modo diverso: mentre i firewall si devono occupare di funzionalità di rete di base come routing e nat a cui si sommano componenti di sicurezza come IDS e IPS, i web application firewall - strutturalmente parlando - sono più dei proxy che si fanno attraversare del traffico web, lo ispezionano e applicano controlli e regole basate su ciò che osservano.

Virtualmente il dettaglio di configurazione che si può ottenere con un WAF è replicabile anche all'interno di un firewall tradizionale, ma solitamente ci si scontra con un livello di granularità delle configurazioni che solitamente è inferiore rispetto ad uno strumento dedicato come il Web Application Firewall.

## Qualche conclusione sul tema

Tecnicamente il WAF vi mette a disposizione molte più funzionalità di un Firewall in relazione a ciò che potete fare a livello di protezione ed analisi del traffico WEB. Quindi se avete l'esigenza di proteggere in modo completo un'applicazione che i vostri utenti utilizzano via HTTP/HTTPS è il WAF lo strumento corretto.

I moderni Firewall sono anch'essi provvisti di della capacità di analizzare il traffico HTTP/HTTPS **ed è possibile proteggere anche applicazioni web**, ma il livello di configurabilità ed il livello di dettagli a cui si può scendere per riconoscere un payload è limitato rispetto ad un WAF. In molti contesti potrebbe essere più che sufficiente, ma non aspettatevi lo stesso livello di dettaglio di un WAF. Se dovete proteggere un'applicazione critica è inutile girarci attorno, valutare uno strumento dedicato e configuratelo bene.

**Guai a dare per scontata la cura e la qualità della configurazione**: utilizzare strumenti evoluti per poi implementare le funzionalità base e le configurazioni di default rischia di invalidare completamente l'adozione dello strumento.
