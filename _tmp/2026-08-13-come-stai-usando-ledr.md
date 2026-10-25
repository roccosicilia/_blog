---
layout:     post
title:      "Come stai usando l'EDR?"
date:       2026-08-13 09:00:00 +0200
categories: [cyber-security, hacking, ita]
image:
---
### Introduzione

Sul mondo degli EDR bisogna fare un po' di premesse e visto che gli interlocutori principali di questa serie sono persone che lavorano per lo più all'interno di un team IT, non necessariamente con competenze verticali sulla sicurezza informatica, creso sia saggio partire da come questi strumenti sono stati proposti.

Dobbiamo fare un salto indietro di qualche anno, all'inizio dello scorso decennio quando il Dr. Anton Chuvakin per primo ha parlato di EDR: Endpoint Detection and Response. In quegli anni i sistemi antimalware stavano evolvendo rapidamente: ci si era resi conto che lavorare unicamente sulle firme dei malware o sul comportamento di un programma, analizzabile real-time o in una sandbox, era insufficiente ed estremamente limitante. Il concetto di malware stesso stava mutando ed ere necessaria introdurre una visione più ampia che doveva comprendere varie tipologie di minaccia (threat).

La risposta dei *vendor* fu l'introduzione di architetture in grado di raccogliere dati dall'endpoint e delegare all'agente locale solo quella parte dell'analisi che poteva essere eseguita localmente senza impatto sulle prestazione dell'host, mentre i dati raccolti dai sensori venivano invece inviati al backend della soluzione dove potevano essere analizzati in dettaglio grazie a regole di correlazione ed indicatori gestiti in modo centralizzato. Con il termine EDR il Dr. Chuvakin "battezzava" questo modello introdotto in quegli anni da alcune soluzioni già in commercio.

---

Se trovi utili i contenuti che condivido e vuoi aiutarmi a migliorare il mio progetto di divulgazione iscriviti e abbonati al blog:

---

Il passaggio da "anti-malware tradizionale" ad EDR è indubbiamente stato qualcosa di innovativo e si stavano affrontando e risolvendo problemi reali. Lo *storytelling* di alcuni vendor, o meglio di alcuni soggetti commerciali, ha generato un po' di confusione e in alcuni caso sono state raccontate delle vere castronerie.

Per un periodo non brevissimo c'è chi ha raccontato che gli EDR erano la soluzione definitiva chiavi in mano, sarebbe bastato attivare il *tenant* ed installare gli agent ed il problema delle minacce cyber sarebbe stato risolto per sempre. Vorrei che queste mie parole fossero solo un'esagerazione assurda, ma la realtà in alcuni ambiti è stata effettivamente questa. C'è voluto un po' per capire che gli EDR erano e sono soluzioni complesse, che richiedono configurazione e gestione, che vanno presidiati e che non sono infallibili. Oggi parliamo di questo.

### Cosa significa usare un EDR

In questa serie mi rivolgo al mondo IT in generale, non necessariamente agli addetti ai lavori per i quali scrivo articoli di approfondimento e che in buona parte sanno bene cosa significa usare un EDR (spero). Probabilmente è bene prima fare un piccolo focus sull'architettura dei moderni EDR per avere una base comune da cui partire.

Possiamo rappresentare l'EDR come una soluzione con diverse componenti:

- l'agente
- i sensori
- la logica di detection
- la dashboard

<img src="{{ '/assets/images-posts/image.png' | relative_url }}" alt="image" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

L'agente è la componente software che viene installata sull'endpoint e solitamente integra/incorpora i sensori. Mentre i sensori di occupano di raccogliere i dati dall'endpoint in base alla loro funzione (logs, stato dei processi, syscall, ...) l'agent di occupa di eseguire alcune analisi locali ed inviare tutta la telemetria raccolta ad un sistema centralizzato (che oggi è praticamente un SIEM).

Qui le informazioni vengono archiviate, arricchite ed analizzate per individuare, tramite delle specifiche logiche di correlazione, possibili attività sospette o threat riconosciuti dal sistema. Il tutto viene presentato all'utente tramite comode dashboard consultabili via web.

Ora, se vestite i panni del membro del team IT e vi hanno detto che questo aggeggio funziona da solo e senza la vostra supervisione/interazione, devo tristemente informarvi che vi hanno detto una cavolata. A meno che assieme al prodotto non sia presente anche un servizio di gestione della baracca (e anche su questo in futuro ne parliamo) questo aggeggio meraviglioso lasciato a se è inefficace e con il tempo diventerà completamente inutile. Intendiamoci, ci sono molti automatismi che si possono impostare per agevolare il lavoro, ma ci sono diversi task che vanno portati a termine da chi gestisce lo strumento:

Le attività minime, post-startup, sono:

- Controllo della dashboard / triage degli alert
- Tuning delle detection
- Aggiornamento di agent, sensori e componenti
- Aggiornamento delle policy di prevenzione e risposta
- Threat hunting
- Revisione delle detection
- Verifica della copertura degli endpoint
- Verifica della telemetria
- Test delle capacità di detection e response
- Gestione degli incidenti
- Revisione dei privilegi e della configurazione
- Integrazione con il resto dell'ecosistema
- Metriche e reporting

Sono un bel po' di ***cose da fare*** ed in questa occasione ne consideriamo alcune per iniziare ad entrare nella logica di utilizzo dello strumento potentissimo che avete acquistato.

### Controllo della dashboard e triage degli alert

Partiamo dalla cosa più logica ed in assoluto meno gestita: il presidio degli allarmi. Lo strumento di base vi da due tipi principali di output che vi traduco in linguaggio parlato:

- "ho visto qualcosa di sospetto, controlla cosa sta succedendo sull'host ***"
- "ho intercettato una minaccia sull'host ***"

Nel secondo caso è anche possibile impostare una risposta automatica che esegua delle azioni, in particolare le minacce riconosciute come tali possono essere bloccate ed il sistema colpito può essere isolato.

Va però chiarito un dettaglio: le minacce moderne sono abbastanza complesse e la detection non avviene sempre real-time, anzi molto spesso l'agent raccoglie i dati dall'host con le relative "azioni" compiute dalla minaccia, i dati vengono quindi analizzati e dopo poco, solitamente da alcuni secondo ad alcuni minuti, nella console dell'EDR appare il verdetto.

Questo significa che quando il problema è stato notificato potrebbero essere già passati alcuni minuti durante i quali la minaccia si è potenzialmente data da fare. L'EDR può bloccare ulteriori azioni ed isolare il sistema per contenere un'eventuale attacco, ma siete voi che dovete poi andare ad indagare, capire che cosa è successo, mitigare ed eradicare la minaccia individuata.

Ovviamente se non siete strutturati per fare in modo che qualcuno controlli costantemente la console (non la mattina appena arrivati in ufficio e poi ci si rivede domani) c'è potenzialmente un bel problema: l'EDR tenterà di fare il suo lavoro segnalando anomalie ma non ha potere di agire in autonomia su tutte le casistiche e non può approfondire in autonomia situazioni complesse. Gli allarmi continueranno, si accumuleranno fino a quando uno di quegli allarmi sarà qualcosa di veramente serio e bisognerà affrontare un incidente di sicurezza informatica.

### Aggiornamento delle policy di prevenzione e risposta

Come detto una delle funzionalità interessanti è il fatto di poter definire delle azioni in risposta ad una minaccia e con questi strumenti si possono fare cose molto più articolate del semplice "bloccare la minaccia riconosciuta". Innanzi tutto il principio è quello del "sospetto", ovvero il sistema EDR, tramite le regole di detection, può segnalarci un'anomalia senza avere la certezza che si tratti di una specifica minaccia ma semplicemente riconoscendo un pattern di eventi che potrebbe essere associato ad azioni malevole.

Quando viene implementata una soluzione EDR inevitabilmente ci saranno molte segnalazioni che il team IT riconoscerà come un'attività lecita fatta da uno specifico software o sistemi nella rete ed è abbastanza normale che attività lecite vengano segnalate come sospette: l'EDR ha semplicemente notato un comportamento che presenta caratteristiche simili al comportamento di una minaccia nota e quindi lo segnala. Se attivassimo una prevenzione automatica per tutti i comportamenti sospetti nel giro di pochi minuti ci troveremmo con decine di lamentele di utenti che riscontrano malfunzionamenti di vario tipo.

Le politiche di prevenzione e di risposta vanno quindi definite sulla base del funzionamento del sistema IT nel suo complesso, andando a caccia di quei comportamenti sospetti ma indagati e classificati come leciti in modo da non far intervenire l'EDR e nel contempo facendolo intervenire in tutti gli altri casi.

È un lavoro di continuo adattamento che non ha una reale fine: se può essere plausibile un momento in cui abbiamo gestito tutte le eccezioni note dobbiamo sempre considerare che l'infrastruttura IT non è qualcosa di statico e ad ogni cambiamento/evoluzione corrisponderanno nuovi adattamenti dell'EDR.

Anche questo task non si esegue da solo come per magia, serve qualcuno che analizzi gli eventi e decida come aggiornare le configurazioni.

### Test delle capacità di detection e response

Chiudo con un tema che mi sta molto a cuore: per essere sicuri che un sistema stia funzionando, soprattutto se è un sistema complesso, **bisogna metterlo alla prova**. Ci sono diversi modi per farlo: simulazioni di attacco, test automatizzati, esercizi in stile cyber range, attività di red teaming, ... Ogni metodologia ha i suoi punti di forza ed i suoi limiti e a mio parere è bene prendere in considerazione più metodologie nel tempo.

L'automazione consente di eseguire un gran numero di test in modo tempo ma tende a peccare il realismo. Al contrario le attività strutturate come le simulazioni di attacco e le azioni di un Red Team devono considerare un numero relativamente contenuto di azioni ma restituiscono un alto livello di realismo.

Se applichiamo il tutto al tema di questo post possiamo sicuramente dire che i team IT possono adoperarsi in autonomia per automatizzare dei test mentre è molto più probabile che debbano chiedere a team esterni le attività più realistiche. Esistono eccezioni: conosco diversi istituti di credito che hanno un red team interno, ma questo non è certo lo standard.

### "Ma devo fare tutto io a mano?"

Ma nemmeno per idea! :-)

Moltissimi task possono essere gestiti introducendo automazione per evitare attività ripetitive e molti strumenti hanno migliorato l'interazione con la dashboard. Le integrazioni con gli LLM hanno permesso di semplificare, in alcuni casi, il task. L'unica baggianata a cui non dovete credere e che lo strumento faccia tutto da solo.

Oppure si delega: strumento + servizio e qualcuno eseguirà controllo e gestione per contro vostro. Ovviamente il servizio è qualcosa che si aggiunge allo strumento, quindi si paga. Diversi vendor hanno integrato nella solo offerta la parte di servizio, solitamente come MDR, oppure ci si può rivolgere ad un provider che lo fa di mestiere. Ad esempio io lavoro in un'azienda che eroga un [servizio di Threat Detection](https://www.nts.eu/it/news/nts-threat-detection-service-siem/?utm_source=roccosicilia) (SOC) basato su uno stack tecnologico specifico.

Questo articolo è la versione testuale del video pubblicato sul canale [YouTube](https://youtube.com/@roccosicilia) per la serie "Appunti per il team IT".
