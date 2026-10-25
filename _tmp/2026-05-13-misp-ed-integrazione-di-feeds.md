---
layout:     post
title:      "MISP how-to: integrazione di feeds"
date:       2026-05-13 15:00:00 +0200
categories: [cyber-security, hacking, ita]
image:      /assets/images-posts/misp-screen.png
---
### Premessa

Questo post riprende una serie di contenuti che avevo in roadmap sul tema MISP e vorrei farlo discutendo alcuni *use case* su cui sto lavorando. Come alcuni sanno tempo fa ho iniziato a lavorare ad un progetto community per promuovere attività di Cyber Threat Intelligence e con l'occasione abbiamo messo online una istanza MISP disponibile ai ricercatori / appassionati che si vogliono contribuire al progetto di condivisione e divulgazione. In questi mesi ho avuto modo di sperimentare varie applicazioni ed integrazioni e ho maturato alcune idee che vorrei provare a strutturare.

Ovviamente quale occasione migliore per raccontarle ed illustrarle :-)

### MISP e feeds

Dobbiamo considerare un "problema" strutturale: MISP è una struttura che consente di raccogliere eventi rilevanti in ambito Threat Intelligence e documentarli con diversi dettagli tecnici ed analitici, i feeds di IoC hanno solitamente una struttura completamente diversa e molto spesso sono collections di IoC più o meno documentate. Di fatto la struttura di MISP e la struttura di un tipico IoC feed sono molto differenti.

Se trovi utili i contenuti che condiviso e vuoi restare aggiornato puoi sostenere il mio progetto di divulgazione [iscrivendoti al mio Substack](https://roccosicilia.substack.com/subscribe). Per gli abbonati metto a disposizione articoli e video di approfondimento.

Allora perché abbiamo la possibilità integrare i feeds in MISP? Dobbiamo tenere a mente che MISP è uno strumento di raccolta e condivisione delle informazioni e possiamo vederlo come un'area di "transito" di diverse tipologie di dati, tra cui anche *raw IoC* da utilizzare in processi di arricchimento, analisi, detection, ecc. Se l'evento è una struttura utile come output di un'analisi il feed lo possiamo vedere come dato aggregato utile per mettere a disposizione dell'analista informazioni di dettaglio circa un determinato IoC.

Facciamo un esempio: durante l'analisi di un threat capita di individuare diversi tipi di artefatti o informazioni come files, IP, domini, ecc. Quello che documentiamo potrebbe essere un elemento rilevante e caratteristico del threat come no. La presenza di uno di questi elementi in un feed (correlazione) potrebbe permetterci di classificare meglio il dato che stiamo analizzando. Quanto descritto è l'output di un processo alla cui base c'è la disponibilità delle informazioni.

### Collecting ed organizzazione dei feeds

Come detto **è fondamentale avere i dati a disposizione** ed averli tutti su una piattaforma ci permette di avvalerci di alcune funzionalità comode di MISP, nel contesti specifico la funzionalità che torna particolarmente comoda è la possibilità di correlare informazioni.

Facciamo un esempio: se durante la nostra indagine su una email di phishing individuiamo un link ad un sito potenzialmente malevolo, avremo l'esigenza di eseguire una verifica tramite uno strumento di terze parti.

<img src="{{ '/assets/images-posts/image-1.png' | relative_url }}" alt="image 1" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Tutto fattibilissimo, ma se nella nostra istanza MISP integriamo il feeds di ThreatFox possiamo ottenere lo stesso risultato senza spostarci su una piattaforma di terze parti.

Operativamente quello che avviene è che alla creazione dell'evento, quando inseriremo l'attributo relativo al dominio sospetto, se il dato è presente in un altro evento (es: la collection di ThreatFox che abbiamo integrato nella piattaforma), apparirà un riferimento ad uno o più eventi nella colonna "Related Events".

<img src="{{ '/assets/images-posts/image-2.png' | relative_url }}" alt="image 2" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Questo indica che il dato è presente in un'altra analisi (e quindi lo abbiamo già incontrato ed analizzato) o è presente in un feed, come in questo caso, e potremo approfondire sulla base delle analisi disponibili pubblicamente.

Una buona pratica è quindi arricchire la propria piattaforma MISP con feeds di terze parti valutando bene l'organizzazione di questi dati. Solitamente si opta per la creazione di un evento con i dati del giorno: sulla mia istanza l'evento "ThreatFox IOCs for 2026-05-12" contiene tutti gli IoC pubblicati da ThreatFox il 12 maggio 2026, dati che integro quotidianamente.

### Integrazione dei feeds

MISP ha una funzionalità di integrazione per aggiungere i dati provenienti da vari feeds. La funzione è disponibile nel menu ***Sync Actions \ Feeds*** e sostanzialmente consente di aggiungere sorgenti di cui si dispone di un'accesso. Ovviamente questa funzionalità è utile per tutte le sorgenti che si possono integrare con MISP, qualora questo non fosse possibile nativamente possiamo sempre avvalerci delle API disponibili: MISP consente di creare eventi ed attributi tramite API, è quindi sempre possibile "leggere" un feed, elaborarlo e trasformarlo in un evento MISP.

Ho in programma un video/live sulle integrazioni: mettere le mani sui sistemi è sempre utile per vedere cosa si può fare nel mondo vero. Suggerisco di seguirmi su [**Substack**](https://roccosicilia.substack.com/) per restare aggiornati sul programma delle live.
