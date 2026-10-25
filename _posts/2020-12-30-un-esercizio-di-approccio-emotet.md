---
layout:     post
title:      "Un esercizio di approccio: Emotet."
date:       2020-12-30 09:00:00 +0100
categories: [cyber-security]
image:
---

Approfitto di un caso arcinoto un po’ fuori dalle cronache (che non amo particolarmente) per ragionare sulla necessità di approcciare la sicurezza informatica in modo integrato valutando le strategie possibili e la necessità di far evolvere le nostre organizzazioni dotandole di una corretta postura di difesa.

Non possiamo prevedere tutto né possiamo pensare di dotare le nostre infrastrutture di tutte le possibili soluzioni di protezione che il mercato offre: sarebbe costosissimo e talvolta inefficace. In tal senso torna utile l’esempio di Emotet che nelle sue recenti varianti presenta un’archivio protetto da password.

> Nota tecnica su Emotet  
> La campagna recentemente si è evoluta diffondendo a mezzo email archivi in formato .zip protetti con una password consegnata con lo stesso messaggio. La variazione introdotta consente ai messaggi di posta di transitare indisturbati attraverso i sistemi di protezione a perimetro delle reti (anti-spam, firewall ed affini) che non hanno la possibilità tecnica di eseguire una verifica del contenuto dell’archivio.

Ancora una volta la furbizia dell’attacker ha consentito di aggirare la protezione offerta dalla mera (ed indispensabile) tecnologia, la storia si ripete. La tecnologia è uno strumento al servizio di una strategia, se non c’è una strategia la tecnologia non sarà sufficiente a garantire livelli adeguati di sicurezza.

Proviamo quindi a ragionare su quale potrebbe essere una corretta postura per la nostra organizzazione e sul possibile approccio al problema. In primo luogo va compreso il problema stesso che un non addetto ai lavori potrebbe scambiare facilmente con l’incident, ovvero con l’evento che il problema ha generato.

Nel caso specifico l’incident, si spera sventato, è identificato del fatto che gli utenti si vedono recapitati dei messaggi di posta apparentemente puliti, con un mittente solitamente noto, un allegato .zip ed una password per estrarre l’archivio. Il contenuto dell’archivio, una volta recuperato, porta sull’endpoint un malware pronto ad essere eseguito. Come detto la natura stessa di questa campagna consente ai messaggi di essere recapitati beffandosi dei sistemi di protezione a perimetro.

Da quando ho memoria i malware si diffondono tramite le email (qualcuno si ricorderà anche i floppy disk, ma è un’altra storia) con un allegato. Il problema che identifico, secondo la mia esperienza, sta nella gestione dello scambio di dati tramite email. A distanza di decadi dovremmo quindi iniziare ad imparare qualcosa dagli errori e **gestire in modo più furbo e con delle procedure ben definite lo scambio di file in ingresso ed in uscita dalla nostra organizzazione**.

Il mezzo “email” non è qualificato per questa funzione ed espone a molti rischi (Emotet è solo uno dei tanti). Scambiare file è ovviamente indispensabile a molti utenti, un’approccio corretto potrebbe quindi essere quello di valutare, sulla base delle esigenze degli utenti, una piattaforma che consenta agli utenti di inviare e ricedere file secondo delle policies ben definite e condivise.

Questo cambio di approccio alla gestione della condivisione dei files porterebbe diversi vantaggi:

- consente di identificare meglio l’interlocutore grazie ad uno scambio di credenziali/referenze
- consente una gestione centralizzata dei dati scambiati sia dal punto di vista della tutela che per quanto riguarda eventuali tecniche di analisi delle minacce (ATP ad esempio) prima che i contenuti arrivino sull’endpoint dell’utente
- consente di ottimizzare l’utilizzo degli archivi di posta spesso impropriamente utilizzati come file server

Il corretto approccio al problema migliora la postura di tutta l’organizzazione e, per lo specifico tema, **migliora anche il percepito dall'esterno e diventa un elemento di valutazione**: io personalmente scambio più volentieri dati con chi mi mette a disposizione strumenti utili alla tutela delle informazioni che condivido e che ricevo.

Lo strumento da utilizzare lo scegliete voi, non mancano certo le piattaforme ed i software in tal senso… ma **il punto resta l’approccio e l’esigenza di definire prima una strategia di gestione e delle regole condivise**, una volta fatto questo lo strumento viene da se.