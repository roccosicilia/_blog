---
layout:     post
title:      "Cloud Security: assessment e detection [prima parte]"
date:       2022-04-14 08:13:35 +0200
categories: [cyber-security, hacking, ita]
image:
---
Quella che voglio fare è una prima riflessione ad "alta voce" su un tema che, per una serie di coincidenze, ho toccato in diverse occasioni negli ultimi giorni. Scrivo quindi di getto qualche pensiero e annoto pubblicamente qualche risorsa per dar seguito poi a qualche approfondimento.

Parto dallo scenario: molte aziende ed organizzazioni hanno spostato - e continuano a spostare - workload e dati in cloud sfruttando i vantaggi ed i servizi dei diversi provider ed in particolare dei tre big: AWS, Azure, GCP. Osservo due principali comportamenti: chi "sposta" ciò che fino a ieri gestiva con una Virtual Machine nella sua forma più simile, come una instance, e chi (a mio parere più saggiamente) approfitta dell'occasione per rivedere anche la forma dei propri workload e fa uso di containers, soluzioni as-a-Service per storage e basi dati, soluzioni/implementazioni serverless. Non è questa l'occasione per discutere di quale sia la strategia migliore per spostare i workload in cloud, parlatene con i vostri cloud architect che sapranno consigliarvi a dovere, il tema che voglio affrontare è come gestire la sicurezza dei dati e dei servizi una volta che li avete spostati... tema che sarebbe meglio affrontare prima di spostare i workload, giusto per non andare poi a mettere pezze.

Parto da qualche domanda che credo dovremmo porci:

- Nella realizzazione del nuovo scenario sono state considerate le linee guida del provider in termini di sicurezza dei sistemi e dei dati? (Security by design)
- Una volta spostati i dati ed i servizi, dobbiamo ancora preoccuparci di verificare l'esposizione a minacce? (Security Assessment e Security Test)
- Come gestiamo la detection di eventuali attività sospette? Le procedure e gli strumenti che abbiamo implementato per i sistemi "on prem" sono ancora valide? E le competenze?
- Come reagiamo ad eventuali incident? Abbiamo adeguato le procedure e le strategie di incident management? Ci siamo dotati di strumenti coerenti al nuovo assetto tecnologico?

Discutendo con qualche addetto ai lavori è emerso che non tutte le scelte fatte per i sistemi ospitati "tra le mura aziendali" conservino la loro validità una volta spostati e trasformati i workload. Inoltre capita frequentemente di approcciale la gestione di ciò che è in cloud adattando procedure storicamente applicate per i workload attivi presso i Data Center dell'organizzazione. E' sicuramente vero che la gestione di alcuni aspetti va in delega al provider ma è altrettanto vero che la delega non piò essere totale: molte configurazioni degli ambienti restano a discrezione dell'organizzazione a partire dagli accessi ed i profili degli utenti, l'eventuale software che chiediamo di eseguire alle piattaforme cloud ha le stesse esigenze del software che facciamo girare all'interno del nostro (Virtual) Data Center, temi come la riservatezza e l'integrità dei dati restano in buona parte in carico al cliente della piattaforma. Per farla breve la sicurezza delle informazioni va gestita in ogni caso, cambiano probabilmente alcuni dettagli operativi ma le metodologie base non cambiano.

Ovviamente gli aspetti da considerare sono moltissimi, in questa prima riflessione volevo partire dagli argomenti che recentemente mi è capitato di affrontare: Assessment e Detection.

## Security Assessment

Sul fronte dei security assessment l'esigenza è forse palese: probabilmente non ci si metterà ad eseguire scansioni delle vulnerabilità delle piattaforme cloud (o forse si, io un check lo farei comunque o quanto meno farei delle valutazioni di merito) ma indubbiamente ha senso verificare la coerenza delle configurazioni applicate in fase di attivazione dei servizi al fine di non esporre vulnerabilità logiche e by desing. Inoltre, come accennavo, è probabile che l'organizzazione debba utilizzare componenti software di terze parti o auto-prodotte all'interno della propria piattaforma cloud, questi elementi avranno le stesse esigenze di gestione e manutenzione di prima anche se sarà probabilmente un po' più semplice agire mitigation e remediation grazie agli strumenti che i cloud provider stessi mettono a disposizione.

Nota a margine. Il tema degli strumenti di gestione o a supporto delle applicazioni in cloud non è banale, disporre di molte opzioni anche a livello di soluzioni di protection rapidamente implementabili è un indiscutibile vantaggio di gestione. Un esempio banale: un security test mette in evidenza una vulnerabilità software in una applicazione web per la quale non esiste una fix e si mitiga con una configurazione a livello di Web Application Firewall probabilmente già disponibile tra le funzionalità attivabili all'interno dell'ecosistema cloud.

Proviamo a ragionare sulla metodologia e per questa prima analisi restiamo sui classici: NIST, [Security Testing and Assessment Methodologies](https://csrc.nist.gov/CSRC/media/Presentations/Security-Testing-and-Assessment-Methodologies/images-media/day2-6_kscarfone-rmetzer_security-testing-assessment.pdf). Il documento, che credo non abbia bisogno di presentazioni, illustra metodologia e fasi per un security assessment e ci ricorda le motivazioni per il quale ha senso condurre questo tipo di analisi:

- Conferma se i sistemi sono stati opportunamente resi *sicuri*
- Identifica eventuali requisiti di sicurezza dell'organizzazione non soddisfatti (*)
- Soddisfa il requisito di eseguire una valutazione/misurazione periodica del sistema
- Non sostituisce i controlli si di e la gestione della sicurezza dei sistemi

(*) Da notare che il framework parte da un assunto: che l'organizzazione abbia definito dei requisiti di sicurezza. Partiamo quindi da questo punto, abbiamo definito dei requisiti di sicurezza per ciò che stiamo implementando in cloud? Ci sono scelte e valutazioni che le organizzazione devono necessariamente eseguire in autonomia ma qualche spunto, se non sapete da dove partire, spesso viene dato proprio dai cloud provider.

## Detection

Il secondo argomento parte da una domanda facile: come gestire il rilevamento dei security incident per un workload in cloud? Ovviamente rilevare l'icident è solo la scintilla di tutto ciò che riguarda poi la gestione dell'incident stesso, ma in questo momento restiamo solo sul tema della detection e, sempre per semplicità, restiamo ancora su NIST come riferimento.

A pagina 7 del documento "[Framework for Improving Critical Infrastructure Cybersecurity](https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.04162018.pdf)" c'è una definizione abbastanza chiara:

<img src="{{ '/assets/images-posts/image-2.png' | relative_url }}" alt="image 2" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

NIST - Framework for Improving Critical Infrastructure Cybersecurity

Chiaramente la funzione di detection ha lo scopo di individuare eventuali eventi di interesse per la gestione della sicurezza dell'infrastruttura e dei dati da essa gestiti. Per gestire la detection dobbiamo quindi necessariamente accedere agli eventi che interessano i workload tenendo in considerazione il fatto che in molti casi non si parla più di Syslog e Windows Events. Le diverse piattaforme mettono infatti a disposizione in forme diverse gli eventi che interessano i vari servizi, di solito grazie a delle API che consentono di interrogare i sistemi oggetto di interesse.

Va anche considerato che strumenti che tipicamente vengono utilizzati dalle organizzazioni come SIEM e XDR devono disporre di opportune funzionalità per accedere a questo patrimonio di informazioni e devono anche sapere cosa farci con quei dati. Provo a chiarire il tema con un esempio: se il nostro SIEM deve analizzare i log provenienti da una istance o da un container probabilmente poco cambia rispetto a ciò che arrivava dalla virtual machine (sui container ci sarebbe di più da dire, eventualmente ne parlo in una live), ma se gli eventi sono prodotti dalla piattaforma che gestisce le nostre applicazioni in modalità serverless (es: procedure di integrazione, scripts di automazione) i nostri sistemi sono in grado di analizzare correttamente eventi di questo tipo?

Tecnologicamente è più che fattibile, è necessario tenere a mente che il passaggio di un workload in cloud richiede ancora che venga gestita la detection e che potremmo dover adeguare procedure e strumenti.

## Best Practices

Nella maggior parte dei casi parliamo dei tre big player citati, ma in generale tutti i provider di servizi mettono a disposizione delle linee guida per affrontare diversi aspetti della sicurezza dei sistemi e dei dati all'interno dell'universo cloud.

In questa prima parte vorrei quindi dare un'occhiata a cosa suggeriscono a livello di best practices i tre provider di riferimento: AWS, Azure e GCP.

Inizio da AWS che aggrega in un pagina una serie di temi per i quali rimanda a diversi articoli e trainng: <https://aws.amazon.com/it/architecture/security-identity-compliance/>.

<img src="{{ '/assets/images-posts/image-3.png' | relative_url }}" alt="image 3" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

I titolo sono più che eloquenti. Il tema **Identity e Access Management** è evidentemente un argomento cruciale per una piattaforma cloud dove dovranno probabilmente accedere più utenti con credenziali di servizio per la gestione delle diverse componenti. E' quindi opportuno proteggere opportunamente questo livello di accesso e profila correttamene gli utenti in modo da non dare privilegi elevati a chiunque.

AWS dedica inoltre uno spazio dedicato al tema della **Detection** dove cita una soluzione interna alla piattaforma - Security Hub - che consente di gestire alcune minacce (solitamente quelle più comuni) con delle azioni preimpostate (playbook); su questo elemento siamo già su un altro tema che in realtà ha un capitolo dedicato: le azioni di mitigation e remediation. Viene inoltre citata un'altra componente che dalla documentazione mi sembra più "core" per la funziona di detection che è GuardDuty.

---

Anche per Azure abbiamo a disposizione molta documentazione, devo dire tantissima ma anche molto sparsa. Ho trovato utile partire da un documento di sintesi con una top 10 di argomenti con i relativi rimandi alla documentazione dedicata: [https://docs.microsoft.com/.../cloud-adoption-framework/secure/security-top-10](https://docs.microsoft.com/en-us/azure/cloud-adoption-framework/secure/security-top-10).

Noto subito un certo allineamento di argomenti: anche Azure parte dal tema degli utenti suggerendo formazione specifica e ovviamente una corretta gestione delle profilazioni. Si fa quindi riferimento a role-base access control e [identity and key management](https://docs.microsoft.com/en-us/azure/cloud-adoption-framework/organize/cloud-security-identity-keys).

Su fronte della **detection** trovo un approccio interessante che titola "Integrate native threat detection". In sintesi si parla di integrare le funzionalità di detection di Azure direttamente all'interno del proprio SIEM di riferimento. In questo caso si sta facendo riferimento, se comprendo bene, alle funzionalità di [Microsoft Defender for Cloud](https://docs.microsoft.com/en-us/azure/defender-for-cloud/defender-for-cloud-introduction), componente che vale quindi la pena di indagare meglio.

---

Anche per Google Cloud esiste una montagna di documentazione con una main page che raccoglie le best practice: <https://cloud.google.com/security/best-practices>. La struttura della documentazione di BigG è ovviamente differente rispetto ad Azure e AWS e anche in questo caso bisogna andare un po' a caccia dei temi. Già nella main page li parla però di moltissimi aspetti tra cui il già citato tema dell'**Access Management** e un interessante documento che titola "Security best practice checklists".

Sul tema Detection anche Google risponde con una propria soluzione: <https://chronicle.security/>. Di fatto un SIEM "cloud-native" (su questa denominazione potremmo discutere all'infinito) per le operazioni di **detection and response**.

## Qualche conclusione non concludente

Come scrivevo l'obiettivo di questo primo post era far(mi/ci) un'idea come si stanno muovendo i big player sul fronte della gestione delle minacce in un contesto che varia rapidamente ed è sicuramente molto diverso da quello che le aziende tipicamente gestiscono internamente.

Partire dalla letteratura mi aiuta a organizzare le idee per andare poi a selezione gli argomenti da approfondire. Quindi per ora mi fermo qui e agli interessati lascio il link al mio canale Twitch dove questa sera - giovedì 14 aprile - alle 21:30 faccio una sessione di studio in cui leggiamo e chiacchieriamo a ruota libera su questo tema: <https://www.twitch.tv/roccosicilia>.
