---
layout:     post
title:      "Threat Hunting Process."
date:       2026-10-14 21:00:00 +0200
categories: [cyber-security]
image:      /assets/images-posts/gemini-threat-hunting.webp
---

Il Threat Hunting è un processo molto strutturato che richiede metodo, competenze specifiche a strumenti adeguati. Per eseguire attività di hunting con efficaci è necessario comprendere ed implementare correttamente i principi chiave della disciplina.

- Esistono due principali tipologie di hunting: proattivo e reattivo. Nel primo caso il processo viene eseguito secondo un programma continuativo di esercizi di hunting, nel secondo caso il processo viene "attivato" dall'esigenza di analizzare in dettagli eventuali eventi sospetti.
- Sul piano tattico l'esercizio di hunting è guidato da ipotesi di nuovi scenari di attacco, analisi di nuovi dati o la consapevolezza di nuove minacce che possono interessare un target.
- Un processo di hunting deve essere efficiente, deve quindi essere identificato un preciso scope per evitare di condurre esercizi complicati dalla vastità degli asset coinvolti.
- Il processo di hunting è da considerarsi un'attività pianificata in cui viene definito lo scope, le risorse e gli strumenti da utilizzare per le Operations.
- Gli esercizi di hunting devono essere strutturati e documentati: l'utilizzo dei framework possiamo considerarlo NON opzionale.

Questi sono i principi di base del processo di Hunting che verranno affrontati in questo capitolone.

>Questa serie di articoli viene dai miei appunti di studio sul Threat Hunting e dal confronto con varie figure dell'information security tra cui diversi analisti del mondo della Defense. Se gli argomenti che porto sul blog ti solo utili puoi iscriverti o seguirmi su una delle piattaforme dove pubblico regolarmente contenuti. **Trovi tutte le info nella pagina [Divulgazione]({{ '/divulgazione' | relative_url }})**.

## Approccio al Threat Hunting

<img src="{{ '/assets/images-posts/threat-hunting-process.webp' | relative_url }}" alt="image 3" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

I servizi di Detection erogati da strutture come i SOC devono utilizzata un processo di qualifica ed assegnazione delle priorità agli eventi registrati da strumenti come i SIEM e gli XDR. La metodologia con cui viene definita la priorità spesso dipende dal framework che si è deciso di adottare e gli strumenti a disposizione.

Se un evento viene classificato come "True Positive", in quanto l'analisi iniziale lo interpreta come effettivo tentativo di attacco, viene attivato il processo di investigation per comprendere cosa sta succedendo sul sistema. In questo caso si ha un task di hunting *generato* da una nuova evidenza da indagare.

L'analisi produrrà delle nuove evidenze in merito a "firme", tattiche o comportamenti malevoli che potranno poi essere comunicate al SOC Team che le utilizzerà come fonti di intelligence da utilizzare per migliorare il processo di monitoraggio.

Questo modello viene definito ***Reactive Threat Hunting***: a seguito di una segnalazione o un incidente viene investigato in dettaglio ciò che è successo partendo dal primo evento della Kill Chain ed arrivando ad approfondire e documentare tutto ciò che è avvenuto a livello rete e sistemi.

Questo approccio consente di individuare ed analizzare GAP nella detection, nuovi IOCs e comportamenti che gli strumenti di monitoraggio hanno potuto intercettare solo in parte. Non è necessario che l'incidente sia in corso, l'attività può riferirci anche a situazioni passate già gestite di cui si vuole però approfondirete lo stato dei sistemi o individuare nuovi elementi per la comprensione e gestione della minaccia. L'attività non va confusa con l'incident response che ha finalità completamente differenti: si tratta di due task complementari che richiedono differenti metodologie e tempistiche.

L'altra faccia della medaglia è il ***Proactive Threat Hunting***: non ci sono eventi scatenanti ma la volontà di individuare nuove tipologie di minacce che possono aver interessato l'infrastruttura target. Si tratta quindi di un processo che viene reiterato secondo una pianificazione che può essere "alimentata" da report di threat intelligence, ipotesi tecniche, evidenze post Penetration Test o Adversary Simulation, ecc. Si identificano di base tre fasi:

- il trigger, ovvero ciò che "accende" il task e, come detto, può anche essere una semplice ipotesi formulata sulla base di un report esterno;
- la ricerca effettiva con la relativa raccolta di dati e le valutazioni per determinare se ciò che si sta osservando corrisponde ad una minaccia o meno;
- report/export dei risultati

Anche in questo caso l'output deve servire a produrre nuove logiche di detection o attività di hardening e configurazioni utili alla prevenzione della minaccia indagata.

## Due esempi da fare in lab

Per mettere le mani sui sistemi si potrebbero fare degli esercizi in laboratorio. Il primo caso si riferisce ad un task di hunting reattivo: il SIEM segnala che una workstation ha avviato una comunicazione con un IP sospetto. In questo caso possiamo eseguire i seguenti controlli:

- Analisi del traffico della workstation con raccolta del dump e verifica tramite IDS
- Identificazione dei processi che hanno generato la connessione sospetta
- Contenimento e "pulizia"

Nel secondo task possiamo considerare una casistica di hunting proattivo: suppiniamo di aver scoperto che un threat actor utilizza powershell per avviare payload malevoli e vogliamo verificare se questo sta accadendo nella nostra rete anche se non ci sono allarmi in merito. Questa ipotesi deve essere verificata con una serie di azioni:

- raccolta dei powershell log dalle workstation
- dai log possiamo verificare, tramite opportune ricerche, la presenza di specifiche azioni da parte del threat actor (l'utilizzo di sequenze di comandi, tools, ecc.)

## Tattiche di hunting e threat intelligence

Il threat hunting basato sulla threat intelligence è un metodo proattivo di analisi che va molto oltre le misure di sicurezza tradizionali. Il threat hunter utilizza le informazioni che possono essere condivide tramite report di threat int. da altri team per analizzare ed identificare eventuali gap nella capacità di detection o intercettare minacce sulla base di nuovi IoC e TTPs.

Per procedere con un'attività di hunting è quindi necessario disporre degli elementi di base come:

- IoC provenienti da feeds qualificati
- report che descrivono nuove metodologie di attacco o campagne specifiche
- analisi relative a tecniche e tattiche utilizzate dagli attaccati

Traduco con degli esempi concreti e reali nel contesto italiano:

- ACN o CSIRT potrebbe segnalare elenchi di IP che fanno capo a botnet o campagne di phishing
- un **Threat Int. provider**, un **Defense Team** o un'**analista indipendente** può segnalarci nuove campagne di attacco che utilizzano ClickFix per ingannare gli utenti (molto di moda in questo periodo ed è un'attività che ho svolto anche su questo blog).
- ad una conferenza possiamo apprendere come viene utilizzata una specifica tecnica e che tracce potrebbe lasciare sui sistemi (es: analisi del comportamento di un malware)

Ovviamente il contesto fa sempre la differenza (come ho spesso detto) e analizzare in dettagli le vulnerabilità che l'infrastruttura presenta è un elemento indispensabile per valutare quali debolezze potrebbero essere realisticamente sfruttate e con che tecniche.

Nota personale: nel mio archivio appunti metto spesso in relazione gli elementi che caratterizzano una vuln. con le azioni che posso eseguire per sfruttarle ed in che condizioni di detection posso restare "silenzioso". Parte di questi

Un altro elemento importante sono le "anomalie apparentemente innocue": variazioni e deviazioni dal normale funzionamento dei sistemi, configurazioni fuori dallo standard (ammesso che esista uno standard), carichi insoliti, traffico di rete insolito o osservato per la prima volta... ci sono decine di micro-comportamenti che possono celare tracce di una minaccia che si sta lentamente radicando nel sistema.

La Cyber Threat Intelligence (CTI) è una disciplina complessa quanto il Threat Hunting: vengono raccolte informazioni da molte fonti e queste devono essere raffinate in feeds strutturati che mettano a disposizione degli analisti artefatti sfruttabili ed indicatori validi.

Gli **artefatti** sono tracce o residui lasciata da un'attività malevola come log record, file, configurazioni. Non sono elementi malevoli di per se ma sono l'effetto collaterale del comportamento malevolo. Un **indicatore** è qualcosa che definirei più concreto nel senso che è un elemento che consente di tracciare l'azione malevola come l'IP da cui è partita una connessione anomala o la URL di un sito usato per attività di phishing.

Un elemento molto discusso è la "vita" dell'indicatore o dell'artefatto, ovvero la sua validità nel tempo. È ovvio che un IP address segnalato come indicatore di compromissione non può esserlo per sempre e determinare la validità nel tempo dell'indicatore è fondamentale per utilizzarlo nel processo di hunting come nel processo di detection.

Un approccio che definirei complementare si base sulle TTPs documentate su MITRE. Anche in questo caso si sono diversi modi di operare. Si può considerare il modus operandi di uno specifico threat actor, quali tecniche utilizza, che tools usa e cercare evidenze del "transito" dell'attaccante sapendo che elementi cercare in rete. Un altro modello può prendere in considerazione le TTPs più utilizzate da più threat actor in modo da allargare lo scope a più potenziali avversari.

Ogni approccio ha i suoi pro e i suoi contro e ovviamente le ipotesi di partenza possono guidare molto la scelta: se il task parte dalla consapevolezza di una specifica debolezza sfruttata da molti avversari è ovvio che conviene operare sulla base delle TTPs che più probabilmente possono essere utilizzate per abusare della falla che ho riscontrato.

Per procedere con il task di hunting si fa riferimento, solitamente, a questi step (in parte già discussi, ma torniamoci):

1. Studiare il comportamento di un'avversario e le sue TTPs
2. Formulare un'ipotesi (es: l'attaccante potrebbe utilizzare una tecnica di social engineering come ClickFix)
3. Determinare le sorgenti dei dati (es: nel caso di ClickFix vanno considerati i log di navigazione ed il comportamento degli endpoint, soprattutto in merito all'utilizzo di shell e script interpreter)
4. Generare visibilità aggiuntiva in caso i dati di cui al punto 3 non siano tutti disponibili (così si lavora anche sui punti ciechi, visto che vogliamo diventare fortissimi)
5. Ricerca delle informazioni rilevanti in relazione al threat che stiamo cercando
6. Validazione delle evidenze individuate per determinare se fanno effettivamente riferimento ad una minaccia
7. Approfondimento ed reiterazione della ricerca basandosi sui risultati del task svolto

## Identificare i GAP

Questo tema mi sta molto a cuore ed è stato l'argomento che ho portato ad una [recente conferenza](https://roccosicilia.com/conferenze/) in cui ho trattato in particolare di GAP di detection, ma non è l'unico GAP che potremmo dover gestire.

- **Impreparazione**: in riferimento alla consapevolezza degli utenti o alla preparazione tecnica degli addetti ai lavori.
- **Mancanza di monitoraggio**: spesso le soluzioni di controllo sono presenti ma mal gestite.
- **Gestione del perimetro**: in un periodo storico in cui non esiste un vero perimentro della rete aziendale.
- **Rischi derivanti da terze parti**: fornitori, vendor, soluzioni software.
- **Rischi legati alle persone**: dall'insider threat agli errori umani.
- **Infrastruttura ICT**: come viene gestita e manutenuta.

Ogni possibile GAP può essere analizzato al fine di definire una strategia di consenta di portare in controllo eventuali debolezze che possono emergere da attività di assessment come da un esercizio di hunting.

Ricordati che puoi sostenere il mio progetto di divulgazione per aiutarmi a proporre nuovi contenuti e nuovi progetti. Trovi tutte le info qui: <https://roccosicilia.com/divulgazione/>.

## Threat Hunting basato sulle anomalie

Forse l'approccio più "fine" e decisamente complesso è quello che si basa sulle anomalie, non allarmi, non indicatori specifici, semplici variazioni del normale funzionamento dei sistemi.

Ovviamente per tracciare un'anomalia è necessario aver ben documentato il comportamento "normale" del sistema, nella sua interezza. Se normalmente la mia rete genera 100 GB di traffico in download da internet ogni ora mi posso accorgere di un'anomalia nel carico della rete se osservo 200 GB in una fascia oraria in cui di solito ne osservo la metà. Devo poter comparare i dati che raccolto con il normale comportamento del sistema.

È, come sempre, indispensabile poter accedere alle informazioni sul comportamento del sistema in cui ho osservato l'anomalia. Per restare dell'esempio del carico di rete è indispensabile poter accedere ad eventuali sistemi di monitoraggio del traffico e del carico dei sistemi oltre che alle informazioni sulla struttura stessa della rete.

I dati a disposizione devo essere ovviamente analizzati per identificare ed isolare l'anomalia, determinare eventuali cause esterne o l'elemento scatenante e procedere con l'azioni di risposta e mitigazione se possibile.

## Conclusioni

Questi ultimi due blog post sono molto lunghi e si riferiscono ad una parte teorica molto importante del materiale di studio. Seguirà qualche post+video di laboratorio.

Iscriviti al blog per restare aggiornat*.