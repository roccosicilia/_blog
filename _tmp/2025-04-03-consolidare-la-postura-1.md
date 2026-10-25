---
layout:     post
title:      "Consolidare la postura (1)"
date:       2025-04-03 12:00:00 +0200
categories: [cyber-security, ita]
image:      /assets/images-posts/in-questo-post-parlo-di-threat-intelligence-e-threat-hunting.png
---
## Intro

Ho in mente alcuni temi che, per diversi motivi, stanno convergendo. Di alcuni ne parlo da parecchio e mi sono guadagnato un sacco di sguardi perplessi quando proponevo percorsi che andavano verso la Threat Intelligence, il Threat Hunting, la verifica costante della superficie attaccabile... oggi molte aziende che non hanno avviato questo processi sono considerate "in ritardo"... i misteri del mondo info sec.

Mi piacerebbe aver sufficiente proprietà di linguaggio per parlarne in un unico lungo video, ma devo optare per un metodo più strutturato: scrivo, organizzo le idee e poi faccio anche dei video di sintesi.

Questa mini-serie è dedicata al consolidamento: ormai le scelte tecnologiche, più o meno giuste, sono state fatte e quello che (IMHO) va fatto è capire come queste scelte stanno cooperando per migliorare la capacità di gestione delle minacce informatiche. Quindi la questione che pongo in questa riflessione è: **abbiamo scelto tecnologie sulla base di processi che ora possiamo integrare ed automatizzare?** Se, come spesso osservo, abbiamo scelto bellissime tecnologie senza pensare al processo di gestione ed integrazione probabilmente abbiamo un bel problema che solitamente si traduce in investimenti inefficienti se non inefficaci. Tradotto: abbiamo speso 100 in "prodotti cyber" e la nostra postura è migliorata di 30. Perché?

## Parto dalla fine

Introduco il tema partendo da un recente episodio (spoiler: tutto quello che scriverò viene da episodi recenti, altro elemento su cui ragionare). Qualche giorno fa, il 28 marzo, sono stato ospite ad un evento - vi lascio i link a fine post - in cui ho parlato di Threat Hunting, tema che solitamente si approccia quando si sono già implementate un po' di cose.

Per chi non conosce questa pratica, il Threat Hunting è un processo che consente di andare letteralmente a caccia di "prove" di una passata compromissione o tentativi di compromissione. Facciamo il solito esempio: se vengo a conoscenza del fatto che un certo Threat Actor (TA) utilizzava, per le proprie attività, una botnet di cui si sono scoperti gli indirizzi IP degli hosts, posso verificare nei log del traffico del mio firewall se in passato ho osservato traffico da o verso uno di questi IP. Se trovo tracce di attività da parte del TA allora potrebbe valer la pena di indagare per verificare se vi sia stata compromissione, se non trovo nulla va bene così.

Questo processo è necessario per diversi motivi:

- non tutte la azioni dei TA sono immediatamente identificabili come malevole dagli strumenti di detection
- cercare indicatori di compromissione (IoC) consente di intercettare minacce particolarmente "silenziose"
- disporre di IoC esterni consente di creare regole di detection efficaci basate su dati oggettivi come specifici elementi o comportamenti adottati dai TA
- comprendere le tattiche e tecniche di attacco consente di migliorare le regole di detection

È un processo che richiede una certa struttura: solitamente questo tipo di attività viene eseguita grazie al fatto di disporre di uno storico degli eventi registrati da EDR/XDR, logs raccolti dai sistemi server, logs del traffico di rete ed eventi significativi da qualsiasi sistema della rete e software di detection.

Durante il talk ho fatto cenno al fatto che quello appena descritto è un punto di arrivo di per se già molto strutturato: collezionare tutti gli eventi significativi significa disporre delle tecnologie per registrarli e disporre di un sistema in grado di raccogliere i dati in modo strutturato (un SIEM ad esempio). Il SIEM non è uno strumento che non tutti possono permettersi di gestire in casa e spesso manca, ma EDR (visibilità a livello endpoint) e firewall (visibilità a livello rete) sono oggi gli strumenti di base che più o meno tutti hanno, al netto delle tecnologie più o meno prestanti.

Quello che spesso manca è una profonda conoscenza delle piattaforme adottato e di conseguenza è molto difficile operare una gestione continuativa e strutturata: abbiamo gli EDR ma ci accontentiamo di quello che sono in grado di fare con la configurazione iniziale per poi scoprire (lo vedo continuamente durante i security test che eseguo) che il sistema è configurato in modo da poter gestire solo un set relativamente ridotto di scenari generici di compromissione e la configurazione non è coerente con le peculiarità dell'organizzazione che devono proteggere. Inoltre attività di gestione come il tuning delle configurazioni e l'arricchimento della base IoC sono spesso completamente abbandonate.

Qui abbiamo il paradosso: tecnologia potenzialmente molto prestante dal punto di vista della detection e della gestione di una minaccia, ma assolutamente sotto-utilizzata sia per il potenziale di detection che per quanto riguarda le attività di miglioramento continuo e ricerca attiva di potenziali situazioni critiche all'interno della rete. Il risultato è una postura su carta anche buona, ma se messa sotto attacco (simulato) emergono le debolezze.

## Il fatto è che...

... i concetti che stanno alla base del Threat Hunting non sono nuovi. Se scaviamo nella letteratura di settore troviamo articoli ben strutturati che mettono le basi della disciplina già dal 2014 (vi lascio [questo link](https://ryanstillions.blogspot.com/2014/04/the-dml-model_21.html) di esempio), si è iniziato a parlare in modo strutturato di Threat Hunting qualche anno dopo. Dal mio punto di vista se una pratica considerata estremamente utile è ancora qualcosa che fanno in pochissimi (ricordo che il mio punto di osservazione si limita al sud e centro Europa) anche tra gli addetti ai lavori, è segno che qualcosa non sta funzionando.

Ovviamente non è il Threat Hunting che ci salverà da tutte le minacce che dovremo affrontare, ma in un certo senso è qualcosa che chiude il cerchio: il nostro modello di gestione delle minacce ci porta ad essere in un costante stato di attesa in cui aspettiamo che qualcosa di nuovo ci si presenti per poi analizzarlo e capire come intercettarlo/bloccarlo/eliminarlo. Considerando che gli attacchi informatici seguono determinate fasi, disporre di uno strumento che ci consenta di cercare elementi o indizi collegabili ad azioni offensive rappresenta un vantaggio strategico: avremmo modi di intercettare attacchi nelle fasi preliminari, prima che la minaccia si concretizzi con degli impatti.

L’infrastruttura tecnologica è già nostra disposizione, quello che manca sono le informazioni (che arrivano dal mondo della Threat Intelligence) da utilizzare in un processo di ricerca che richiede skills elevate. Ed è qui che ci si arena: gli strumenti - EDR, XDR, SIEM, ... - sono abilitanti per questo tipo di processo, ma le attività vanno gestite da un analista. Sicuramente si può automatizzare buona parte del processo ed è possibile essere supportati da tecnologie come gli LLM, ma **permane la necessità di governare un processo che richiede uno sforzo intellettivo**, sforzo che probabilmente si spingerà sempre più verso un supervisione di un processo sempre più automatizzabile.

Una volta che abbiamo compreso gli obiettivi, abbiamo acquisito le skills e abbiamo definito il processo, possiamo parlare di strumenti, automazione, intelligenza artificiale e tutto quello che vi pare. **Quindi, per l'ennesima volta, smettiamo di pensare che il *prodotto* sostituisca il *processo*, non ha mai funzionato così e sono sempre serviti entrambi.**

## È un percorso

Non si fa tutto in un giorno e nemmeno in una settimana. Come ho accennato il Threat Hunting è più un punto di arrivo, è un processo che viene abilitato da strumenti, competenze e altri processi di controllo.

Sarebbe bello partire da un greenfield per avviare questo percorso ma nella maggior parte dei casi tutte le organizzazioni hanno qualcosa di attivo e in parte strutturato. Bisogna partire da una mappatura degli strumenti che si hanno, dalle relazioni tra questi strumenti (spesso inesistenti al T0) e dai processi che abbiamo già implementato.

Dal prossimo post inizierò ad ipotizzare un possibile percorso chiamando in causa le diverse tecnologie e le attività da implementare per utilizzarle al meglio.

## Note conclusive

Ho sfruttato la scusa della mia presenza alla conferenza per partire dal tema del Threat Hunting, ma il discorso è molto più articolato e seguiranno altri post.

Qui vi lascio il link alla pagina della conferenza di cui dovrebbero uscire dei contenuti: <https://lp.t-consulting.it/iscrizione-t-con-2025>.

Qui vi lascio il link al video in cui racconto come mi preparo a questo tipo di conferenze: <https://www.patreon.com/posts/preparare-un-125652311>
