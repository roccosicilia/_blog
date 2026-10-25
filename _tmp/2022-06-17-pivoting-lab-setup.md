---
layout:     post
title:      "Pivoting: lab setup"
date:       2022-06-17 09:30:27 +0200
categories: [cyber-security, hacking, ita]
image:
---
Osservare alcune specifiche tecniche di attacco consente di comprendere meglio quanto possa entrare in profondità un attacker. Uno scenario abbastanza tipico che mi capita di analizzare è relativo alla presenza di reti relativamente "piatte", ovvero segmentate a livello di subnet/vlan ma talvolta non segregate e lasciate molto libere di comunicare tra loro.

Il disegno di una rete impatta notevolmente sulle opzioni che un attacker ha a disposizione una volta individuata una breccia. Lasciandoci alle spalle l'irrazionale pensiero che "a noi non capiterà mai", una strategia di difesa efficace deve tener conto della possibilità che un attacco abbia successo con la conseguenza di trovarci con elementi interni della rete compromessi almeno in parte. Esistono decine di scenari esplorabili in tal senso: in generale nel momento in cui un attacker dovesse guadagnare una posizione all'interno della rete, non sapendo come la rete è strutturata, andrebbe a caccia di nuove informazioni con l'obiettivo di utilizzare il sistema compromesso come "base" per altre azioni.

Il pivoting è una delle classiche tecniche per entrare ancor più in profondità nella rete target in quanto consente all'attacker, **se ve ne sono le condizioni**, di passare da una rete all'altra estendendo il suo raggio d'azione. Ho volutamente evidenziato l'esigenza di specifiche condizioni perché questo avvenga in quanto, di fatto, un buon disegno della rete ed opportuni controlli possono limitare enormemente l'attività dell'ospite indesiderato.

A me piace mescolare, quindi nella live di questa sera tiriamo su un piccolo lab per provare la tecnica citata per vedere come un attacker potrebbe comportarsi e poi analizziamo le possibili azioni correttive da adottare per limitare l'azione dell'attacker.  
  
Come di consueto alle 21:30 sul mio canale Twitch: <https://www.twitch.tv/roccosicilia>.
