---
layout:     post
title:      "Assume Breach: evoluzione di uno scenario"
date:       2025-09-05 18:34:44 +0200
categories: [cyber-security, hacking, ita]
image:      /assets/images-posts/coding.png
---
Sto preparando una breve presentazione di un ipotetico scenario di test nella modalità Assume Breach e ne approfitto per scrivere due righe in merito... qualche dettaglio sull'esperienza ve lo racconto su [Patreon, come sempre nei miei "***dietro le quinte***"](https://www.patreon.com/c/roccosicilia/posts?filters%5Btag%5D=dietro+le+quinte).

La presentazione sarà in inglese ma per questo post mantengo l'italiano, eventualmente lo traduco per la mia pagina su [Medium](https://roccosicilia.medium.com/).

#### Preparazione dello scenario

Quando si affronta un test in questa modalità è bene definire degli assunti che poi potranno essere verificati su campo. Nel mio scenario si assume che:

- il target/client mette a disposizione un riferimento interno coinvolto nelle attività di test che dovrà essere escludo da eventuali path di escalation
- il test partirà da una workstation a cui il Threat Actor ha accesso con una credenziale valida, non sono quindi in *scope* le azioni che hanno portato l'attaccante in possesso delle credenziali
- il test viene eseguito mantenendo i sistemi di detection attivi ed eventuali servizi di monitoraggio (MDR/SOC) all'oscuro dell'attività
- il test prevede l'esplorazione della rete target ed azioni anche su altri sistemi, non esiste un preciso scope o vincoli se non definiti in anticipo

Prima di eseguire le attività onsite è opportuno raccogliere dati, da fonti pubbliche, sulla corporate: potrebbe essere utile identificare eventuali tecnologie in uso come Firewall, EDR ed eventuali software utilizzati sui client. Questa fase può dare spunti interessanti: identificare eventuali software in uso dal target permette di valutare attack path specifici per il contesto.

<img src="{{ '/assets/images-posts/image-18.png' | relative_url }}" alt="image 18" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Guardando alla Cyber Kill Chain così come solitamente la definiamo (oggi prendo in prestito una slide Cisco), le fasi che considero in questo scenario sono quindi la Reconnaissance per poi saltare all'Exploitation e da li seguire le fasi successive.

#### Esecuzione del C2

Il focus della mia presentazione è l'avvio di una sessione di comunicazione con il mio C2 senza farsi intercettare/bloccare da Firewall, IDS ed EDR e da questa posizione eseguire azioni esplorative all’interno della rete. Il mio attuale modo di operare (2025) non è lo stesso che utilizzavo quando ho iniziato a lavorare in modo strutturato a questa tipologia di test (2019-2020), penso sia utile raccontare almeno i principali step del processo che ha portato all'attuale risultato, a prescindere dagli esiti delle singole evoluzione che hanno una valenza legata al periodo di utilizzo, concetto che spiego meglio durante il post.

Tempo fa utilizzavo semplici sessioni tcp o http per aprirmi delle comode reverse shell scritte per lo più in Powershell, con un po' di furbizia ed *obsuscation* si riusciva ad ingannare AMSI e anche molti EDR. Powershell era/è spesso disponibile sui sistemi target senza particolari limiti e bastavano poche macro ed una USB rubber ducky per ottenere risultati. Ho anche fatto uso di infrastrutture C2 note come *Covenant* ma un bel giorno approdai su *Villain* (ne ho parlato spesso su questo blog) ed ho iniziato a lavorare su varianti dei payload "compatibili" con questo framework.

<img src="{{ '/assets/images-posts/screenshot-2025-08-28-at-09.18.24.png' | relative_url }}" alt="screenshot 2025 08 28 at 09.18.24" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Due esempi di payload generati con Villain

Se analizziamo il codice generato si nota la meccanica di funzionamento di questi payload e, se si *bazzica* un po' il mondo dei C2, il modello risulterà molto familiare. Se indentiamo il codice si capisce subito cosa sta accadendo:

<img src="{{ '/assets/images-posts/image-19.png' | relative_url }}" alt="image 19" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

L'esempio precedente ma leggibile

La variabile *$v* contiene il risultato di una *Invoke-RestMethod* (una chiamata *http get*) verso una URL che nel mio script corrisponde all'indirizzo del C2 a cui vengono passare delle informazioni tramite le stesse stringhe inserite in URL: l'identificativo della sessione *aa0471*, l'*hostname* e lo *username*. Questa informazione serve al server Villain per "mappare" la sessione.

Il *core* del funzionamento è il ciclo *for()*: ad ogni iterazione lo script esegue una prima *Invoke-RestMethod* con cui chiede al server il comando da eseguire (variabile *$c*), successivamente il comando viene eseguito localmente tramite *Invoke-Expression $c* (output in variabile *$r*) ed il risultato viene infine inviato al server con una *http post* che nello script è l'ultimo *Invoke-RestMethod [...] -Method POST*.

---

Se trovi utili i miei contenuti ed il lavoro di ricerca che svolgo e condivido puoi supportarmi iscrivendoti ad uno dei miei canali come [il mio Patreon](https://patreon.com/roccosicilia).

Se vuoi rimanere aggiornato su prossimi articoli e video puoi iscriverti a questo blog:

Da qualche giorno è attivo anche un subreddit per discutere dei temi che tratto abitualmente: *[r/SheliakNotes](https://www.reddit.com/r/SheliakNotes/)*.

---

Fortunatamente le capacità di detection di AMSI e degli EDR si sono rapidamente adeguate, oggi (e già dal 2023) la telemetria di uno script Powershell che innesca un ciclo come quello descritto genera una istantanea reazione di AMSI e, se per qualche ragione si riesce ad aggirare il controllo locale, ci pensa l'EDR ad intercettare e riconoscere la sequenza di comandi come un pattern sospetto. Le regole di detection di molti EDR (in configurazione di dafault) sono però legate al contesto Powershell ed all'intercettazione di specifiche sequenze di comandi come una ***curl*** seguita da una ***iex***.

Regole di detection troppo precise sono facilmente aggirabili in quanto è sufficiente alterare a sufficienza le componenti del pattern per non consentire all'EDR di intercettare l'azione pur ottenendo lo stesso risultato. Un tipico esempio è l'utilizzo di utility di sistema "alternative" per eseguire una *http get*: [collection come quelle di ***LOLBAS*** ci hanno insegnato ad usare ***certutil.exe***](https://lolbas-project.github.io/lolbas/Binaries/Certutil/) (grande classico) per eseguire il download di un contenuto.

Chi lavora su questi temi ad alto livello solitamente implementa regole di detection in grado di tener conto di questi tricks, cosa che ovviamente pone dei limiti a chi fa security test (gente come me) ed anche ai Threat Actor.

#### Nuova strategia

> Ma allora come fanno i Threat Actor ad aggirare le regole di detections?

Devo premettere che non so quanto sia merito dei Threat Actor e quanto sia merito dei ricercatori. Quando ho cercato info sul tema sono risalivo a talk (DEFCON e BlackHat) in cui si parla aggirare i sistemi di controllo con diverse tecniche e si fa riferimento a Python, Go e Rust sia per implementare tecniche di evasione che per sfruttare i *Detection GAP*, ovvero la mancanza di regole di detection utili a riconoscere l'evoluzione di alcune minacce. Nel 2023 ho iniziato a lavora seriamente sul concetto di ***Detection GAP*** e solo di recente ho preso in mano il tema dell'***evasion*** pura.

La scelta fatta all'epoca è stata quindi quella di riscrivere il mio C2 in python, prima il solo payload e poi anche la componente server, in modo da avere uno strumento semplice ma molto efficace per aggirare le regole di detection "standard" (definiamole cosÌ) che molti Blue Team utilizzano sulle proprie piattaforme.

<img src="{{ '/assets/images-posts/image.png' | relative_url }}" alt="image" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Flusso semplificato

Il risultato è un semplice script in python che consente di eseguire comandi localmente impartiti dal C2 e da la possibilità al Pentester di governare la macchina target interagendo con il solo C2. Faccio una micro demo in questo video:

https://www.youtube.com/watch?v=z8ENXT5bwps

Demo e video con spiegazione

La struttura che ho scelto mi permette di definire delle "macro" da utilizzare nelle circostanze opportune o di impartire comandi a mia discrezione, dando il comando direttamente al C2.

Se non ci sono sistemi in grado di riconoscere il comportamento dello script come quello di una comunicazione verso un C2, l'azione passa inosservata e si può procedere con la successiva fase. Va ovviamente considerato che l'EDR è comunque attivo sul sistema, anche i comandi che si deciderà di utilizzare nelle successive fasi sono quindi analizzabili.

Utilizzare comandi Powershell è quindi possibile ma va comunque considerata la presenza di regole di deteciton che possono intercettare le azioni del Pentester. Ovviamente ci sono diversi miglioramenti che ho pensato di fare ed in parte ho fatto; ne parlo in diverse live, quindi vi suggerisco di seguirmi su [YouTube](https://youtube.com/@roccosicilia) e [Patreon](https://patreon.com/roccosicilia). Conto di scrivere un altro post quando rilascerò la prossima versione del C2.

#### Considerazioni

Il comportamento registrato varia, ovviamente, in base a moltissimi fattori:

- le tecnologie scelte sono sicuramente un fattore da considerare, non tutti gli EDR hanno la stessa capacità di detection
- la presenza di sistemi in grado di correlare eventi eterogenei (ad esempio i SIEM) può rappresentare un ostacolo importante per il Pentester
- la qualità delle detection rules dei sistemi impiegati dipende dalle competenze del team che presidia le soluzioni e dal livello di tuning che è stato fatto nel tempo

Da quello che ho potuto osservare il tema Detection GAP è critico. Molte soluzioni sono in grado di registrare gli eventi che portano alla compromissione ed all'exfiltration, ma spesso mancano regole in grado di "unire i punti" e generare un allarme.

È evidente che l'utilizzo di Powershell, anche all'interno della sessione C2, sia un comportamento ben osservato, è altrettanto evidente che fino a quando si resta in un contesto più opaco -- come l'invio di comandi come argomento di python -- le regole che solitamente sono attive sui sistemi non sono state implementate per intercettare un comportamento "sospetto" a prescindere dall'eseguibile che lo ha generato. Sintetizzando: c'è un sacco di l**avoro di qualità** da fare per ridurre questo GAP.

Vi lascio anche il link ad un [recente post su LinkedIn](https://www.linkedin.com/feed/update/urn:li:activity:7369645451475705858/) in cui propongo la discussione.
