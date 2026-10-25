---
layout:     post
title:      "Cyber Security Test: conoscere il target (parte 1b)"
date:       2025-01-06 13:00:00 +0100
categories: [cyber-security, hacking, ita]
image:      /assets/images-posts/cybersecurity-test-serie.png
---
Ho deciso di estendere la "parte 1" prima di passare oltre per fare un piccolo focus sull'analisi del sito web istituzionale del target (e dei siti che troveremo). Nelle fasi iniziali del test ogni informazione è preziosa (mi ripeto, lo so) e le fonti vanno spremute bene.

Oltre ai contenuti dei siti web possiamo analizzare ciò che siamo in grado leggere lato client: la struttura HTML, file e componenti di servizio, link, media. Andare a caccia di informazioni in siti di una certa dimensione potrebbe essere difficoltoso se non impossibile, una possibile soluzione è il download di tutte le componenti "statiche" del sito per analizzarle con calma e soprattutto con l'aiuto della CLI.

L'operazione non è esattamente "silenziosa" considerando che ogni nostra richiesta HTTP verrà registrata nei logs del webserver. Inoltre tentare di nascondere la nostra provenienza tramite una VPN o la rete Tor potrebbe peggiorare le cose: ad una eventuale analisi dei logs è molto probabile che gli exit node della rete Tor sia facilmente riconoscibili e questo potrebbe insospettire il target. Si tratta di una precauzione che ha senso solo in contesti di simulazione di attacco, modello che viene sempre più applicato ed apprezzato dalle aziende che chiedono di eseguire test di sicurezza.

Un tool utile ad una rapida analisi delle informazioni legate al dominio web ed alle tecnologie usate dall'host è netcraft. Dalla risorsa <https://sitereport.netcraft.com> è possibile eseguire una scansione di un sito ed ottenere un report relativo a diversi aspetti tecnici. Come sempre un esempio è molto più utile delle parole.

<img src="{{ '/assets/images-posts/image-5.png' | relative_url }}" alt="image 5" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Esempio da roccosicilia.com

Tra le informazioni disponibili c'è il rilevamento della tecnologia usata per le componenti server-side e client-side, viene inoltre verificato se è possibile stabilire il CMS in uso. Vengono inoltre raccolte le informazioni a livello host IP e provider.

<img src="{{ '/assets/images-posts/image-6.png' | relative_url }}" alt="image 6" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

DNS query

Questi ultimi dati ci prendiamo in considerazione in modo dettagliato nel prossimo post, in concetto di base è analizzare il sito web in ogni sua parte in modo da avere una completa panoramica di quanto esposto da questa singola applicazione.

---

La serie di post e [video](https://www.patreon.com/c/roccosicilia/posts?filters%5Btag%5D=cyber+security+test) sui security test prenderà in esame diversi aspetti legati al mondo del Penetration Testing. Per rimanere aggiornato sui prossimi post puoi iscriverti al blog:

---

Nel prossimo post terminiamo la parte di raccolta informazioni passiva con l'obiettivo, già dichiarato, di ottenere un elenco di hosts che si possono riferire al nostro target.
