---
layout:     post
title:      "Threat Hunting and Defending #1: intro"
date:       2026-05-24 18:00:00 +0200
categories: [cyber-security, hacking, ita, study-with-me]
image:      /assets/images-posts/gemini-threat-hunting.png
---
### Premessa

Ricomincio a studiare per una nuova certificazione Cyber Security e quest'anno ho scelto "*Conducting Threat Hunting and Defending using Cisco Technologies for Cybersecurity*". Giustamente molti, già lo scorso anno, mi avevano scritto incuriositi da quella che poteva sembrare una deriva Defense (non che ci sia nulla di male), considerando che di "mestiere" io mi occupo della parte offensiva della sicurezza informatica. In realtà la risposta è molto semplice: il mondo dei SOC e dei servizi MDR si sta evolvendo molto (e molto ancora si deve evolvere) e buona parte dei miei task operativi è finalizzata alla verifica della capacità di detection di sistemi e Blue Team. Comprenderne a fondo metodologie e strumenti (il mio target attuale) è parte integrante, per come la vedo io, del mio percorso di crescita.

Alle dovute premesse aggiungo che vorrei condividervi i miei appunti di studio e come sempre utilizzerò i canali che ho a disposizione, in particolare questo Blog e [YouTube](https://youtube.com/@roccosicilia).

Se trovi utili i contenuti che condiviso e vuoi restare aggiornato puoi sostenere il mio progetto di divulgazione [iscrivendoti al mio Substack](https://roccosicilia.substack.com/subscribe). Per gli abbonati metto a disposizione articoli e video di approfondimento.

### Threat Hunting: la teoria

Come disciplina, il threat hunting, si applica soprattutto alle strutture di difesa come i Security Operations Center (SOC). Da questo tipo di struttura solitamente ci aspettiamo che siano in grado di rilevare, contenere e rimediare ad eventuali attacchi informatici contro la nostra struttura.

É giusto fare una precisazione - non presente nel corso - sui compiti dei SOC: sicuramente in Italia ma anche in molti paesi europei ho notato la tendenza a limitare la copertura del SOC ai compiti di detection e prima risposta di contenimento e tutto il resto sta al team del cliente. Questo modo di concepire il SOC personalmente non l'ho mai visto positivamente, ma a prescindere dal mio parere oggi è sicuramente limitato e poco efficace rispetto a strutture che garantiscono una gestione completa dell'incident fino ad arrivare, se le condizioni lo prevedono, all'attivazione di un team specialistico per operazioni complesse di responce (IT team). Nel corso in oggetto quando si parla di SOC si fa riferimento ad un servizio completo.

È evidente che un approccio come quello che ho riportato ha il limite della reattività: succede qualcosa, scatta un allarme, qualcuno analizza e decide se intervenire. Lineare ma già da qualche è chiaro che attendere passivamente che un qualche strumento generi un allarme è insufficiente. Il Threat Hunting è una disciplina che piò restituire efficacia ed efficienza alla struttura di difesa rendendole "proattive".

La tesi su cui si basa il Threat Hunting è che i sistemi e le automazioni di detection tendono ad una certa staticità ed è necessario condurre delle analisi anche in assenza di allarmi chiari. Inoltre, mi permetto di aggiungere rispetto al materiale del corso, andare a caccia di tecnico non note consente di arricchire le regole di detection dei sistemi.

### Il concept

Avendo recentemente parlato molto di "evasion" possono rimandare ad uno dei miei ultimi video per arricchire il concetto. Il modello di detection oggi in uso da molti SOC consente di intercettare la stragrande maggioranza dei threat (95% stima la documentazione Cisco). La domanda è quindi: cosa succede con il restante 5% dei threat in grado di aggirare la nostra capacità di detection?

Vi lascio uno dei video dove ho parlato di evasion:

https://www.youtube.com/watch?v=FfgfILE3zLg

Se il problema è andare a caccia di minacce che non siamo in grado di intercettare realtime una possibile soluzione è implementare un processo di "ricerca" di queste minacce nella base dati a nostra disposizione: stiamo quindi parlando di ***Threat Hunting***.

> Threat hunting is the security practice of looking for threats that evaded the security controls and are hiding within the environment.

Un documento interessante da leggersi è [TTP-Based Hunting](https://www.mitre.org/sites/default/files/2021-11/prs-19-3892-ttp-based-hunting.pdf) di MITRE che in un prossimo post vedrò di riassumere.

Un problema molto serio a cui i SOC devono far fronte è l'aumento dei tentativi di attacco combinato con una crescente complessità delle tecnologie in campo: il numero di segnalazioni ed allarmi aumenta come la quantità di falsi positivi da gestire. Inevitabilmente gli analisti rischiano di essere distratti da molti allarmi e talvolta di abbassa la "sensibilità" dei sistemi di detection per ridurre il numero di falsi positivi, ma così facendo si aumenta il rischio di non intercettare comportamenti malevoli.

Il threat hunting può aiutare il Blue Team ad intercettare azioni offensive, che non sono state viste dai sistemi di detection, prima che l'attaccante giunga all'obiettivo dell'operazione. Inoltre le attività di threat hunting (come anche l'output delle azioni di Red Teaming) possono aiutare il Blue Team ad individuare nuove politiche e regole di detection grazie all'individuazione di GAP o nuove minacce che non hanno generato segnalazioni.

Le principali aree in cui il threat hunter opera sono relative alle informazioni che possono essere raccolte dagli Endpoint e dalla rete. Uno degli strumenti che oggi non manca praticamente mai all'interno delle infrastrutture enterprise sono gli EDR, ottimo punto di partenza. È comunque utile e suggerito andare più a fondo tramite tools di analisi forense e strumenti di analisi specifici in base a quello che stiamo cercando ed il tipo di sistemi su cui stiamo operando. Anche in relazione alla verifica del traffico possono essere usati diversi strumenti, dagli immancabili firewall log (se il design della rete lo consente) alla cattura del traffico.

Centralizzare le informazioni che ci arrivano dagli EDR e dalla rete grazie alle sonde e le appliance (es: IDS o sistemi Firewall) non è facile e molti vendor implementano il concetto di XDR per mettere a disposizione uno strumento che consenta la massima visibilità e la massima capacità di risposta.

Anche Cisco ha una sua piattaforma [XDR](https://www.cisco.com/site/us/en/products/security/xdr/index.html) che differisce a livello di struttura rispetto a come molti altri vendor hanno implementato il concetto. Non voglio in questa sede fare paragoni, non è lo scopo dei miei studi ne di questi post, va messa in evidenza una sostanziale differenza sull'interpretazione del concetto: Cisco ha preferito creare una piattaforma di aggregazione di sistemi terze parti compresi altri EDR, Firewall, logs, ecc.  
Questa configurazione non è impossibile con altri vendor ma va considerato che solitamente gli XDR di mercato estendono le capacità della piattaforma EDR accettando ed integrando diverse fonti.  
Si tratta di una differenza di Design che fa valutata prima dell'implementazione di questo tipo di soluzioni.

Il Threat Hunter deve quindi poter accedere a strumenti che gli consentano di analizzare il dettaglio di ciò che sta avvenendo sui sistemi e nella rete in modo da poter cercare tracce di specifici pattern di attacco o elementi che possono indicare tentativi di compromissione.

Ciò che può sembrare paradossale è che non sempre si cerca qualcosa di preciso: l'analista potrebbe avere a disposizione gli elementi per cercare una specifica minaccia di cui conosce i tratti caratteristici (known/known), potrebbe avere un'idea di cosa cercare pur non avendo elementi certi per individuare la minaccia (known/unknown) o potrebbe andare a caccia di qualcosa che non conosce e di cui non ha nessun dato preciso (unknown/unknown). Ovviamente l'obiattivo del processo è portare le analisi allo stato di known/known: una volta che abbiamo compreso la minaccia e la sappiano riconoscere potremo creare le regole di detection opportune o implementare contromisure efficaci.

### Tipologie di hunting

Alla base di tutti i nostri ragionamenti di sicurezza informatica c'è una consapevolezza che negli anni è diventata quasi un meme: è praticamente certo che qualsiasi azienda ha in qualche misura subito un attacco che potrebbe anche essere stato intercettato sul nascere dai nostri sistemi di perimetro e non aver generato nessun tipo di allarme.

Quando parlo con le aziende di gestione degli incidenti in caso di grave compromissione spesso scopro che il management non ha idea di quanti ***case*** il SOC gestisce quotidianamente senza farli diventare degli incidenti.

Fare hunting diventa quindi una necessità e deve diventare parte integrante dei servizi SOC. È giusto dirlo anche se potrebbe non far piacere leggerlo: lo fanno in pochissimi, veramente pochi. Gran parte dei SOC (nel 2026) si limita ad attività puramente passive e talvolta anche quelle non sono fatte benissimo (altrimenti i miei security test andrebbe molto diversamente). Ci sono tre principali approcci (sempre secondo il materiale Cisco) all'hunting: non strutturato, strutturato e guidato dalla situazione.

##### Threat Hunting non strutturato

Con questa modalità di lavoro si fa riferimento ad attività eseguire a seguito di una sospetta compromissione non tracciata dai sistemi di detection. La ricerca può essere attivata da fattori esterni come la pubblicazione di informazioni sulla nostra organizzazione o utenti che segnalano email sospette. In questi casi il Security Team può avviare quella che è a tutti gli effetti un'indagine per approfondire eventuali threat sulla base delle informazioni a disposizione.

##### Threat hunting strutturato

Un team qualificato e ben organizzato ha modo di pianificare azioni di hunting non basate sull'occorrenza di fattori esterni ma aulla base di indicatori di rischio. Il team di Threat Hunting può eseguire verifiche sulla base di TTP noti o novità sul fronte dei threat actor e delle loro azioni *operations*.

Esempio: se da un Threat Intelligence feeds veniamo a conoscenza di una nuova campagna di phishing in cui si fa uso di uno specifico fake CAPTHA, possiamo verificare se sui nostri sistemi ci sono eventi che fanno riferimento alla nuova minaccia di cui siamo stati informati. Questo tipo di attività devono essere bel strutturate e pianificate in modo da avere gli analisti all'opera periodicamente su task di ricerca specifici.

##### Threat Hunting contestuale

Questa modalità segue eventuali situazioni o eventi nel contesto di analisi. Si capisce molto meglio con un esempio. In passato, a seguito di attività di Penetration Testing e Red Teaming, mi è capitato di segnalare con urgenza sistemi esposti con gravi vulnerabilità e solitamente suggerivo, oltre al fixing, anche di controllare se la vulnerabilità era già stata sfruttata ed eventualmente accertarsi delle capacità di protezione e detection. In queste occasioni si scoprono sempre cose interessanti: molte volte il team a cui facevo la segnalazione trovata diversi tentativi di exploiting fortunatamente bloccati dall'IPS del firewall di perimetro, ma nessuna segnalazione lato SOC.

Questo tipo di attività deve comunque portare al miglioramento della capacità difensiva oltre che alla correzione di eventuali falle.

### Threat Detection "convenzionale" e Threat Hunting

Solitamente, come accennato, la detection tradizionale si basa sull'individuazione di minacce note: se si conosce un metodo di attacco o se ne conosco alcune caratteristiche si può creare una regola di detection per il caso specifico. Abbiamo strumenti eccezionali per questo tipo di attività come gli EDR, gli XDR ed i SIEM.

Il limite di questo approccio è relativo alla gestione delle minacce non note e le minacce che per qualche ragione non abbiamo ancora preso in considerazione. Va inoltre ricordato - questo lo aggiungo io, non c'è nel materiale del corso - che gli strumenti di detection possono presentare dei difetti o delle debolezze che l'attaccante utilizza per non essere rilevato.

Il threat hunting consente una maggiore flessibilità e non dipende dalla quantità di regole che abbiamo creato per una detection. Si tratta di attività pianificate di ricerca in cui gli analisti possono formulare un'ipotesi o partire da una situazione sospetta per avviare la ricerca di elementi che possono essere associati ad una minaccia. L'ipotesi può quindi partire da un dato analitico, da una specifica situazione, da dati di intelligence o semplicemente sulla base dell'esperienza dell'analista. Lo scopo dell'attività resta quello di individuare qualcosa che è sfuggito alla detection e creare nuovi controlli per coprire eventuali GAP di visibilità e/o detection.

### Tempo di permanenza

Un tema importante su cui porre l'accento sono gli Advanced Persistent Threats (APTs), definizione con cui ci riferiamo agli attaccanti che piantano le tende all'interno di una rete target e riescono a restare all'interno per molto tempo senza farsi intercettare. In questi casi l'obiettivo è ovviamente rubare informazioni in transito o archiviate, azione che richiedere tempo.

Ovviamente se un attaccante è riuscito a compromettere un sistema, installarsi all'interno della rete ed avviare una comunicazione stabile verso l'esterno è abbastanza ovvio che sta sfruttando una debolezza della capacità di detection dei sistemi usati o un punto cieco della difesa. In questi contesti è particolarmente utile ricorrere a task di hunting strutturati e pianificati che potrebbero intercettare un'anomalia che non verrebbe mai rilevata da una tecnologia che opera su principi "reattivi". Il principio di base è quindi usare il threat hunting per ridurre il tempo di persistenza di un threat actor nella rete target.

#### Esempio: Network Threat Hunting

Molti threat actor usano infrastrutture C2 per impartire comandi ai sistemi target o per esfiltrare informazioni (ho fatto diversi esempi in questo blog [che trovare qui](https://roccosicilia.com/?s=C2)). Inevitabilmente la comunicazione tra la macchina target ed il C2 deve transitare dalla rete della vittima ed il traffico è sicuramente visibile, in qualche forma, ai sistemi Firewall ed IDS. Un comportamento molto frequente è la presenza di chiamate ripetitive dalla macchina target verso il sistema C2, un dialogo costante fatto di diverse richieste ad intervalli regolari a cui ci si riferisce con il termine di Beaconing.

Se il malware utilizzato genera connessioni identiche ad intervalli regolari verso lo stesso IP/dominio è possibile individuare con relativa semplicità questi eventi ed indagare di cosa si tratte. Ci sono diversi tools per eseguire questo tipo di analisi e nel contesto del materiale di studio viene preso in esame AC Hunter from Active Countermeasures e Cisco Secure Network Analytics (ex Stealthwatch).

Su questo esempio di Hunting nel mio lab possiamo ricreare le condizioni ed analizzare il traffico di un semplice C2. Questo test lo preparerò tra qualche giorno con un approfondimento sul tema. Segui il mio [canale YouTube](https://youtube.com/@roccosicilia) ed in particolare la playlist **Cyber security in lab**.

### Quando avviare un task di Hunting?

È chiaro che le attività di Hunting non posso partire da un allarme altrimenti torneremmo nel contesto "reattivo" che stiamo cercando di migliorare. Quindi in base a cosa dovremmo avviare un'attività di Hunting?

Si individuano quattro principali trigget:

- la presenza di anomalie non necessariamente tracciate da allarmi come aumenti del consumo di banda o delle sessioni, carichi anomali sui sistemi, change non coerenti con le politiche interne, ecc.
- situazioni derivanti da cambi di contesto come una riorganizzazione che porta molti dipendenti a lavorare da remoto o l'acquisizione di un'azienda che porta le due reti a comunicare tra loro.
- informazioni provenienti da fonti di Cyber Threat Intelligence
- esperienze pregresse come altre attività di hunting o nuove ipotesi formulate a seguito di assessment o security test

È importante ricordare l'obiettivo di questa pratica: stiamo cercando minacce che non conosciamo e che i nostri sistemi di detections potrebbero non rilevare.

### Tools

Ovviamente dobbiamo farci supportare da metodologie e tools specifici in questa pratica. Nelle prossime sessioni del corso verranno tutti approfonditi quindi in questo paragrafo ci limitiamo ad alencarli:

- Frameworks e Threat Model sono la nostra guida teorica per orientare valutazioni ed attività, in cima alla lista c'è sicuramente MITRE ATT&CK ma è opportuno citare anche Targeted Hunting Integrating Threat Intelligence (TaHiTI), Process for Attack Simulation and Threat Analysis (PASTA).
- Telemetria strutturata in arrivo da NDR/EDR.
- Strumenti per accentrare le informazioni come SIEM ed XDR.
- Tools specifici e verticali per analizzare i dati, da Wireshark a CyberChef ce ne sono decine.
- Fonti di Threat Intelligence
- Strumenti di automazione

### Prossimo step

In questo post ho riassunto i miei appunti in relazione al capitolo "Threat Hunting Theory" del corso che sto seguendo. Nel prossimo capitolo si affronta un'altra parte molto teorica in relazione a Framework e Threat Model, ma prima di dedicarmi a questo capitolo preparerò un paio di approfondimenti sui temi discussi con particolare riferimento ai tools citati.

### Note conclusive

Solo per ricordare che il mio interesse verso la materia nasce in parte dalla volontà di comprendere meglio possibilità e limiti dei sistemi di detection. Sia nella mia attività di [studio e ricerca personale](https://roccosicilia.com/divulgazione/) che in [ambito professionale](https://nts.eu/?utm_source=roccosicilia) il fine ultimo è il miglioramento della capacità di difesa di sistemi e reti.
