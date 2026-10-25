---
layout:     post
title:      "Threat Hunting and Defending #2: concepts, framework, Threat Model (p1)"
date:       2026-07-16 14:00:00 +0200
categories: [cyber-security, ita, study-with-me]
image:      /assets/images-posts/gemini-threat-hunting.png
---
### Intro

Nel primo post di questa serie ho riportato soprattutto la teoria della disciplina e l'estrema sintesi è che il Threat Hunting è un processo strutturato utile ad identificare e mitigare minacce informatiche che i sistemi di detection non hanno potuto rilevare a causa di limiti del sistema (e di limiti ne possiamo trovare molti) o perché il Threat Actor utilizza tecniche sofisticate difficili da intercettare.

Le *operations* richiedono un'approccio strutturato, vanno considerate specifiche metodologie per eseguire un task di threat hunting. In questo post tocchiamo quindi un primo tema strutturale: le piattaforme ed i frameworks a cui possiamo fare riferimento.

### Concetti di base (della cyber security)

Se vi è capitato di vedere questo mio breve video alcuni elementi vi potrebbero sembrare familiari.

https://www.youtube.com/watch?v=-4dx1v9ILRY

L'assunto è abbastanza logico: se si vuole implementare un programma di Threat Hunting efficace è necessario sapere come i Threat Actor si muovo, sapere quali vettori utilizzano e conoscere obiettivi e motivazione. È inoltre necessario aderire ad una standard in relazione alla terminologia che si utilizza in questo ambito.

Nella documentazione ufficiale Cisco (ricordo che questi post sono i miei appunti di studio) viene fatto un bel recap di alcuni termini che ricorrono frequentemente.

Se trovi utili i contenuti che condivido e vuoi aiutarmi a migliorare il mio progetto di divulgazione iscriviti e abbonati [al mio Substack](https://roccosicilia.substack.com/subscribe).

**Threat Actor**: è il termine generico con cui si identifica l'entità che attacca.

**Attack Surface**: come si può intuire è la superfice attaccabile di un target come sistemi esposti, endpoint, applicazioni, servizi, ecc.

**Attack Vector**: è la metodologia che l'attaccante selezione per condurre un attacco.

**Tactics, Techniques, Procedures (TTP)**: possiamo sintetizzare questi tre elementi come la combinazione dei metodi, le strategie e le singole operazioni eseguite dal Threat Actor durante le operazioni offensive.

**Advanced Persistent Threat (ATP)**: sono gruppi che operano con tecniche sofisticate al fine di ottenere e mantenere un accesso ad una infrastruttura target senza essere individuati.

**Cyber Threat Intelligence (CTI)**: [vi lascio un video](https://www.youtube.com/watch?v=-1aya_O4PII) in cui ne ho parlato proprio nel contesto dell'hunting ed in questa occasione consideriamo le differenti categorie che possiamo definire.

- Strategic TI: considera aspetti di alto livello come i gruppi attualmente attivi ed i trend di attacco, la tipologia di target impattato, la situazione geopolitica, ...
- Tactical TI:

**Indicator Of Attack (IoA)**: sono gli elementi o i comportamenti che suggeriscono che un attacco sia in corso.

**Indocato Of Compromise (IoC)**: sono gli elementi riconoscibile associabili ad un tentativo di compromissione o ad una compromissione avvenuta.

### Pyramid of Pain

La "piramide del dolore" è un modo di rappresentare i gli elementi che ci consentono di intercettare un attacco con un ordine determinato dalla facilità di individuazione correlata ad basso impatto sulle operazioni dell'attaccante. Più si sale verso l'alto andando verso elementi difficili da tracciare e più aumentano le nostre possibilità di comprnedere e bloccare l'attacco e di conseguenza aumenta la difficoltà/dolore per l'attaccante.

<img src="{{ '/assets/images-posts/image-15.png' | relative_url }}" alt="image 15" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Ho preso in prestito una delle tante rappresentazioni pubblicate in giro. È evidente che utilizzare IoC come *hash* o *IP address* è relativamente semplice, ma questi elementi hanno una altissima variabilità: l'attaccante può rapidamente cambiare host e quindi IP mentre cambiare l'hash di un file senza modificarne il comportamento è un'operazione a costo zero.

Riconoscere e bloccare un tool o addirittura comprende la tecnica o la tattiva grazie alla correlazione degl eventi ci da un enorme vantaggio, ma non è una task semplice da portare a casa.

### Note di chiusura

Il capitolone dei framework è molto corposo, ho quindi deciso di dividerlo in parti. Nel prossimo post riporto gli appunti in merito alle piattaforme.

Questa serie di post fa parte del mio percordo di studio all'interno del team Security con cui collaboro in [NTS Italy](https://nts.eu/?utm_source=roccosicilia). Se ti interessano anche altri argomenti [contattami direttamente](https://www.linkedin.com/in/roccosicilia/).
