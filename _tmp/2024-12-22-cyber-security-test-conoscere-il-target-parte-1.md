---
layout:     post
title:      "Cyber Security Test: conoscere il target (parte 1)"
date:       2024-12-22 15:00:00 +0100
categories: [cyber-security, hacking, ita]
image:      /assets/images-posts/cybersecurity-test-serie.png
---
Iniziamo subito con lo scoperchiare un enorme Vaso di Pandora e discutiamo la fase più sottovalutata da chi esegue security test: la raccolta delle informazioni. Il modello di base è molto semplice e si basa su un principio: meglio conosco il mio "avversario" e più sarò in grado di sferrare un attacco efficace.

Sul piano strategico la valutazione preliminare del target è fondamentale: l'obiettivo del potenziale threat actor deve guidare le scelte dell'analista che prepara la simulazione d'attacco. Bisogna quindi comprendere quali sono gli elementi sensibili del target, raccogliere tutte le informazioni possibili e da qualsiasi fonte e valutare un primo piano di attacco contestualizzando ciò che si è potuto scoprire. In pratica dobbiamo creare un dossier sul potenziale target.

---

Gli argomenti del post sono discussi ed approfonditi in una serie di live liberamente accessibili e di cui le registrazioni sono archiviate sul mio Patreon per i supporter.

[<img src="{{ '/assets/images-posts/image-13.png' | relative_url }}" alt="image 13" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />](https://www.patreon.com/posts/cyber-security-1-118474393)

Video di approfondimento tecnico.

---

Da considerare che la quantità di dati che potremmo trovare e le relative informazioni che elaboreremo saranno un quantitativo elevato ed estremamente eterogeneo. Oltre alle tecniche di ricerca ed ai tools di supporto dobbiamo dotarci anche di strumenti che consentano di documentare il tutto in modo appropriato. Ho pensato di approfittare di questo argomento per rivedere il mio sistema di documentazione e condividervi i concetti di base.

## Database?

Se devo gestire molti dati destrutturati a cui voglio poter applicare una struttura mi viene voglia di usare un Database. Devo anche avere una interfaccia comoda per inserire, modificare, cercare, visualizzare le informazioni e gli elaborati del caso. Ci sono molti strumenti che si possono adottare e la scelta dipende soprattutto dalle esigenze e conoscenze dell'analista che poi ci dovrà mettere le mani. Visto che lo scopo di questi post è studio e divulgazione ci possiamo permettere di dedicare del tempo alla scrittura di qualcosa di custom. Per non partire proprio da zero e considerando che alcuni temi si toccheranno, parto dalla base del progetto ***eg0n*** per costruire una django app d'appoggio in cui metteremo i dati che ci interessano.

## Raccolta delle informazioni (passiva)

È probabile che il termine più familiare per questo task sia Passive Information Gathering e ovviamente se esistono azioni passive ne esisteranno anche di attive.

In questo primo post iniziamo quindi dalle attività che possiamo condurre senza generare sospetto, utilissime per tutti quei test che puntano ad eseguire una valutazione della postura dall'esterno basandosi sulle molte informazioni che un target potrebbe aver distribuito piò o meno volontariamente. Questo tipo di test aiuta a comprendere quanto un target stia "esponendo il fianco" o se esistono in rete informazioni potenzialmente pericolose ed utilizzabili per azioni offensive.

Il principio alla base di questi test è relativo alla riduzione della superficie attaccabile, ovvero ridurre/controllare la quantità di informazioni che esistono, in rete e non, sul target in modo da limitare l'esposizione dell'organizzazione ad inutili rischi.

---

Se ti interessano ai miei contenuti puoi abbonarti al blog lasciando la tua email:

Il mio progetto di divulgazione comprende la scrittura di post e la pubblicazione di contenuti tramite Twitch Live e video. Per sostenere il progetto puoi registrarti ai miei canali o diventare un supporter su [Patreon](https://patreon.com/roccosicilia) dove pubblico anche contenuti inediti e dedicati ai supporter.

---

## Informazioni a partire dal sito web del target

Semplice quanto efficace: il sito web del target ci può fornire molti elementi che potremmo utilizzare in un secondo momento per una delle fasi del security test. Solitamente sono presenti informazioni sull'organizzazione come numero e posizione delle sedi sul territorio, dati sul modello di business ed in alcuni casi dati sul personale attivo (nomi, indirizzi email, numeri di telefono interni).

Queste informazioni non sono immediatamente utilizzabili da un threat actor ma possono essere elementi utili nelle fasi avanzate del test: i dati relativi al personale possono essere confezionati per sviluppare una campagna mirata di phishing o altre azioni di social engineering, nome e cognomi sono relativamente facili da trasformare un elenchi di utenze e email.

Il sito web stesso, se presenta componenti utilizzate da membri dell'organizzazione, potrebbe essere preso in considerazione come elemento da compromettere anche se esterno rispetto al perimetro dei sistemi IT interni. Ad esempio eventuali credenziali utilizzate per l'applicazione web potrebbero essere uguali o simili a credenziali utilizzate per sistemi aziendali o a quelle dell'utente che le gestisce, ottenerle attaccando la webapp potrebbe consentire al threat actor di aprire altre porte.

Oltre ai contenuti pubblici va considerato che ogni tanto gli sviluppatori commettono qualche errore. È sempre opportuno controllare:

- il codice HTML e JS a caccia di commenti soprattutto in versioni precedenti del sito
- eventuali directory pubblicate ma nascoste
- riferimenti a tecnologie usate per il sito web o altri elementi dell'infrastruttura

Durante la raccolta passiva va tenuto a mente il fatto che non deve esserci un contatto con le infrastrutture, ritengo accettabile eventuali attività assimilabili al normale comportamento di un utente che visita le pagine web del sito dell'organizzazione.

## Informazioni a partire dal Domain Name

Saliamo leggermente di livello rispetto al sito web e passiamo al DNS partendo dal **Nome Dominio**. Come noto i Domain Name servono a rendere intellegibili gli indirizzi degli host a cui vogliamo collegarci per accedere ad uno specifico servizio. Per visitare questo blog, ad esempio, avete digitato o richiesto di accedere a ***roccosicilia.com*** che corrisponde al Domain Name del mio sito web.

I domain name sono gestisti da enti ed aziende che ne consentono la registrazione e l'assegnazione a persone fisiche, aziende, società, ecc. ed i database con l'elenco dei nomi dominio, a prescindere dall'uso e dal proprietario, sono pubblicamente disponibili. C'è da dire che alcuni dati, per una questione di privacy, possono essere resi anonimi, come nel caso del mio nome dominio:

<img src="{{ '/assets/images-posts/image-3.png' | relative_url }}" alt="image 3" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Screenshot da icann.org

La raccolta di questi dati consente di fare dei ragionamenti, anche molto speculativi, sul target. Potrebbe essere utile annotarsi i servizi correlati come gli indirizzi dei Name Server utilizzati dal target e i riferimenti delle persone coinvolte che potrebbero essere membri dell'organizzazione. Anche associare tra loro questi elementi è utili ai fini dell'analisi.

Da questo micro-dato possono emergere informazioni relative ai rapporti con fornitori visto che il dominio va acquistato da qualcuno ed i DNS sono solitamente gestiti da un provider con cui bisogna avere un rapporto, potrebbero emergere informazioni su sistemi aziendali in caso i name server siano gestiti direttamente dal team IT. Come dicevo è difficile seguire un path lineare proprio per le molte ramificazioni che potrebbero derivare dal target. La cosa migliore è documentare tutto nella forma che più ci aiuta.

<img src="{{ '/assets/images-posts/image-4.png' | relative_url }}" alt="image 4" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Esempio di grafo con Maltego

Un bellissimo tool che possiamo utilizzare è Maltego che consente di costruire dei grafi con relazioni e molti dettagli (argomento trattato in dettagli nel video con gli approfondimenti sul tema) a cui possiamo affiancare i nostri appunti che per l'occasione vorrei strutturare in un database.

I dati che sicuramente vorrei annotare in relazione al domain name sono:

- Il nome del dominio (ovviamente)
- L'azienda associata, non necessariamente quella che lo ha acquistato
- I name server
- Data di:
  - creazione
  - scadenza
  - ultimo update

A questo vorrei associare i dati delle eventuali persone coinvolte, quindi non nella stessa "table" annoterò i riferimenti per il Registrant, il contatto Amministrativo ed il contatto Tecnico. Stiamo parlando quindi di tre table (models in django) dedicate: una per i domain name, una per le organizzazioni ed una per le persone.

<img src="{{ '/assets/images-posts/image-6.png' | relative_url }}" alt="image 6" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Esempio di ENTRY con i dati del mio blog.

Da questi semplici elementi la ricerca può procedere in diverse direzioni e, per esplorarle al meglio, utilizzerò un vero target di cui censurerò i riferimenti.

## Un esempio dal mondo vero

Supponiamo di voler raccogliere informazioni dalla *Bithorn Corp.* per valutare eventuali vettori di attacco esterni, partendo dal dominio web del target. Le "trasfomazioni" di Maltego ci possono rapidamente fornire qualche elemento di partenza:

<img src="{{ '/assets/images-posts/image-8.png' | relative_url }}" alt="image 8" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Maltego GUI

Una semplice DNS query come anche un ping ci consentono di ottenere dalla URL del sito target il suo ip. Le DNS query possono inoltre darci informazioni sui record del dominio, tipicamente possiamo chiedere il record MX (come si vede nello screenshot di Maltego), i record A ed i record TXT.

<img src="{{ '/assets/images-posts/image-10.png' | relative_url }}" alt="image 10" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Elementi raccolti tramite il tool dig.

Lo stesso processo possiamo eseguirlo per eventuali altri Domain Name che possiamo associare al target e che possiamo individuare tramite ricerche mirate. Ovviamente anche di questo dobbiamo andare a caccia e possiamo utilizzare diversi strumenti per estendere il perimetro da analizzare, ad esempio con delle query "mirate" sui motori di ricerca potremmo ottenere link a pagine web che parlano del nostro target ma che non fanno parte del dominio istituzionale che già conosciamo:

<img src="{{ '/assets/images-posts/image-11.png' | relative_url }}" alt="image 11" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Con questa ricerca si ottengono anche tutti i link in cui si parla del target su siti terzi, altre fonti da analizzare.

## Nel prossimo post...

Compreso lo scopo ed i principi base della ricerca di informazioni per prossimo post discutiamo le principali tecniche e tools per:

- ottenere un elenco di domini, url ed IP address che si riferiscano al target
- ottenere un elenco di riferimenti (persone, dipendenti, collaboratori, ecc) relativi al target e loro dati come username, email, numeri di telefono
- ottenere informazioni sulle tecnologie usate dal terget

Questa serie di post non ha la forma del tutorial, quindi gli esempi ci servono a comprendere lo scopo dei security test e come possiamo usarli per migliorare la nostra postura.
