---
layout:     post
title:      "Concetti di hacking etico per team IT: Intro e Reconnaissance."
date:       2024-01-02 09:00:00 +0100
categories: [cyber-security, hacking, ita]
image:
---
Tema "vecchio", discusso almeno sei anni fa con un po' di gente del settore: portare nozioni di sicurezza offensiva o hacking (nel titolo ho voluto usare una formula abbastanza comune e riconosciuta) a figure professionali che non sono chiamate ad usarle in prima persona.

Il vantaggio che ci ho sempre visto è di pura consapevolezza: buona parte delle figure IT non hanno idea di come si muova un threat actor, la loro conoscenza della materia è limitata ai temi mainstream: i malware, i ransomware, i concetti di Data Breach. Raramente conoscono le tecniche di attacco se non quelle più *famose*, note perché passate agli onori della cronaca.

[<img src="{{ '/assets/images-posts/image.png' | relative_url }}" alt="image" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />](https://www.patreon.com/posts/concetti-di-per-95721880)

Video di approfondimento su Patreon

Il concetto di base e' molto semplice: se conosco il modus operandi del threat actor posso facilmente prevenire alcune situazioni spiacevoli, ad esempio introducendo concetti di security by design o hardening dei sistemi.

In passato avevo preparato del materiale specifico per i team IT, in questi giorni lo riprendo in mano e qui faccio una piccola sintesi. Ho pensato ad una suddivisione in moduli:

- Introduzione al concetto di hacking etico - Per un team IT credo sia più utile avere una infarinatura del modello senza addentrarci eccessivamente nel campo del penetration testing, non perché non sia utile ma perché credo che l'attività di penetration testing richieda un focus tale da renderla poco compatibile con le attività che devo svolgere un system/network administrator.
- Panoramica sulla Cyber Kill Chain - Molti hanno ben presente le fasi di un attacco, pochi hanno un idea precisa di cosa comportano e su cosa fanno leva le singole fasi.
- Focus sulle fasi di un attacco in chiave IT/*sistemistica*:
  - **Reconnaissance**: comprensione e valutazione della superficie attaccabile, social engineering, OSInt.
  - **Weaponization**: valutazione della possibile "arma" da utilizzare nel contesto analizzato
  - **Delivery**: metodi di trasmissione dell'*arma* scelta
  - **Exploitation**: innesco o utilizzo dell'arma selezionata per sfruttare una falla nel sistema attaccato
  - **Installation**: installazione di componenti o compromissione della configurazione del sistema target al fine di ottenere una presenza persistente
  - **Command and Control**: instaurazione di un metodo di comunicazione sicuro con il sistema target
  - **Actions on Objectives**: esecuzione delle azioni sul target, fine ultimo dell'attacco

Provo a sviluppare su queste pagine una sintesi dei temi e condividerò slide e video con degli esempi e degli approfondimenti. Parto dall'inizio.

## Hacking

Personalmente il termine ***Ethical Hacking*** a me non piace: la pratica dell'hacking e' di per se etica ed il rafforzativo avvalora la tesi, a mio parere errata, che ci sia un hacking non etico. C'e' da dire che la mia formazione a partire dalla seconda metà degli anni novanta (si sono vecchio, lo so) si basava sui saggi di [Eric Raymond](https://en.wikipedia.org/wiki/Eric_S._Raymond) e [Pekka Himanen](https://en.wikipedia.org/wiki/Pekka_Himanen), quindi ho sempre avuto un idea di hacking molto affine ai concetti di ricerca, studio, miglioramento, crescita, curiosità. Detto questo mi riferirò, da qui in poi, semplicemente al concetto di hacking.

Applicate ai nostri scopi le pratiche dell'hacking nel campo della sicurezza informatica sono utili per comprende a fondo il funzionamento di un sistema compresso e valutarne eventuali falle osservandolo nel sui insieme, non solo a livello tecnico (i sistemi informativi) ma a livello globale: strutture fisiche, persone, processi, collegamenti, sistemi, servizi, modello di business, ...

Una delle principali caratteristiche dell'hacking e' la curiosità che spinge ad un livello di approfondimento estremo ed e' quindi ovvio osservare un target come un sistema complesso di elementi che interagiscono tra loro. Se il mio obiettivo e valutare la sicurezza di una organizzazione allora devo considerare tutte l'organizzazione, sono solo i sistemi informativi.

## Cyber Kill Chain

Esistono diverse versioni e riadattamenti della cyber kill chain, la più famosa è sicuramente la versione Lockheed Martin ripresa in quasi tutte le presentazioni ed articoli in cui viene affrontato il tema.

<img src="https://www.lockheedmartin.com/content/dam/lockheed-martin/rms/photo/cyber/THE-CYBER-KILL-CHAIN-body.png.pc-adaptive.1280.medium.png" alt="immagine" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

In estrema sintesi si tratta di una descrizione, a mio parere ottima, delle fasi di un attacco e consente di fare una sorta di zoom-out del modus operandi dei threat actor. Non e' raro trovare persone che non hanno una visione completa di come si svolge un attacco informatico in quanto sono consapevoli di quello che riescono a vedere o tracciare, spesso limitato agli effetti dell'attacco come un tentativo di exploiting bloccato dal sistema EPP o una email di phishing.

Ciò che sfugge sono gli eventi che hanno preceduto l'azione visibile: per arrivare alle azioni "invasive" il threat actor ha dovuto preparare il terreno per assicurarsi che l'attacco sia efficace. Non è una regola fissa, esistono threat actor che sparano nel mucchio e gli effetti sono anche relativamente facili da osservare, basta buttare un occhio ai log in un UTM Firewall utilizzato per esporre qualche servizio o i log di un webserver.

Essere consapevoli della struttura di un attacco ci consente di comprendere meglio alcuni eventi che ci capita di osservare come una strana email di phishing, un evento anomalo sul firewall, un comportamento inaspettato di un'applicazione aziendale. Il fatto che un attacco si svolga per fasi ci da la possibilità di adattare la nostra postura di sicurezza al modus operandi del threat actor così da prevenire alcune sue mosse.

## Reconnaissance

E' la fase forse meno presa in considerazione dai non addetti ai lavori, è fondamentale per chi lavora in questo campo. Tutte le valutazioni che seguiranno dipendono dalle informazioni che l'analista (o il threat actor) riesce ad ottenere dal proprio target. Su questo tema ho già scritto e qui riporto i post dedicati:

- <https://roccosicilia.com/2023/07/25/penteststudy-info-gathering-intro/>
- <https://roccosicilia.com/2023/08/01/penteststudy-passive-info-gathering/>
- <https://roccosicilia.com/2023/09/25/penteststudy-active-info-gathering/>

In questo post mi limito a dare un po' di struttura al tema. Durante questa fase si viene in contatto con una enorme quantità di dati che riguardano l'organizzazione target e le persone che la popolano. Per prima cosa c'è un tema etico da considerare: eventuali informazioni sulla vita privata delle persone dovrebbero essere trattate con una certa cautela, o meglio, non dovrebbero proprio essere trattate. La privacy dell'individuo non deve essere minacciata da un security test pur consapevoli che nel mondo vero il threat actor non bada a questo dettaglio. **Accettiamo quindi i limiti imposti dal rispetto della privacy consapevoli del fatto che l'analista disporrà di una quantità di dati inferiore rispetto a quella che potrebbe reperire il criminale informatico**.

Altro tema da considerare è la riservatezza delle informazioni, tema che vale per tutte le fasi del security test. Per quanto apparentemente innocui i dati provenienti da forti pubbliche (siamo quindi nell'ambito OSInt) possono facilmente essere sfruttati a fini illeciti. Di fatto questo è ciò che avviene anche durante i test: i dati raccolti vengono utilizzati per valutare una strategia di attacco. Al pari dei dati più tecnici, queste informazioni vanno gestite in modo da non essere accessibili a chiunque, sia all'interno dell'azienda che esegue il test che all'interno dell'organizzazione target. Se un threat actor si trova nelle condizioni di poter fruire di tali informazioni avrebbe parte del lavoro già svolto e potenzialmente validato.

Come ultimo punto strutturale citerei il tema della documentazione e catalogazione dei dati. Se è vero che di base si tratta di prendere appunti è anche vero che molti dei dati raccolti vanno messi in relazione tra loro, vanno approfondito ed arricchiti. Uno dei tool più apprezzato per questa fase del lavoro è sicuramente Maltego in quanto permette di personalizzare a livello visuale molti dati e consente di strutturare dei grafi. Anche io lo uso abitualmente come base di visualizzazione anche se sto rapidamente migrando ad una piattaforma che mi sto scrivendo nel tempo libero: un database che mi consente di raccogliere e relazionare diversi dati provenienti da fonti aperte (il progetto è disponibile su [GitHub](https://github.com/roccosicilia/eg0n)).
