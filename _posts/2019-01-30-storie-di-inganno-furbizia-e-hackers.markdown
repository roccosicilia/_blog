---
layout: post
title:  "Storie di inganno, furbizia e hackers."
date:   2019-01-30 09:00:00 +0200
categories: [cyber-security]
---
Un attacco informatico ben riuscito raramente è costituito da una singola e categorica azione. Osservando come il business del Cyber Crime “fa i soldi” balza all’occhio l’enorme fetta di revenues relativa al furto e “commercio” delle informazioni. Il furto di questi dati (quello che fa figo chiamare Data Breach) è possibile miscelando sapientemente astuzia, inganno, fantasia e stregoneria… perché quando parlo di “ attacco informatico ben riuscito “ mi riferisco a quell’opera dell’ingegno che porta l’attacker a prendere residenza all’interno di un sistema informatico vittima — senza che nessuno se ne renda conto — per depredarlo silenziosamente per mesi o anni, spesso mentre chi lo presidia afferma che “è tutto sotto controllo”.

La premessa era doverosa per introdurre il tema di questo post, in cui vorrei raccontare e commentare lo sviluppo di un attacco informatico condotto con il Red Team con cui collaboro (ovviamente in un contesto di Ethical Hacking) in cui abbiamo applicato e mescolato differenti tecniche di attacco così come avviene in un reale costesto “criminoso”. Si è trattata di una sessione dimostrativa che aveva lo scopo principale di portare all’attenzione del Blue Team, con cui ci siamo confrontati, come si sviluppi un attacco informatico in un contesto già in parte protetto da specifiche tecnologie. L’obiettivo di base concordato era l’accesso ai sistemi allo scopo di trafugare informazioni potenzialmente sensibili.

Ovviamente l’attività non è stata fine a se stesse ma è servita aiutare il team IT del committente ad accrescere le proprie conoscenze in relazione alle tecniche di difesa dagli attacchi informatici e ha messo alla luce possibili scoperture architetturali nonostante la presenza di eccellenti prodotti per la gestione della Cyber Security.

Sul tema e sulle strategie di attacco utilizzate abbiamo successivamente costruito un laboratorio recentemente presentato all’evento CisCon e che spero di riproporre prossimamente in altre occasioni.

## Analisi della superficie d’attacco

Come mi trovo spesso a ripetere (noto con piacere di non essere l’unico), il primo passo è studiare il nemico. Di solito è ciò che consiglio ai Blue Team riprendendo i precetti strategici di Sun Tzu (L’arte della Guerra) ed è esattamente ciò che fa l’attacker: conoscere il nostro nemico ci da un vantaggio strategico nei suoi confronti.

Il target selezionato era un’azienda di grandi dimensioni (più di 1000 dipendenti e diversi stabilimenti in Europa) che produce e commercializza vari prodotti in ambito industriale. Da una rapida analisi (OSint base) è emerso che il sito web e altri servizi di contorno (es: Mail Relay, MX secondario) erano implementati su piattaforma AWS.

> Nota: l’architettura di AWS (come molte altre architetture cloud-oriented) solitamente limita molte scelte dell’attacker in quanto è più probabile che certi processi di security management siano osservati rispetto a ciò che accade nelle private cloud.

L’analisi della zona DNS ha permesso di individuare un altro MX record a cui è associato un indirizzamento pubblico proveniente da una rete provider non associata a hoster/datacenter noti. Geolocalizzando l’IP la location risultava coincidere con l’indirizzo di una sede operativa italiana del target. Si è dedotto che almeno un sistema di posta elettronica fosse posizionato presso tale sede. Altre informazioni hanno rafforzato questa ipotesi: la dimensione della sede faceva pensare che vi fossero diversi dipendenti che vi lavorano, la stessa sede era citata sul sito istituzionale come un centro di produzione, le foto disponibili sul web evideziavano la presenza di uffici con personale amministrativo e commerciale. Diverse informazioni frammentate che andavano a comporre un puzzle molto più grande.

> Mescoliamo più tecniche contemporaneamente, via via che il perimetro diventa nitido diventa possibile utilizzare nuovi metodi di ricerca informazioni per dettagliare meglio il contesto.

Da un serie di ricerche tramite Social Network (LinkedIn e Twitter in questo caso) sono stati identificati i possibili dipendenti dell’azienda target impiegati fisicamente presso l’ipotetica sede. Lo si è dedotto semplicemente icrociando i dati disponibili sull’area di residenza dei soggetti e i dati raccolti hanno permesso di costruire una mappa dei ruoli, delle competenze e degli interessi degli utenti identificati… tutto grazie a dati pubblicamente disponibili e spesso forniti direttemente dall’utente al mondo.

> La scelta dei contatti con cui interagire è cruciale. In alcuni casi si scelgono figure “deboli”, facili da circuire o con ruoli non ben definiti. In altri contesti si cercano figure tecnicamente poco competenti, poco orientate al digitale, ma con ruoli manageriali.

Sono stati successivamente scelti tre dipendenti di tre distinte aree dell’azienda a cui inviare una email pulita (senza malware, semplice testo) con delle banali richieste di informazioni. Per le tre missive si è scelto di utilizzare tre false identità (inventate): un potenziale candidato, un potenziale cliente ed un potenziale fornitore. Anche sulla scelta delle identità sono state fatte delle considerazioni di merito sulla base di quanto dedotto dal destinatario del messaggio (es: età, sesso, stato sociale, competenze, ruolo, ecc); nella costruzione di una mossa di Social Engineering anche i dettagli più banali possono fare la differenza (tema da trattare in sede opportuna).

Dopo poche ore abbiamo ricevuto risposta a due dei tre messaggi: al candidato sono state fornite informazioni sul come rispondere alle offerte di lavoro tramite il sito istituzionale, al potenziale cliente sono stati forniti i riferimenti del commerciale che avrebbe potuto dar seguito alle richieste (email, telefono, ecc). Al di la dei dati comunicati dal personele dell’azienda, lo scambio di messaggi è stato utile per analizzare gli header delle email dove sono disponibili informazioni aggiuntive, tra cui:

- IP pubblico di provenienza (stessa subnet dell’ipotetica sede)
- IP privato, probabilmente della DMZ, del server di posta
- FQDN interno, quindi con domain name, del server di posta
- FQDN pubblico del relay di posta elettronica su cui rispondeva l’interfaccia Web di gestione di uno noto Spam - Firewall
- URL del servizio di Web Mail

L’analisi è proseguita ben oltre e molte altre informazioni sono state trovate sul target, alcune interessanti altre meno, ma tutto contribuisce a tratteggiare i contorni di un perimetro attaccabile. Le informazioni citate sono quelle che si sono rivelate poi particolarmente utili.

## Analisi dei sistemi (scan/enum)

Capito meglio chi abbiamo di fronte si può cominciare a farsi un’idea più dettagliata dei sistemi / processi che compongono il perimetro individuato, partendo ovviamente da ciò che — ad un occhio allenato — appare essere più promettente. L’attività di scanning prevede, sostranzialmente, di verificare nel dettaglio ogni singolo punto raggiungibile, sia esso l’IP di un sistema o un riferimento interno che presidia una determinata funzione.

Strategicamente è sembrato saggio concentrarci sui sistemi della sede e sul sito web aziendale in quanto le attività di Social Engineering ci hanno consentito di comprendere che dal sistema ospitante il sito internet istituzionale transitava il processo di recruitment. Nello specifico al candidato veniva chiesto di eseguire l’upload del proprio curriculum tramite un’applicazione “incorporata” nel sito web.

In relazione alla subnet pubblica della sede individuata si è potuto comprendere quali sistemi e quali applicazioni erano esposte verso internet per consentire ad utenti esterni di accedervi. Nelle varie attività esplorative è emerso che:

- i sistemi di posta elettronica erano ben presidiati grazie allo Spam Firewall
- i sistemi che esponevano servizi dalla rete verso il pubblico risultavano protetti da un apparato di - Firewalling in grado di intercettare alcuni tentativi ricognitivi di attacco (usando degli innocui Proof of Concept) basati sulle vulnerabilità note individuare grazie alle verifiche manuali sui sistemi
- gli scan massivi sono risultati inefficcaci
- il sito wordpress presentava diverse falle tra cui una vulnerabilità nota e abbastanza famosa (CVE-2016–10033) e di cui, senza troppa fatica, si possono trovare diversi p-o-c ed exploit
- il server sul quale era installato il sistema CMS wordpress risultava protetto da un firewall locale o da un qualche sistema che agiva una sorta di fail2ban in caso di richieste http non proprio ordinarie

## Un momento di riflessione

Le attività di raccolta delle informazioni possono produrre moli immense di dati anche per sistemi relativamente piccoli. E’ necessario predisporre dei momenti di revisione e cernita delle informazioni per cominciare a delineare una strategia offensiva. Il tema di fondo è comprendere qual’è il punto debole più semplice da sfruttare (ovvero che presenta delle maggiori probabilità di successo) e come può essere utilizzato a nostro vantaggio. Il concetto stesso di “punto debole” deve essere ben chiaro: ci riferiamo a sistemi/processi/persone che, per diverse ragioni, non sono correttamente presidiati e/o non presentano strumenti di controllo efficaci.

Avere una visione d’insieme del nostro target ci permette di pensare ad ampio spettro tenendo in considerazione tutte le inefficienze che le aziende hanno (nessuno è perfetto). Ognuno ha il suo metodo, io catalogo le informazioni in un database per andare poi a caccia di correlazioni, c’è chi disegna diagrammi, chi usa le mappe mentali, chi scrive tonnellate di appunti… il punto resta lo stesso: fare un bel “zoom out” di ciò che abbiamo trovato, riorganizzarlo e trovare uno “schema”.

Nel caso specifico abbiamo pensato che un vettore comodo potevano essere i curricula che in qualche modo passavano dal sito web aziendale ai PC dell’ufficio HR. Abbiamo quindi deciso di sviluppare un primo attacco al sito web con lo scopo di comprendere meglio il flusso dei dati. Contemporaneamente abbiamo risposto a diversi annunci candidando falsi profili con l’obiettivo di guadagnare un incontro presso la sede identificata (purtroppo senza esiti nei tempi sperati, le prime chiamate sono arrivate ad attività concluse).

## Strategia di attacco (1)

L’attaco al sito ha richiesto un po’ di fantasia in quanto il sistema di protezione limitava i nostri movimenti. L’ipotesi, poi in parte verificata, era che vi fosse un proxy a filtrare le richieste http e https verso la URL del sito (ad attività concluse il cliente ci ha rivelato che si trattava di un WAF, non di un proxy). Spesso la configurazioni di questi sistemi richiede che vengano specificate le URL da sottoporre ad analsi e dai dati raccolti in precedenza era emersa la presenza di più record DNS che puntavano al medesimo host:

Dalle scansioni eseguite vi era la certezza che il web server fosse un glorioso Apache (aggiornatissimo) su cui, tipicamente, vengono configurati i virtual host per “smistare” le richieste http alla DocumentRoot del sito desiderato.

Una tipica tecnica di elusione dei proxy consiste dell’utilizzare URL differenti per eseguire chiamate alla stessa DocumentRoot. In un server che ospita essenzialemnte un unico sito vengono spesso utilizzare delle configurazioni di default che generano l’effetto di visualizzare il sito web di default chiamando anche altre URL di terzo livello, per fare un esempio questa è la configurazione di default di molti ISP che offrono Web Hosting (es: provate a navigare su http://ftp.roccosicilia.it, verrete comunque “indirizzati” alla DocumentRoot del www.* e poi a questo blog). Chi configura i proxy viene, purtroppo, spesso male informato sulle URL che dovrà gestire e tipicamente la configurazione base comprende i nomi domini che si ritengono da proteggere… raramente verrà quindi configurato a livello proxy il dominio http://ftp.roccosicilia.it.

Infatti… il proxy (anzi WAF — Web Application Firewall) in oggetto veniva bypassato per l’URL ftp.nomedelsito.es a cui rispondeva il sito web del target. Questo ci ha consentito di caricare sul sistema una php-shell un po’ rielaborata (grazie alla vulnerabilità del CMS). Per evitare di lasciare troppe tracce, la shell utilizzata eseguiva una DNS query verso un sistema appositamente configurato, in cui veniva richiesto uno specifico record TXT contenente una stringa di testo. La stringa conteneva il comando da eseguire sul sistema dallo script php caricato. Per invocare lo script abbiamo utilizzato un altro stratagemma, sfruttando la stessa vulnerabilità abbiamo modificato il file wp-config.php (evidentemente dimenticato con i permessi in scrittura come credo nella maggior parte delle installazione di wordpress) affinché vi fosse in append la chiamata allo script php “malevolo”. L’effetto ottenuto è che ad ogni richiesta di navigazione legittima sul sito web, proveniente dai normali utenti, corrispendeva l’esecuzione del nostro script con l’innesco della query DNS e l’esecuzione locale di quanto specificato nel record TXT.

Questo incastro da malati di mente, elaborato mescolando tre diverse e famosissime tecniche di attacco, ci ha consentito di compromettere stabilmente il sistema eseguento solo una GET e due POST, da questo momento non abbiamo più avuto necessità di “toccare” il server per eseguire comandi specifici, è stato sufficiente variare la stringa del TXT record DNS. La posizione guadagnata ci ha permesso di analizzare il codice delle applicazioni ed i LOGs di Apache alla ricerca di attività proveninenti dalla rete della sede del target per capire che tipo di interazione ci fosse con il sito web. E’ emerso che alcuni dipendenti visionavo ed eseguivano il download dei curricula direttamente dal sito.

## Strategia di attacco (2)

Compreso il flusso dei dati inerenti i curricula si è valutato di utilizzare i file in oggetto come vettore d’attacco: tipicamente i file provenienti da una fonte fidata, come il sito web aziendale, vengono trattati con meno attenzione dagli utenti che ritengono di operare in un contesto fidato, protetto. Tale contesto porta l’utente ad abbassare la guardia e lasciare “qualche porta aperta” a potenziali attacker.

E’ stata quindi inviata un’altra candidatura ad una posizione aperta con relativo invio del curriculum tramite l’applicazione preposta nel formato accettato, il classico PDF. In un secondo momento il “curriculum” caricato è stato sostituito con un altro file (utilizzando la php-shell) camuffato con le “solite tecniche” e contenente un p-o-c di un malware innocuo che l’utente ha fatto poi detonare sul proprio PC.

L’evento è stato tracciato grazie al fatto che il “finto malware” era stato programmato per eseguire delle banali chiamate http verso uno specifico sistema (un VPS anonima raggiungibile direttamente via IP address) e ci ha dato l’opportunità di “estrarre” ulteriori informazioni di rete dal client (configurazione delle NIC, hostname). Collaudata la tecnica si è reiterato l’attacco più volte utilizzando diverse tipologie di malware e continuando a tracciare le “detonazioni” anche quando le componenti di codice malevolo venivano bloccate dal software di Endpoint Protection.

L’attacco ha portato i suoi frutti dopo diversi tentativi (ovvero dopo più finte candidature a diverse opportunità) con un PDF appositamente modificato per eseguire dei comandi PowerShell sulla macchina client a cui l’utente ha evidentenmente dato il consenso (di solito l’applicazione chiede l’autorizzazione a procedere).

## Bene, ma non troppo.

Queste duemila parole volevano avere principalmente due obiettivi

- dare un’idea di come ragiona l’attacker quando progetta un crimine informatico, non è un nemico da sottovalutare, è furbo, è resiliente, è insistente
- raccontare alcune tecniche semplici quanto efficaci che possono mettere in difficoltà anche realtà strutturate di grandi dimensioni e con team tecnici preparati

Verificare che un sistema di protezione come un Firewall, un WAF o un anti-malware funzionino bene quando serve, non è qualcosa da cui si può prescindere, siamo abituati ad affidarci completamente a questi sistemi ma raramente strutturiamo un processo di implementazione e soprattuto di gestione che sia poi all’altezza di un attacker motivato (economicamente). Raramente chi implementa questo tipo di soluzioni prende in considerazione quali tecniche esistano per eludere quel livello di sicurezza, banalmente perché si tratta di un altro mestiere… non tutti sono Hacker (etici), non tutti hanno respirato per decenni l’aria delle community del cyber-space dove astuzia, ingegno e stregoneria si fondono per formare nuove idee, nuove tecniche di attacco e difesa.