---
layout:     post
title:      "Cyber Security Test: post introduttivo"
date:       2024-11-24 15:00:00 +0100
categories: [cyber-security, hacking, ita]
image:      /assets/images-posts/cybersecurity-test-serie.png
---
Come accennato nel post in cui ho anticipato il progetto vorrei partire veramente dall'inizio: a cosa servono i security test?

Ho pensato di cogliere l'occasione per rivedere un po' di storia. La base storica dei test di sicurezza sono quelli che furono chiamanti "penetration test" nel 1967 durante la [Joint Computer Conference](https://en.wikipedia.org/wiki/Joint_Computer_Conference) che si tenne ad Atlantic City. In quel periodo diversi enti U.S.A. cominciavano ad utilizzare i sistemi informatici a disposizione attraverso le prime reti di comunicazione, solo un paio di anni dopo sarebbe nata la famosa ARPAnet. Nel corso della conferenza diversi esperti del mondo informatico attivi sia nel settore privato che all'interno della NSA e del DoD (Dipartimento della Difesa di cui NSA fa parte) discussero delle problematiche di sicurezza legate alle tecnologie informatiche emergenti utilizzando per la prima volta il termine "penetration" per descrivere l'azione aggirare i sistemi di sicurezza di un sistema per verificarne la vulnerabilità. In quel contesto è nato un modello di security test che negli anni è stata ampliato ma che già nella sua prima versione aveva una struttura che ci è sicuramente familiare:

- Trovare una vulnerabilità sfruttabile
- Progettare un attacco intorno a essa
- Testare l'attacco
- Impadronirsi di una linea in uso
- Eseguire l'attacco
- Sfruttare ingresso per recupero delle informazioni

Con queste fasi James P. Anderson descriveva un ipotetico attacco informatico nel 1971. Perché sono andato a riesumare fatti di 55 anni fa? Trovo interessante che in mezzo secolo i concetti di base che stanno dietro alla sicurezza offensiva sono rimasti invariati. Fu, a mio parere, una grande intuizione probabilmente figlia di uno specifico mindset, quello comune a tutte le strutture di "difesa" in cui la conoscenza delle capacità di attacco del nemico è parte integrante della strategia difensiva (Sun Tzu è sempre tra noi).

<img src="{{ '/assets/images-posts/image.png' | relative_url }}" alt="image" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Copertina del repporto Ware.

Il modello di base prevede quindi che per valutare la struttura di difesa dell'organizzazione devono essere condotti dei test in cui l'organizzazione viene attaccata da un team che riproduce il modello di comportamento di un attacker e questo concetto lo stiamo applicando, con le sue varie sfumature, da più di cinquant'anni. L'obiettivo è identificare le debolezze su cui lavorare per ridurre le possibilità di riuscita di un attacco. L'evoluzione, in questi anni, ha interessato gli scenari che possiamo prendere in considerazione, ma il mindset è rimasto invariato.

Nonostante le decadi passate dobbiamo prendere atto del fatto che il mindset in questione ha iniziato ad essere preso in seria considerazione in tempi relativamente recenti e spesso viene interpretato in modo pessimo: molte organizzazione fanno security test che non portano a nessun livelli di miglioramento della postura di sicurezza. Un paradosso.

## Scenari

Proviamo a fare un esercizio almeno noi che in questo ambito ci lavoriamo e/o facciamo ricerca: dimentichiamoci per un attimo tutte le "etichette" che il mercato della sicurezza informatica ha introdotto e ragioniamo sull'esigenza. Abbiamo un target che deve misurare la capacità di resistere ad eventuali attacchi informatici e, in base ai test che faremo, deve decidere che correttivi applicare.

La cosa più utile che possiamo fare è analizzare il contesto e definire un set di scenari di attacco che possano realisticamente interessare il target e su quelli, in base alle risorse a disposizione, definire i test da eseguire. Qualche esempio: se l'organizzazione in questione produce palline da ping-pong e le vende unicamente tramite e-commerce potremmo ipotizzare che due principali processi come la produzione e la vendita siano vitali per l'organizzazione. Ogni processo, per essere attuato, utilizza varie risorse: persone, sistemi informatici, servizi, ecc. Quello che dobbiamo fare è definire dei test di sicurezza che siano in grado di attaccare il processo, discuterli ed identificare quelli sui quali ha effettivamente senso fare dei test.

Ragionando in questo modo si evitano situazioni poco utili allo scopo finale in quanto si dovrebbero identificare test contestualizzati su processi effettivamente critici per il business. Ovvio che se avessimo budget infinito ci piacerebbe verificare ogni virgola, ma questa non è la realtà, le risorse sono sempre limitate ed i budget vanno gestiti. Quindi i test da fare dobbiamo sceglierli con cognizione di causa, ovvero ostinarsi a fare il compitino del Penetration Test annuale sul solito gruppetto di IP per poi mettere i risultati in un cassetto equivale a buttare i soldi... dobbiamo fare qualche passo in più.

Alcuni scenari sono sicuramente molto peculiari ma possiamo permetterci di fare delle generalizzazioni e definire una scaletta di massima. Resta indispensabile l'analisi del contesto, i temi di seguito esposti sono quindi puramente indicativi e mi sono utili per anticipare gli argomenti dei prossimi post.

---

Se i miei contenuti ti interessano e vuoi rimanere aggiornato su quello che pubblico e sugli approfondimenti puoi abbonarti al blog lasciando qui la tua email:

Riceverai una notifica ogni volta che pubblicherò un nuovo post riguardante la sicurezza informatica/

---

***Postura esterna***  
Un buon punto di inizio è la verifica di ciò che "comunichiamo" di noi stessi. Verificare il perimetro esterno che il threat actor è in grado di percepire ci consente di comprendere quanto ci stiamo esponendo a rischi. In questa analisi non possiamo metterci solo il classico elenco di *IP address* sei sistemi esposti, vanno considerati **i contenuti dei canali digitali e non** che utilizziamo, la **presenza social** dell'organizzazione e dei collaboratori, gli strumenti utilizzati, le **informazioni pubbliche**, eventuali **dati già raccolti dai threat actor** e molti altri elementi che possono aiutare un potenziale attacker a farsi un'idea di come funziona il business del suo potenziale target. Per come funziona il mercato del cyber crime, più informazioni esistono sul nostro conto e più aumenta la nostra appetibilità, soprattutto se le informazioni consentono di delineare delle possibili strategia di attacco.

Quello che emerge da questa indagine è materiale di studio per identificare eventuali attack path da sfruttare o approfondire. Potrebbe non emergere nulla di rilevante o potremmo scoprire di esporre troppo il fianco, lo sapremo una volta che avremo i dati per stabilirlo.  
Va inoltre considerata la possibilità di monitorare costantemente la nostra esposizione a nuove minacce. Se per alcuni elementi potrebbe essere complesso, per altri potremmo ipotizzare di implementare automatismi o adottare servizi dedicati allo scopo.

***Simulazioni di attacco***  
Una volta analizzato il contesto o parte di esso possiamo valutare di eseguire test specifici che ci consentano di verificare come reagisce l'organizzazione se interessata a specifiche azioni offensive. I test che possiamo implementare sono veramente molti: dal più tradizionale Penetration Test dell'applicazione web su cui poggia il business dell'azienda alla verifica degli strumenti di detection con attacchi mirati all'infrastruttura protetta dal Blue Team interno e/o da un SOC esterno.

Il modello che deve guidare la scelta dei test si basa sempre sull'esigenza di accertare che quanto implementato per la sicurezza delle informazioni stia funzionando e nella maggior parte dei casi questo porta a valutare diverse tipologie di test che potremmo dividere in tre macro aree:

- i test che toccano la sfera tecnologica
- i test che toccano la sfera umana
- i test che toccano i processi dell'organizzazione

Ragioniamo su un esempio. Supponiamo di aver attivato da ormai qualche mese il servizio SOC che si basa su sistemi implementati e gestiti in parte internamente ed in parte esternamente. Un grande classico sono gli strumenti di Detection come NDR ed EDR precedentemente adottati dall'organizzazione gestiti dal team interno e strumenti di aggregazione ed analisi come SIEM ed XDR gestiti dal SOC. È molto probabile, per non dire certo, che SOC e Blue Team debbano in qualche misura collaborare, saranno quindi state implementate specifiche procedure di gestione degli allarmi ed escalation.

Qualsiasi cosa sia stata fatta, ad un certo punto una prova su strada la dovremmo fare, quanto meno per non trovarci a dover affrontare una gara (security incident) con una macchina mai collaudata prima. Non che non si possa fare, intendiamoci, ma quanto meno dobbiamo essere consapevoli dei rischi enormi che abbiamo deciso di prenderci **e del paradosso di assumersi rischi aggiuntivi in uno mondo dove la riduzione del rischio è l'obiettivo supremo**.

Un test in cui un team esterno simuli azioni offensive verso un target protetto toccherebbe diverse sfere dell'organizzazione: sicuramente quella tecnologica e quella relativa alle procedure in campo, ma potremmo porre l'attenzione su diversi punti relativi alla sfera umana misurando la preparazione del team e le capacità di gestione dell'incident. Tutti elementi di cui è bene misurare la prestazione periodicamente ed agire di conseguenza migliorando ciò che non va.

***Addestramento***  
Per quanto sia auspicabile eseguire test specifici a tutti i livelli è molto probabile che non si possa arrivare a verifica tutto ne che si possano eseguire simulazioni ad ampio coinvolgimento. Anche su questo possiamo lavorare con delle attività che vanno un po' oltre la formazione, a me piace parlare di addestramento.

Un esempio molto utilizzato sono i tabletop exercise, una modalità di simulazione a tavolino di eventi critici come un grave fault tecnico o un data breach. Un punto a favore di questo tipo di attività è rappresentato dalla possibilità di coinvolgere anche figura dell'organizzazione che in caso di incident potrebbero essere chiamate a prendere decisioni importati o per gestire la comunicazione di crisi. Non sempre tali funzioni aziendali sono facili da coinvolgere nelle sessioni prettamente tecniche, mentre un tabletop exercise potrebbe essere una buona occasione per estendere la cultura della sicurezza informatica dell'organizzazione.

## Prossimi step

Vorrei procedere con una trattazione a "scenari". Nei prossimi post costruisco uno scenario realistico per discutere le attività che potremmo eseguire ed approfondirle tecnicamente una ad una.

Sono apprezzati feedback e suggerimenti.

---

Link utili:

- [Rapporto Ware](https://www.rand.org/pubs/reports/R609-1.html), inizialmente classificato e pubblicato nel 1979.
