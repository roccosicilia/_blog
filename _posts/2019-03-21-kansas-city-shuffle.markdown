---
layout: post
title:  "Kansas City shuffle."
date:   2019-03-21 09:00:00 +0200
categories: [cyber-security]
image:  "/assets/images-posts/kansas-city-shuffle.png"
---
Esiste un GAP, in costante variazione, tra chi sviluppa ed implementa tecnologie e strategie di protezione dagli attacchi informatici e le tecniche di attacco utilizzate dai Cyber Criminali. La storia vede i primi mettere delle “pezze” alle novità che i secondi “propongono”; la conseguenza diretta è che il settore della Cyber Security evolve in relazione — ed in ritardo — rispetto al settore dell’Offensive Security. Per farla breve: prima viene inventata una nuova tecnica di attacco e solo quando viene rilevata e compresa si riesce a sviluppare lo “strumento” di difesa. Inizialmente è spesso un’azione correttiva con validità temporanea per mitigare il danno ed in un secondo momento si provvede ad integrare il nuovo “scudo” in modo strutturato.

Sia come ricercatore che come Ethical Hacker il mio lavoro si svolge “al di là della barricata”, ovvero dal punto di vista di chi progetta l’attacco a partire dall’intuizione iniziale fino all’esecuzione realistica in una sessione offensiva, ciò che viene volgarmente chiamato “Penetration Testing” (fatto a regola d’arte, non martellando con un maglio come vedo spesso fare). Da questa posizione il GAP culturale a cui facevo cenno è ben visibile e, soprattutto, facilmente sfruttabile per me quanto per i Cyber Criminali.

Riflettendo su alcune tecniche di attacco che ho avuto modo di provare su campo — ovviamente sempre in contesti di Ethical Hacking — mi è venuta in mente una battuta di un film di qualche anno fa in cui si faceva cenno alla “ mossa Kansas City “ come metafora dell’inganno definitivo in cui “tu guardi a destra e io vado a sinistra”.

A livello di strategie di difesa molti stanno “guardando a destra” introducendo meccanismi di protezione laddove ritengono di poter essere attaccati. Intanto i Cyber Criminali “vanno a sinistra” con tecniche e vettori di cui molti non conoscono l’esistenza.

Questa tendenza unita alla presunzione di aver giá implementato una strategia di difesa senza peró averla messa alla prova puó portare ad una sola conclusione ovvia: attacchi a segno in aumento in tutti i settori.

Due esempi al volo che sto approfondendo a livello di ricerca e che ritengo estremamente efficaci:

- USB Rubber Ducky: assomiglia in tutto ad un pen-drive ma in realtà è una USB keyboard programmabile che, una volta inserita in un End Point, esegue molto rapidamente una serie di comandi prestabiliti impartendoli direttamente dalla “tastiera” del sistema vittima (acquistabile per 50 $)
- Radio KeyLogging: molte Wireless Keyboard lavorano in radio frequenza a 2.4 GHz tramite un canale di trasmissione (reggetevi) non protetto… le digitazioni sono quindi trasmesse in chiaro e facilmente intercettabili in un raggio di 10–20 metri con strumenti ordinari e fino a 100 metri con strumenti di aplificazione (acquistabili per 40 $)

Discutiamone. Come le gestiamo queste tecniche di attacco? Ne avete mai sentito parlare?