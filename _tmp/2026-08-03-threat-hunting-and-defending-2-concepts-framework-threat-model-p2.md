---
layout:     post
title:      "Threat Hunting and Defending #2: concepts, framework, Threat Model (p2)"
date:       2026-08-03 18:00:00 +0200
categories: [cyber-security, hacking, ita, study-with-me]
image:      /assets/images-posts/gemini-threat-hunting.png
---
Come detto nei precedenti blog-post, la disciplina richiede l'acquisizione di diverse skills che, per essere applicate con efficacia ed in modo efficiente, devono essere affiancate a **strumenti e piattaforme** dedicate.

Il processo di hunting parte dalla formulazione di un'ipotesi relativa a possibili minacce che possono riguardare le infrastrutture che vogliamo proteggere. Per verificare l'ipotesi è necessario accedere alle informazioni ed ai sistemi sotto il proprio controllo e per ovvie ragioni sarebbe impensabile operare direttamente sui singoli host. Solitamente è necessario disporre di strumenti dedicati da utilizzare nel day-by-day per attività come la verifica di logs, eventi ed anomalie al fine di metterle in relazione con TTPs o comportamenti sospetti.

Se trovi utili i contenuti che condivido e vuoi aiutarmi a migliorare il mio progetto di divulgazione iscriviti e abbonati [al mio Substack](https://roccosicilia.substack.com/subscribe).

Solitamente i tools con cui si deve prendere confidenza sono:

- Piattaforme di Threat Intelligence (TIP)
- Security Information and Event Management system (SIEM)
- Soluzioni di Security Orchestration, Automation and Response (SOAR)
- XDR / EDR / NSM / DPL
- Sistemi di Threat Emulation
- vari tools specifici utili all'analisi dei dati

La soluzione che "fa tutto" e copre tutte le casistiche non esiste, solitamente ci si affida a più soluzioni di cui si cerca un certo livello di integrazione. In questo senso si parla per lo più di piattaforme dedicate al threat hunting: un insieme di soluzioni e strumenti che l'hunter utilizza in modo strutturato.

È sicuramente necessario disporre di qualcosa dove archiviare ed organizzare le informazioni, non a caso si citano SIEM e vari software che raccolgono log e telemetria. È sicuramente necessario disporre di strumenti che ci consentano di applicare logiche di machine learning ed analisi del comportamento. Non va dimenticata l'esigenza di automatizzare task e la possibilità di generare report ed analitiche.

Sulle **piattaforme di Cyber Threat Intelligence** (TIP) bisogna dedicarci un po' di spazio. La Cyber Threat Intelligence genera molte informazioni:

- dati provenienti da attività di OSInt
- ricerche eseguite da analisiti
- collection di dati telemetrici
- informazioni provenienti da studi in collaborazione tra team e ricercatori indipendenti

Le informazioni raccolte consentono di individuare e catalogare gli elementi costitutivi degli attacchi informatici, quelli citati nella *[pyramid of pain](https://roccosicilia.com/2026/07/16/threat-hunting-and-defending-2-frameworks-p1/)* nel precedente post. È una mole di dati enorme che vien continuamente arricchita ed aggiornata e che richiedere una certa gestione dello storico: alcuni elementi sono molto effimeri come IP e HASH, antro sono molto più strutturati come i TTPs.

Solitamente gli analisti utilizzano database di terze parti per accedere a questa enorme mole di informazioni. Ad esempio nel [mio contesto lavorativo](https://www.linkedin.com/posts/roccosicilia_cybersecurity-realismo-share-7483217213320151041-83Z0/?utm_source=share&utm_medium=member_desktop&rcm=ACoAAATK5U0By2qlNbOT_QThQp0s692DGhr_JfU) usiamo molto Cisco Talos e Unit42 come fonti enterprise assieme a molte altre fonti disponibili pubblicamente o parzialmente pubbliche.

Come si può intuire si lavora a più livelli. I ricercatori studiano ed analizzano i nuovi vettori di attacco, nuove tecniche e nuove vulnerabilità. La telemetria generata dai sistemi di detection come IDS, Firewall e EDR consentono di osservare eventuali elementi tecnici relativi ad eventi sospetti. Le piattaforme di Cyber Threat Intelligence pensate per organizzare i dati raccolti, gestire priorità ed in generale supportare l'attività di analisi.

Nel materiale relativo alla certificazione Cisco sono citate alcune piattaforme specifiche per le quali è necessario avere degli accessi con sottoscrizione. In questa occasione le cito e prendo spunto per cercare anche qualche alternativa open.

**ThreatConnect** è una piattaforma che mette a disposizioni, oltre alle fonti dati, integrazioni con sistemi SIEM, SOAR, EDR e NSM. La piattaforma è a pagamento ma il vendor mette a disposizione un altro tool per lo scambio federato di informazioni: [Polarity](https://knowledge.threatconnect.com/docs/polarity). Sembra interessante e me lo appunto per fare dei test.

**Anomali** è un'altra piattaforma di CTI per la condivisione di feeds qualificati, tema che ho spesso discusso quando ho parlato di CTI feeds. Anche questa piattaforma è prettamente ad uso commerciale e si accede tramite subscription ma ho notato che c'è un'interessante [utility per la gestione di feed](https://www.anomali.com/resources/staxx) STIX/TAXII. Anche questa da indagare.

**Recorded Future** probabilmente non ha bisogno di presentazioni, piattaforma nota e molto utilizzata per l'analisi di dati CTI che integra funzionalità tipiche degli LLM per agevolare il lavoro degli analisti. Ho avuto modo di metterci le mani grazie al fatto che è tra i prodotti proposti da [NTS](https://nts.eu/?utm_source=roccosicilia), la company per cui lavoro.

Anche questa piattaforma richiede una subscription per essere utilizzata ma mette a disposizione un set di tools free interessanti che [potete trovare qui](https://www.recordedfuture.com/get-started#free-tools).

**Intel 471** è una piattaforma specializzata nell'analisi e condivisione di informazioni provenienti dal monitoraggio delle Dark Net. Molto interessante ed utile anche prendere visione periodica del blog e dei [post relativi alle nuove minacce](https://www.intel471.com/blog?category=emerging-threats).

**IBM X-Force Exchange** è una piattaforma di condivisione di dati analiticy in relazione a threats e feeds oltre che diversi reports. Molto utile anche per [ricerche realtime di IoC](https://exchange.xforce.ibmcloud.com/).

**MISP** è un progetto open-source per la condivisione di informazioni di cui ho parlato molto in questo [blog](https://roccosicilia.com/?s=MISP) e sul canale [YouTube](https://www.youtube.com/@roccosicilia/search?query=MISP).

Curiosamente assente, nell'elenco proposto dal materiale di studio della certificazione, **VirusTotal** di Google.

Disporre di dati valutati e commentati da altri analisti da la possibilità di valutare nuovi criteri di ricerca all'interno della nostra base dati di eventi e ci consente di comprendere meglio gli elementi che stiamo osservando.

Ovviamente questi dati vanno condivisi in qualche modo ed esistono standard specifici per la loro formattazione e condivisione. Su questo tema ho avuto modo di sperimentare la complessità della cosa ed i problemi di integrazione che le piattaforme presentano. Di base il formato più diffuso è STIX v2.x (Structured Threat Information Expression), ovvero una struttura dati JSON che consente di descrivere IoC, vulnerabilità, campagne e threats in generale.

Solitamente si associa questo formato STIX a TAXII come metodo di trasporto, ovvero la speficia standard delle RestFull API per scambiare dati in formato STIX v2.x. La versione 1.x di STIX aveva una struttura XML ed è incredibilmente ancora utilizzata da alcuni vendor nonostante i limiti ed il fatto che sia considerata obsoleta.

Altri due formati spesso utilizzato sono:

- OpenIOC, una struttura XML molto flessibile per descrivere IoC
- Cyber Observable Expression (CybOX): una struttura standard per documentare gli elementi osservabili di un threat.

#### Focus sulle piattaforme Cisco

Nel mondo Cisco le piattaforme che rientrano nel contesto sono sicuramente il SIEM Splunk (famosa acquisizione) il relativo SOAR Phantom e la piattaforma Cisco XDR che, a divverenza dagli altri XDR, funziona da aggregatore ed orchestratore più che da EDR ***eXtended***.

Il SIEM è per lo più un oggetto passivo: Splunk riceve dati dalle diverse sorgenti, per lo più logs ed eventi vari. Ovviamente con questi dati ci possiamo fare un sacco di cose:

- Analisi e correlazione
- Analisi forense
- Verifica della compliance **
- Audit
- Alerting
- Dashboard di controllo
- Report
- ...

** Sul tema compliance ho in mente un lab relativo ai CIS Benchmark che penso possa essere molto utile. Vorrei sperimentare la possibilità di controllare il livello di hardening dei sistemi usando strumenti solitamente già attivi come SIEM o EDR.  
  
Non ho una previsione di quando lo farò, mi è venuto in mente oggi lavorando ad un task :-) ma se segui il blog o il mio [substack](https://roccosicilia.substack.com/subscribe) ti arriverà la notifica.

Una piattaforma XDR "classica" solitamente si presenta come un EDR a cui è stata data la possibilità di ricevere ed elaborare anche dati provenienti da altri sistemi oltre ai classici endpoint (solitamente sistemi client e server di vario tipo). La cosa curiosa è che gli XDR tradizionali si sono di fatto evoluti in ecosistemi EDR + SIEM (ne avevamo parlato in diverse puntate podcast).

Cisco ha scelto un'altra via, l'XDR non integra funzionalità SIEM o EDR ma è uno strumento di aggregazione di diverse soluzioni e dispone di connettori utili a dialogare in modo bidirezionale con tutti gli strumenti (Cisco e non) utilizzati per la gestione della postura di sicurezza. Inevitabilmente ci sono funzioni che si sovrappongono agli EDR ed ai SIEM.

#### Threat Emulation Tools

Un elemento molto utile per misurare e verificare il buon funzionamento di una soluzione di detection e le capacità di hunting sono i tools di emulazione in grado di eseguire azioni offensive reali/realistiche verso sistemi di test.

Ne esistono di diversi tipi ed il più famoso è probabilmente **Mitre Caldera**. Giusto citare un altro strumento open-source: **Red Canary Atomic Red Team**.

#### Threat Hunting Tools

Al di la delle piattaforme ci sono strumenti di specifici con cui è necessario prendere confidenza.

**YARA rules**  
Yet Another Recursive Acronym è un sistema open-source per identificare specifici patters relativi a files, processi, dati in memoria o altri elementi che si desidera intercettare in una base dati. Utili per descrivere in modo strutturato gli elementi che si vogliono cercare in fase di threat hunting.

**Active Countermeasures AC-Hunter**  
Strumento ideato per intercettare anomalie a livello rete ed in particolare i classici pappern di traffico dei command-and-control.

**Elastic**  
Nulla da aggiungere, se segui i miei LAB ne hai visto il potenziale ed in questa serie farò nuovi test.

**CyberChef**  
Anche su questo tool direi che non c'è bisogno di dire nulla, se non lo conosci probabilmente hai iniziato da poco il tuo viaggio nella cyber security.

**Analisi forense della memoria**Alcune minacce non si basano su files eseguibili o script ma sono semplici comandi eseguiti direttamente in memoria. Bisogna poter analizzare anche quest'area del sistemi a caccia di anomalie. Volatility è forse uno dei tool più noti in questo ambito.

#### Note conclusive

Con lo studio di questo capitolo ho messo in roadmap l'inserimento nel mio LAB di un sistema Ansible per gestire eventuali automazioni e una macchina dedicata a Mitre Caldera. Affiancherò anche una istanza Splunk di test al già presente Elastic.

Sarà anche utile la piattaforma MISP gestisco per i miei test e che ho reso disponibile pubblicamente (progetto portato avanti con la community BitHorn).
