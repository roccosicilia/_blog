---
layout:     post
title:      "Cloaking, SEO e minacce via web."
date:       2026-06-26 10:32:41 +0200
categories: [cyber-security, hacking, ita]
image:
---
Altra tecnica datata ma molto efficace in determinati contesti: il cloaking. Va detto, per prima cosa, che il cloaking è una tecnica considerata poco etica nel mondo della SEO. Consiste nel verificare la provenienza dell'utente per decidere che contenuti presentare, spesso era usata per dare in pasto ai BOT dei motori di ricerca contenuti utili a livello SEO mentre gli utenti venivano reindirizzati sui contenuti effettivi del sito, non necessariamente coerenti con l'indicizzazione. Il trucco funzionava e probabilmente funziona tutt'ora in quanto gli utenti tendono a fidarsi dei risultati del motore di ricerca.

Supponiamo ora di essere un threat actor che deve convincere gli utenti ad atterrare sulla propria pagina truffaldina, ad esempio una pagina usata per distribuire un payload (rif. a [questa analisi](https://roccosicilia.com/2026/02/17/analisi-di-un-c2-per-osx/) di qualche settimana fa).

Se trovi utili i contenuti che condiviso e vuoi restare aggiornato puoi sostenere il mio progetto di divulgazione [iscrivendoti al mio Substack](https://roccosicilia.substack.com/subscribe). Per gli abbonati metto a disposizione articoli e video di approfondimento.

La tecnica potrebbe essere usata per portare in indicizzazione una pagina di transito in grado di comparire con specifiche ricerche. I BOT indicizzerebbero correttamente la pagina e potrei anche fare in modo di presentare un contenuto "di servizio" sia ai BOT che agli utenti ed eventuali strumenti di analisi che tentino di accedere direttamente alla pagina. Se l'accesso arriva invece da un browser ed ha come referer un motore di ricerca posso ipotizzare che chi sta accedendo è a tutti gli effetti un utente che ha trovato il link nel corso di una ricerca, la potenziale vittima della mia pagina malevola.

## Esempio reale

In questi giorni ho preparato le slide di una presentazione tecnica dove introduco OSInt e le Google Dorks. Ero intento a preparare degli esempi molto semplici, dei grandi classici come la ricerca di webcam online, cosa che per qualche ragione piace sempre, e stavo utilizzando la chiave di ricerca:

```
intitle:"Live View / - AXIS"
```

Google mi propone il solito listone di risultati ma alcuni mi portano ad una pagina a me ben nota (vedi immagine). Si tratta di una pagina appositamente creata da un bad actor per indurre l'utente ad eseguire un payload localmente sulla sua macchina, payload che avvia un processo di comunicazione con un C2.

<img src="{{ '/assets/images-posts/image-11.png' | relative_url }}" alt="image 11" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Mi è sembrato strano che Google portasse in indicizzazione un contenuto così diverso dalla chiave di ricerca, inoltre si tratta di url con reputazione molto bassa. Il trucco che è stato utilizzato è il cloaking: il link indicizzato da google porta ad una applicazione che si occupa di verificare i dettagli della chiamata HTTP e del browser in modo da capire se chi sta accedendo alla pagina è una potenziale vittima o un BOT.

Le informazioni raccolte vengono poi inviate alla stessa pagina con una chiamata POST, se le condizioni sono quelle di un browser con determinate caratteristiche ed il referer è il motore di ricerca, l'applicazione risponde con un redirect al sito malevolo (vedi screen di Burp). Altrimenti si atterra su una pagina di servizio che appare assolutamente innocua.

<img src="{{ '/assets/images-posts/image-12.png' | relative_url }}" alt="image 12" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Un bel trucchetto per nascondere dietro una ricerca su google un fileless malware custom per il sistema operativo che accede alla pagina.

## Le finezze che ho notato

La prima cosa interessante che ho notato, ma che mi ha anche fatto dubitare, è il comportamento diverso del link accedendovi direttamente. Accedendo direttamente con un browser come Firefox il contenuto presentato non è il redirect ma una pagina apparentemente statica:

```
URL: http://18.234.112.52/grassy-lookout/mending-sanctuary/live-view-axis-fix-link
```

<img src="{{ '/assets/images-posts/image-13.png' | relative_url }}" alt="image 13" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Altra scelta interessante è l'indicizzazione dell'host con il sui IP e non con una URL, cosa assolutamente normale quando si tratta di webcam pubblicata "malamente" ed è anche il motivo per il quale ho inizialmente pensato che il risultato fosse coerente con la ricerca:

<img src="{{ '/assets/images-posts/image-14.png' | relative_url }}" alt="image 14" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Non male come tecnica, nella sua semplicità è sicuramente funzionale e non è banale spiegare agli utenti che devono stare attenti anche ai risultati di un motore di ricerca che sembrano assolutamente affidabili.
