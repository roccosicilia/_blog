---
layout:     post
title:      "API ed info-sec"
date:       2025-11-30 21:00:00 +0100
categories: [cyber-security, ita, vlog-podcast]
image:
---
Sono impegnato, in questo periodo, nello studio per una certificazione Cisco in ambito Cyber Defense (i motivi li ho spiegati qui) e ho trovato molto interessante il fatto che un'intero capitolo sia stato dedicato al tema API ed integrazioni.

È, ancora una volta, una questione di approccio: chi da per scontato che tutto ciò che viene implemento per la gestione della difesa digitale sia in grado - magicamente - di integrarsi, scambiarsi dati, interagire con il resto dell'infrastruttura e dei processi probabilmente non ha un'idea chiara dell'info sec. e forse neanche dell'IT.

Se soluzioni software sono qualcosa di abilitante che, oltre ad aver bisogno di una gestione dedicata, devono anche essere inserite in un contesto e devono essere messe in grado di dialogare con ciò che esiste in rete.

Un modo è "sporcarsi le mani" ed utilizzare le API che mettono a disposizione. Per dirla in modo molto diretto dovete imparare a scrivere un po' di codice che vi consenta di mettere in comunicazione due soluzioni.

Nella maggio parte dei casi di tratta di leggere delle informazioni da una o più fonti, elaborarle ed eseguire un'azione. Non è un caso che nella maggior parte dei casi le API che vi vengono messere a disposizione vi consentono di leggere e scrivere dati e attivare dei processi.

Supponiamo di dover generare un allarme basato su una condizione che dipende dal dato che possiamo leggere su due sistemi. Utilizzando le API potremmo leggere periodicamente le informazioni che ci servono dalle due sorgenti in questione (es: una WabApp esterna ed il log di un nostro sistema interno), utilizzare questi dati per verificare se si è verificata la condizione che stiamo cercando e, quando si presenta, chiedere al sistema di monitoraggio, tramite una sua API, di generare un alert specifico.

Ho [proposto il tema su LinkedIn](https://www.linkedin.com/feed/update/urn:li:activity:7399857446661423106/) ma forse è un po' complesso o troppo noioso per la piattaforma :-) ho quindi pensato di rilaciare anche qui e con un VLOG:

https://youtu.be/PgZdoUeVsig

API e info sec.: le stai usando?

---

Registrati al blog per rimanere sempre aggiornato sulle novità:
