---
layout:     post
title:      "Honeypot e threat intelligence"
date:       2025-05-21 13:00:00 +0200
categories: [cyber-security, hacking, ita]
image:      /assets/images-posts/screenshot-2025-05-21-at-15.44.25.png
---
Come promesso durante la live di venerdì (02.05.2025) faccio un post di recap sul tema degli honeypots e sul loro utilizzo nell'ambito della threat intelligence.

Il concetto di honeypot credo sia ben noto: si tratta di software che ci consentono di creare sistemi "civetta" per gli attacker, ambienti che assomigliano a sistemi di produzione appetibili ma che in realtà sono delle vere e proprie trappole che registrano ogni sollecitazione a cui sono sottoposti. Mentre in un ambiente di produzione dobbiamo necessariamente discriminare il traffico e le azioni lecite da quelle potenzialmente malevole per capire cosa stia succedendo, in un honeypot non sono previste interazioni lecite. Ne consegue che tutto ciò che si osserva è potenzialmente un'azione offensiva verso il target.

Ci sono due principali ambiti in cui possiamo sfruttare questa peculiare situazione ed in questo post ne affrontiamo uno in particolare: la threat intelligence. È chiaro che se ho a disposizione uno strumento che funge da *barattolo di miele* per le formiche, dove le formiche sono i threat actor, posso potenzialmente raccogliere informazioni specifiche sul comportamento degli stessi nelle diverse fasi di un attacco. Più il mio strumento è in grado di interagire e più saranno i dati che potrò raccogliere in relazione alle tecniche di attacco utilizzare.

---

Se trovi utili i miei contenuti [puoi sostenere il mio progetto di divulgazione](https://patreon.com/roccosicilia) tramite il mio Patreon. Sostenendo il progetto mi aiuterai creare a condividere nuovi articoli tecnici e video di approfondimento, inoltre i sostenitori accedono a diversi contenuti esclusivi ed agli archivi delle Live Session come quella registrata lo scorso venerdì e disponibile in archivio.

[<img src="{{ '/assets/images-posts/screenshot-2025-05-04-at-16.48.25.png' | relative_url }}" alt="screenshot 2025 05 04 at 16.48.25" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />](https://www.patreon.com/posts/live-session-e-128125019)

Sessione live del 02.05.2025

---

## Scenario di base

Una delle prime azioni che il threat actor compie è chiamata discovery, ovvero deve individuare dei sistemi nella rete che siano potenzialmente interessanti. Per eseguire questa azione solitamente ci si affida a tools o script che inviano richieste ai sistemi cercando specifici servizi disponibili, ad esempio se volessi individuare tutti i web-server di una rete potrei eseguire una richiesta verso la porta 80 e 443 degli IP della rete ed annotare i sistemi che rispondono a questa richiesta.

Un noto strumento per questo tipo di attività è nmap, usatissimo dagli addetti ai lavori ma che possiamo considerare un po' troppo rumoroso per azioni offensive realistiche, anche perché è relativamente semplice per un firewall ben configurato riconoscere "l'impronta del tool" ed agire di conseguenza. Nel "mondo vero" è più probabile vengano usati metodi meno riconoscibili, per l'occasione scriviamo qualcosa di molto semplice come un python script che esegua delle richieste HTTP e verifichi la risposta del servizio.

<img src="{{ '/assets/images-posts/screenshot-2025-05-05-at-23.05.09.png' | relative_url }}" alt="screenshot 2025 05 05 at 23.05.09" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Test script *httpCheck.py* disponibile nella repo <https://github.com/roccosicilia/honey-eg0n>

Ora mettiamoci nei panni del threat actor che ha individuato un target interessante ed ha bisogno di capire se ci sono hosts che presentino servizi specifici e potenzialmente vulnerabili, quindi usiamo il nostro tool "contro" la subnet target e vediamo quali hosts del perimetro rispondono.

Una subnet pubblica solitamente è costantemente sollecitata da tentativi di scansione ed exploiting ed il firewall di perimetro ha la capacità di registrare nel proprio traffic log tutto il traffico (che sarebbe bello portare in un SIEM, ma ne parliamo in un prossimo post), compreso quello anomalo. Il target è quindi già nella condizione di individuare anomalie in mezzo al "rumore" del resto del traffico. Un honeypot ci consente di isolarci rispetto alle conversazioni in corso in quanto il sistema sarebbe interessato quasi esclusivamente da traffico anomalo: se metto in rete un servizio che nessun utente utilizza, tutto il traffico che riceve è potenzialmente anomalo se escludo il broadcast. In base a questo principio una semplice azione di discovery, per quanto delicata e poco rumorosa, verrebbe osservata e tracciata nel log del nostro honeypot.

A “basso livello” dobbiamo scrivere un tool che si comporti come un normalissimo web server di base: alla richiesta *GET o POST /* di un browser dobbiamo rispondere con un contenuto che il client visualizzerà.

<img src="{{ '/assets/images-posts/image-3.png' | relative_url }}" alt="image 3" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Funzione di risposta alle richieste GET

Ovviamente ogni richiesta con i relativi dati deve essere registrata in un log file in modo da consentirne l'analisi.

Nell'esempio disponibile nella repo, che ho intenzione di strutturare meglio nel tempo, abbiamo iniziato ad intercettare alcuni tipi di richieste, non solo le **richieste /** quindi ma anche una richiesta **/admin** ed una richiesta **/robots.txt**. L'interazione che si può ottenere è altissima, una delle evoluzioni potrebbe essere quella di presentare dei campi per invogliare dei tentativi di injection.

Una volta ottenuto il nostro finto web-server ci manca solo una macchina su cui farlo girare con un IP pubblico da esporre e vedere cosa succede.

<img src="{{ '/assets/images-posts/screenshot-2025-05-21-at-15.44.25.png' | relative_url }}" alt="screenshot 2025 05 21 at 15.44.25" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Esempio di richieste raccolte dal honeypot.

Ora che abbiamo i primi dati possiamo iniziare a ragionare di analisi.

## Threat Intelligence

Non mi azzardo a trattare il tema interamente in questo post, ma vorrei accennare a come si potrebbe sviluppare il processo partendo dal nostro piccolo esperimento. È evidente che quello che stiamo intercettando sono probabilmente bot a caccia di sistemi specifici o a caccia di vulnerabilità note da sfruttare. Nell'eseguire queste scansioni il threat actor ci regala qualche dato: sicuramente l'IP della macchina che sta eseguendo la scansione, lo user agent, la URI e, in alcuni fortunati casi, il payload utilizzato. Già con questi dati abbiamo di che divertirci.

Task per le prossime live sull’argomento: leggiamo assieme qualche dato e vediamo come approcciare un’analisi e creare un evento sulla piattaforma MISP che stiamo implementando a livello community.

---

Sei interessato a partecipare al progetto MISP che sto portando avanti? Contattami direttamente sul mio server [Discord](https://discord.gg/Ys5AAbsyyH) ed iscriviti al blog per restare aggiornato.

---

La prossima live sul tema l'ho pianificata per il 23.05.2025 sul mio canale [YouTube](https://youtube.com/@roccosicilia).
