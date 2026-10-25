---
layout: post
title:  "La strategia non è un prodotto."
date:   2020-01-14 09:00:00 +0200
categories: [cyber-security]
imege:
---

Una strategia di difesa è qualcosa che va oltre la mera protezione. Difendersi deve comprendere la gestione di situazioni critiche anche e soprattutto nel momento in cui si verifica il peggio, ovvero il superamento delle barriere protettive.

Il modello comportamentale più comune prende molto in considerazione il tema protezione. In questo scenario vediamo le aziende dotarsi (saggiamente) di sistemi, soluzioni e procedure atte a contrastare una serie di minacce che, per ovvie ragioni, sono quelle note… sperando di conoscerle tutte.

Questo modello presenta palesi ed ataviche debolezze: metodi e tecnologie di attacco si evolvono costantemente e molto più velocemente delle tecnologie di protezione che, storicamente, hanno sempre “rincorso” il problema. E’ evidente che per difendersi è necessario un approccio un po’ più strutturato: non basta erigere barriere, dobbiamo anche comprendere a cosa siamo vulnerabili e quali strategie possiamo adottare per migliorare il nostro livello di sicurezza e gestire il nostro livello di insicurezza.

Il tema ha dei risvolti terribilmente pratici, alcuni dei quali vengono affrontati quotidianamente da chi, come me, si occupa di sicurezza informatica. E’ preoccupante la frequenza con la quale aziende anche molto strutturate si trovano ad dover affrontare security incident senza avere un piano. Purtroppo si sta facendo esclusivo affidamento su tecnologie che, pur essendo indispensabili, non sono assolutamente sufficienti a garantire la sicurezza informatica di un sistema. So che sono anni che insisto su questa tesi, ma è effettivamente così, ed è ormai ormai fin troppo evidente.

Anche il mio team, nelle sessioni di attacco simulato, utilizza tecniche ideate appositamente per aggirare i sistemi di protezione.

<img src="{{ '/assets/images-posts/la-strategia-non-e-un-prodotto.webp' | relative_url }}" alt="strategia" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Ad esempio, abbiamo sviluppato un prototipo di malware, ovviamente innocuo, che sfrutta funzioni base e del tutto consentite di Powershell per crittografare dei file ed inviare la chiave all’esterno del sistema. Questo tipo di attacco, veicolabile facilmente con l’inganno o utilizzando tecniche fileless come una USB Rubber Ducky, è tanto semplice quanto pericoloso. Al momento non viene intercettato neanche da sistemi anti-malware molto sofisticati, per motivi banalissimi:

Se eseguito come script la sequenza di eventi è estremamente semplice e poco invasiva, il comportamento è ridotto ai minimi termini proprio per non “insospettire” i sistemi di behaviour analysis.
Se eseguito in modalità fileless non c’è niente da analizzare se non un evento sicuramente sospetto di un utente che lancia una serie di comandi dalla propria CLI Powershell.
L’esempio di malware che abbiamo realizzato, di cui parlerò in un post dedicato, è stato sviluppato appositamente per restare sotto traccia eseguendo pochissime operazioni e non andando a toccare componenti core del sistema operativo.

Nonostante sia qualcosa che in un certo senso non fa parte del nostro modo ordinario di ragionare, è necessario valutare strategie che prendano in cosiderazione i passi da fare in caso di security incident. Dobbiamo abituarci a rispondere a domande scomode come “cosa facciamo in caso di Data Breach?” o “come ci muoviamo in caso di una infezione da crypto-malware?”.
Essere preparati a questo tipo di situazioni ed avere a disposizione team e consulenti addestrati ad operare in questi contesti può fare tutta la differenza.