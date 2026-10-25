---
layout:     post
title:      "Quando serve davvero la process injection?"
date:       2026-08-28 17:24:24 +0200
categories: [hacking, ita]
image:
---
Ormai è un po' che mi interesso alle tecniche di attacco basate su fileless malware, sia per rendere i miei security test più realistici sia, lo ammetto, perché il tema mi affascina molto. In particolare mi sono concentrato inizialmente sulla possibilità di eseguire porzioni di script tramite un primo stage PowerShell. Quello che ho notato durante i miei test è che, utilizzando esclusivamente strumenti e runtime già presenti sull'endpoint come PowerShell/.NET, Python e altri strumenti nativi, riesco a coprire una parte piuttosto ampia delle attività che mi interessano.

Discutendo di questo con la community, mi è stato però fatto notare che, negli stage successivi di molte intrusion chain, diventa abbastanza frequente l'utilizzo di codice compilato e di tecniche di process injection. Le motivazioni sono diverse: sfruttare il contesto di sicurezza di un altro processo, accedere a risorse disponibili all'interno di quel contesto oppure modificare il modo in cui l'attività viene osservata dagli strumenti di sicurezza. Su questo tema sto ragionando molto, anche a "voce alta" come in questo post.

Nelle mie simulazioni, quando provo ad interagire con processi di sistema o ad alterarne il comportamento, gli EDR tendono ad essere piuttosto reattivi. Al contrario, quando mantengo l'esecuzione all'interno del processo PowerShell che ho già avviato e utilizzo funzionalità dell'host attraverso .NET o altri runtime, vedo comunque molta telemetria, ma in alcuni casi la correlazione degli eventi sembra essere meno efficace. Non intendo dire che PowerShell sia "invisibile" agli EDR. La telemetria viene comunque raccolta. La mia osservazione è semplicemente che, in alcuni scenari, sembra esserci una differenza nella capacità di correlare quello che sto facendo.

Le attività che simulo sono relativamente semplici: reconnaissance, collection, exfiltration e lateral movement. Per questo, almeno nella mia esperienza, non ho ancora incontrato un vero requisito operativo che mi obblighi ad utilizzare process injection.

Da qui la mia domanda per chi è più esperto di me.

Quali attività concrete di post-exploitation diventano possibili, o significativamente più semplici, grazie alla process injection rispetto all'utilizzo di un processo già compromesso e degli strumenti/runtime nativi disponibili sull'host?

Non mi interessa tanto capire quali siano le tecniche di injection in sé (quelle sono note e ben documentate), quanto piuttosto quale sia il loro vero vantaggio operativo.

La mia impressione, che potrebbe tranquillamente essere sbagliata, è che in molti casi la process injection non aggiunga vere e proprie capacità all'attaccante, ma cambi principalmente il contesto in cui il codice viene eseguito. Privilegi, token, accesso a determinate risorse o processi e, soprattutto, il modo in cui l'attività viene osservata dagli strumenti di sicurezza. In altre parole, mi chiedo se il valore della process injection sia spesso più legato al contesto di esecuzione che alle capacità che permette di ottenere.

Se ho già un processo sotto il mio controllo e posso utilizzare le API e i runtime disponibili sull'endpoint, cosa mi sto perdendo?

È probabilmente una domanda influenzata dal tipo di attività che simulo e dai casi d'uso che ho incontrato finora, quindi sono curioso di capire dove questa interpretazione smette di essere valida.

PS: ho fatto la stessa riflessione [su HN](https://news.ycombinator.com/item?id=49479767) sperando che qualcuno di forte mi dia il suo punto di vista e tutto nasce da una chiacchierata sul mio server Discord.
