---
layout:     post
title:      "Individuazione delle vulnerabilità: attacco e difesa (prima parte)"
date:       2021-07-07 07:47:32 +0200
categories: [cyber-security, hacking, ita]
image:
---
La gestione delle vulnerabilità è ovviamente un tema ricorrente nelle organizzazione che devono governare infrastrutture IT/OT/IoT dal punto di vista della sicurezza cyber. Tutte le componenti, tecnologiche e non, di una organizzazione sono di fatto potenziali target per attacchi atti a raccogliere informazioni o compromettere i sistemi, cosa che, nei contesti di produzione, metto a rischio il funzionamento dell'organizzazione ed in alcuni casi il prodotto stesso (gli smart device sono l'esempio più ovvio).

Negli ultimi giorni ho avuto modo di illustrare alcuni step di attacco ad un collega “temporaneo” (abbiamo “a bordo” un ragazzo in alternanza scuola lavoro con una sincera passione per la tecnologia e la cyber security) e nelle chiacchierate è emerso un elemento che ho visto spesso anche in molti menbri degli uffici IT, compreso il management: di fronte ad un nutrito set di bug e vulnerabilità individuate tramite una o più fonti - non sempre grazie ad una metodologia di gestione del rilevamento delle stesse - si tende al disordine: l'assenza di una procedura definita per la gestione delle vulnerabilità lascia spazio alla propria interpretazione / percezione del rischio e l'organizzazione, se reagisce, lo fa in modo disorganizzato.

Inevitabilmente si tende a correre ai ripari per quanto riguarda le vulnerabilità che sembrano essere quelle più critiche a prescindere dal contesto. E’ vero che le vulnerabilità che consentono lo sviluppo di un attacco diretto sono estremamente pericolose in quanto più semplici — di solito — da sfruttare, ma la contestualizzazione della vulnerabilità può cambiarne sensibilmente il rischio correlato: esporre un sistema con evidenti vulnerabilità che consentono l'esecuzione di codice da remoto (Remote Code Execution) è ovviamente un elemento che rende il target estremamente appetibile, ma se il contesto presenta uno strumento di filtering in grado di riconoscere e bloccare i tentativi di exploiting (come IDP/IPS a livello firewall o un sistema di anti-exploiting a bordo del server) le probabilità che la vulnerabilità sia sfruttabile si riducono enormemente.

> Attenzione: si riducono, non svaniscono.

E' necessario poter correlare una vulnerabilità ad un asset e di quell'asset dobbiamo conoscere il contesto operativo e l'impatto sul business dell'organizzazione.

Dobbiamo necessariamente fare i conti con la realtà ed accettare che non tutte le organizzazioni hanno modo di costruire in tempi rapidi una mappa dei business impact legati agli asset. Inoltre, come accennato, non tutti dispongono di procedure di gestione delle vulnerabilità. Il modello che vorrei quindi proporre in questa mini serie - ed è anche la tesi discussa con il giovanissimo collega - è di approcciare la cosa per gradi mettendoci nella situazione peggiore ma spesso reale di non disporre di un database degli asset e delle loro caratteristiche.

> Nota: lo scenario non è in alcun modo da considerarsi sostitutivo alla predisposizione di un processo di asset management e relativi strumenti di gestione. L'obiettivo dell'articolo è ragionare assieme.

Come spesso scrivo nei post e racconto sia nei podcast che di persona, l'approccio dell'attacker è metodico e prevede la qualifica del target per comprendere se esiste una reale convenienza nello sferrare un attacco: costruire un'azione offensiva a scopo estorsione per colpire un piccolo studio professionale è molto diverso rispetto a ciò che comporta la progettazione dello stesso attacco con target una multi nazionale. Cambiano le economie dell'impresa (d'attacco), la possibile revenue, i tempi di realizzazione, ecc. Il modello prevede quindi l'analisi costo/benefici al fine di individuare un target appetibile.

Esistono diversi metodi per individuare target appetibili, uno di questi è legato alle tecnologie in uso dalle organizzazioni. Come avvenuto per recenti attacchi che hanno coinvolto migliaia di organizzazioni, l'attacker può utilizzare una falla nota presente in sistemi e piattaforme largamente utilizzate per costruire campagne di attacco anche massive ma con un vettore molto specifico.

In poche parole si tratta di analizzare le vulnerabilità note di tecnologie che il target utilizza a caccia della falla che potrebbe consentire un accesso ai sistemi in modo relativamente semplice. Ovviamente la quantità di vulnerabilità su cui eseguire questa analisi è enorme ed esistono database utilizzabili sia a fini offensivi che difensivi: di base dobbiamo acquisire un'informazione in relazione alla presenza di tecnologia, all'interno dell'organizzazione, che può essere sfruttata per un attacco informatico.

Esistono meravigliosi tools per verificare se parte del vostro asset presenta delle vulnerabilità critiche: se avete implementato una procedura di Patch Management e/o Vulnerability Management probabilmente subito dopo vi siete dotati di una soluzione software che vi aiuti a governare tale procedure; **se avete acquisito la soluzione software ma non avete una procedura ufficiale per la gestione di questi processi, avete un problema di governance e vi suggerisco di affrontarlo rapidamente per non vanificare l'investimento fatto.**

Visto che in questa sede parliamo di metodologia e non di tools (per i quali farete le vostre valutazioni) vediamo come possiamo entrare in possesso delle informazioni minime che ci servono per valutare se esiste un reale rischio per la sicurezza dell'organizzazione (se la vediamo dal punto di vista del team che deve difendere l'organizzazione) o una opportunità di business (se la vediamo dal punto di vista dell'attacker). Gli ingredienti sono:

- elenco asset / tecnologie in uso presso il target
- elenco vulnerabilità in riferimento alle tecnologie in uso
- contesto di utilizzo della tecnologia vulnerabile

Partiamo leggeri, non censiamo subito gli asset ma preoccupiamoci almeno delle tecnologie in suo. Esiste una convenzione che ci aiuta a definire, in modo univoco, la tecnologia che stiamo utilizzando: si chiama CPE (Common Platform Enumeration). Senza dilungarmi troppo (di seguito qualche link per documentarvi) si tratta di un metodo standard per identificare uno specifico vendor/prodotto/versione/ecc...

> Pagina dedicata di wikipedia: <https://en.wikipedia.org/wiki/Common_Platform_Enumeration>  
> Mitre specification: <https://cpe.mitre.org/specification/>

Un primo step potrebbe essere quindi quello di censire i CPE di riferimento per le tecnologie in uso nella nostra organizzazione: se utilizziamo una specifica versione di Microsoft Windows Vista, ma non ricordiamo esattamente l'update o altri parametri di dettaglio, potremmo annotare nella lista il CPE più generico:

> cpe:2.3:o:microsoft:windows_vista:6.0:*:*:*:*:*:*:*

Ovviamente questo elenco dovrà essere mantenuto aggiornato, quindi la versione *alpha* della procedura di inventory delle CPE dovrà prevedere che ogni nuova tecnologia introdotta/individuata nell'organizzazione dovrà essere censita in questa repository.

Una volta gestito questo patrimonio di informazioni (utile per fare una montagna di altre attività virtuose) nel modo più automatizzato ed efficiente possibile, possiamo andare ad analizzare un altro dataset interessante ben più noto dei CPE, ovvero i CVE: Common Vulnerability Enumeration. Esistono diversi siti ed organizzazioni che mettono a disposizione un database con l'aggregato delle CVE rilasciate per i vendor, c'è l'imbarazzo della scelta. Per questo piccolo esperimento utilizziamo una API di https://cve.circl.lu/ che consente di richiedere le ultime 30 CVE pubblicate in formato json.

<img src="{{ '/assets/images-posts/getcve.py_.png' | relative_url }}" alt="getcve.py_" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Esempio di lettura delle CVE tramite API

All'interno di una CVE trovate le informazioni sulla vulnerabilità compreso lo score e le CPE vulnerabili, ovvero l'elenco delle versioni software (talvolta in combinazione con specifici hardware) che presentano la vulnerabilità.

Siamo arrivati all'epilogo di questa prima parte di "avvio" dell'argomento che sintetizzo così: chiunque sia a conoscenza di una specifica applicazione in uso all'interno dell'organizzazione può identificare un potenziale set di vulnerabilità associate. Scopo di questa mini serie è discutere assieme le metodologie per rilevare e correggere le vulnerabilità prima che siano sfruttate. Nel prossimo post discutiamo una bozza di procedura e prendiamo in considerazione alcune tecniche di rilevamento (offensive e difensive) delle vulnerabilità.
