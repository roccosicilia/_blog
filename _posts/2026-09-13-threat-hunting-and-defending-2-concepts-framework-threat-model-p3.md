---
layout:     post
title:      "Threat Hunting and Defending #2: concepts, framework, Threat Model (p3)"
date:       2026-09-13 19:00:00 +0200
categories: [cyber-security]
image:
---

La pratica del Threat Hunting è di supporto alla soluzione di problemi complessi e l'analista deve prendere in considerazione una notevole quantità di informazioni attraverso tools differenti in contesti eterogenei. Tecnicamente parlando è una vera e propria *baraonda*. **Per dare una direzione alle attività sono stati sviluppati dei framework che possono aiutare a mettere ordine** e ad agire in modo strutturato.

## MITRE ATT&CK

Indubbiamente tra i più famosi c'è MITRE che ci ha aiutato a spostare l'attenzione su come è strutturata la minaccia per intercettare potenziali attacchi. Il modello prende infatti in considerazione il modus operandi dell'attaccate che è stato analizzato e scomposto in una "matrice", la famigerata [Enterprise Matrix](https://attack.mitre.org/matrices/enterprise/) dove sono raccolte le Tattiche, le Tecniche e le sotto-tecniche documentate.

<img src="{{ '/assets/images-posts/mitre-matrix.webp' | relative_url }}" alt="image 1" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Conoscere e comprende la struttura dell'Enterprise Matrix aiuta a comprendere anche l'evoluzione di un attacco e come questo si svolge nelle sue fasi intermedie. Per una figura come la mia che principalmente si occupa di sicurezza offensiva queste informazioni sono ben note, ma per chi lavora in contesti di difesa è diverso e si tratta di nozioni da studiare ed acquisire.

Il materiale relativo alla certificazione che sto studiando le illustra tutte quindi facciamo un bel ripassone :-)

**Reconnaissance**: l'attaccante raccoglie informazioni sul target usando sia strumenti passivi che azioni specifiche "contro" il target come scansioni del perimetro esterno o analisi dei dati raccolti da siti istituzionali.

**Resource Development**: è una fase di preparazione durante la quale il bad actor predispone gli strumenti per eseguire l'attacco, strumenti che possono essere predisposti o acquistati.

**Initial Access**: la tattica si riferisce alle diverse metodologie che possono essere messe in campo per guadagnare un primo accesso alla rete target.

**Execution**: la tattica si riferisce all'esecuzione di azioni sui sistemi target solitamente per ottenere obiettivi specifici come una escalation di privilegi o la raccolta di ulteriori informazioni.

**Persistence**: l'attaccante opera in modo di mantenere un accesso permanente all'infrastruttura target.

**Privilege Escalation**: solitamente il primo livello di accesso ha bassissimi privilegi, l'attaccante sviluppa quindi una serie di azioni finalizzate ad ottenere maggiori provilegi sui sistemi compiti.

**Defense Evasion**: le reti solitamente presentano diversi sistemi di difesa e detection che l'attaccante cerca di ingannare o disattivare.

**Credential Access**: se possibile l'attaccante cerca di ottenere ulteriori credenziali valide all'interno della rete per utilizzarle al fine di accedere a nuovi sistemi o con differenti privilegi.

**Discovery**: all'interno della rete l'attaccante cerca di comprendere come è strutturato l'ambiente con azioni di discovery di altri host o servizi.

**Lateral Movement**: si riferisce a tutte le tecniche usare per spostarsi all'interno della rete target passando da un sistema all'altro.

**Collection**: anche all'interno della rete è necessario raccogliere nuove informazioni per valutare e identificare i path sfruttabili per raggiungere i propri obiettivi.

**Command and Control**: tema di cui ho parlato moltissimo su questo blog e sul canale [YouTube](https://youtube.com/@roccosicilia) e riguarda le tecniche che possono essere messe in campo per governare un sistema compromesso da remoto.

{% include youtube.html id="ggZ5biRMH8k" title="Come funzionano i C2" %}

**Exfiltration**: si riferisce alla capacità del threat actor di portare fuori dalla rete informazioni.

**Impact**: questa fase fa riferimento alle tecniche che vengono utilizzare per "finalizzare" l'attacco con relative compromissioni a livello di integrità del sistema e/o dei dati.

Saper navigare il framework è estremamente utile per dare struttura alle attività dei threat actor e imparare a riconoscere i pattern ed i relativi tools che possono essere utilizzati.

La nomenclatura utilizzata da MITRE è una standard e fa da "lingua comune" nello scambio di informazioni. Ad esempio se stiamo indagando un'esecuzione di un comando powershell che ci ha insospettito o che ha insospettito uno dei sistri sistemi di detection possiamo analizzare il contesto ed attribuirgli un'intenzione. Qualche giorno fa spiegavo in un blog post su ClickFix come un comando Powershell può essere utilizzato come stage iniziale da parte di un Threat Actor per installare un C2.

Spesso la celeberrima "matrix" viene usata dai SOC Team solo per mappare l'azione del bad actor che si sta osservando, ma il livello di documentazione e correlazione va molto oltre. Ad esempio vengono messe in relazione TTPs e gruppi in modo da poter analizzare il comportamenti tipico di uno specifico bad actor.

<img src="{{ '/assets/images-posts/mitre-groups.webp' | relative_url }}" alt="image" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

La funzione è disponibile tramite il tool che mette a disposizione il "Navigator Layers" del gruppo che si sta analizzando ed è un comodo strumento visuale assieme all'elenco delle TTPs che viene riportato nella documentazione.

Dal punto di vista del Threat Hunter saper individuare un comportamento malevolo ha molto più valore rispetto ad individuare uno specifico IoC. Per fare un esempio pratico potremmo dire che è più interessante riconoscere un C2 grazie all'analisi del comportamento dell'host o del traffico rispetto a riconoscerlo grazie al fatto che l'IP del C2 server presenta una low-reputation. Ovviamente lavorare sul riconoscimento dei pattern consente di costruire regole di detection molto più efficaci rispetto alle regole che si basano sul riconoscimento di un IoC.

## Hunting Frameworks e metodologie

Esistono diverse metodologie di hunting che solitamente vengono utilizzate e la documentazione Cisco che prende in considerazione in particolare tre: TaHiTI, Cyber Kill Chain, OODA Loop, Diamond Model, Hunting Maturity Model.

### TaHiTI

Targeted Hunting Integrating Threat Intelligence è un processo che integra Threat Hunting e Threat Int. per ottenere un approccio orientato alla valutazione del rischio. Il processo è molto lineare ed è diviso in tre fasi.

Nella **prima fase** il team di Threat Hunting viene attivato da un elemento esterno che può avere differenti origini:

- un'informazione proveniente dalla threat intelligence (nuova minaccia, nuova CVE potenzialmente sfruttabile, ...)
- un'anomalia segnalata dal sistema di monitoraggio (SIEM, XDR, ...)
- analisi di terze parti o elementi emersi da attività di assessment (es: una configurazione debole potenzialmente sfruttabile da un bad actor)

Con le informazioni in proprio possesso il team definisce un abstract in merito al task di hunting in cui vengono documentati tutti i dettagli: data della sessione (necessaria per il riferimento ai dati che verranno utilizzati), ipotesi iniziale, elementi di partenza, priorità, ... tutte informazioni che devono essere gestite come gli elementi di un *case* o di un *ticket*. Questi elementi vanno a costituire una "coda" delle attività di hunting che, come detto in precedenza, sono da intendere come task pianificabili, non come incidenti.

Nella **seconda fase** il team lavora sui dati di analisi definendo e documentando dettagli rispetto a quando riportato nell'abstract. I dati vengono quindi arricchiti con nuovi elementi di contesto e viene definito uno *scope* di ricerca sulla base dell'ipotesi iniziale. Le ipotesi riportate nell'abstract devono essere quindi verificate per evitare di giungere a conclusioni errate.

In questa fase devono essere identificate tutte le fonti dati utili alla verifica delle ipotesi iniziali: dati di traffico, logs, telemetria, data analitici ed eventi di sicurezza. Tutti i dati raccolti devono essere salvati in una repository centralizzata per consentirne l'analisi strutturata anche grazie a tools di terze parti.

Vengono definiti quattro specifici task in questa fase:

- partendo dall'ipotesi iniziale l'abstract viene arricchito con riferimenti al framework MITRE ATT&CK, vengono identificati il potenziali bad actor e le motivazioni/obiettivi e vengono valutate risorse e tempi per eseguite il task
- viene strutturata un'ipotesi verificabile con gli strumenti a disposizione (inutile cercare elementi di attacchi basati su fileless malware se non abbiamo strumenti con telemetria sufficiente per questo tipo di minaccia)
- vengono definite le fonti dati per la ricerca in base allo scope identificato nell'ipotesi iniziale:
- vengono definite le tecniche di ricerca da applicare alle informazioni disponibile (es: se disponiamo di un SIEM sarà sicuramente possibile eseguire query estese per identificare elementi specifici), i dati vengono analizzati nel loro insieme utilizzando tecniche di clustering

L'analisi dei dati deve portare ad un verifica dell'ipotesi iniziale che può essere così provata (l'analisi conferma l'ipotesi), non confermata o inconclusiva (non ci sono abbastanza dati per provare o meno l'ipotesi iniziale).

La **terza** e conclusiva fase è relativa alla documentazione ed al report finale: tutto va dettagliato in un documento tecnico che descrivere cosa è stato fatto e che dati sono emersi per poi essere illustrato ai team interessati.

Il report è estremamente importante in quanto potrebbe interessare diversi team in modo diverso e con urgenze diverse:

- Se viene rilevato un **incidente di sicurezza non tracciato** va ingaggiato il team di Incident Response con urgenza
- Una ipotesi confermata può **produrre nuove detection rules** da segnalare al team di monitoraggio (SOC, MDR)
- Nuove tipologie di minacce possono arricchire la threat intelligence
- Nuove vulnerabilità identificate possono essere comunicate al team IT per avviare il processo di remetiation

### OODA loop

L'acronimo sta per Observe, Orient, Decide, Act ed è un modello di decision making ideato da uno stratega militare: John Boyd.

Il threat hunting, come esercizio/task, consente un'applicazione efficace del modello:

- Si parte da una ipotesi spesso legata ad osservazioni tecniche
- Si eseguono delle investigazioni con tools e tecniche specifiche
- Si identificano nuovi patters o TTP
- Si procede con un miglioramento della capacità di analisi e detection

Non esistono ovviamente vincoli specifici ma il modello descrive perfettamente il loop tipico dei task di hunting e può essere applicato anche a diverse attività di assessment orientate al miglioramento della capacità di detection.

### Hunting Maturity Model

Sul mondo dei "maturity model" sarebbe bello fare degli approfondimenti: sono convinto che siano molto utili per capire cosa un'organizzazione è effettivamente in grado di fare, in questo caso con focus la capacità di Hunting (personalmente ho molto approfondito i modelli che misurano la capacità di detection, ad esempio).

<img src="{{ '/assets/images-posts/hunting-maturity.webp' | relative_url }}" alt="image 2" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Il modello presenta 5 "voti" che esprimono uno stato sulla capacità di hunting in modo da ottenere una valutazione obiettiva sulle aree da migliorare per arrivare ad un processo di hunting funzionale.

## Conclusioni

Questa parte del corso è molto teorica ma serve ad affrontare con struttura i case study che stanno per arrivare. È evidente che non ci si può improvvisare Threat Hunter e c'è molta struttura e metodo in questa disciplina.

Con il prossimo argomento torno un po' in confort zone: Threat Modeling.hunting-matu