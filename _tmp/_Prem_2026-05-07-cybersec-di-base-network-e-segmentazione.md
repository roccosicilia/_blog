---
layout:     post
title:      "CyberSec di base: network e segmentazione"
date:       2026-05-07 09:00:00 +0200
categories: [cyber-security, ita]
image:      /assets/images-posts/monitor-cybersec.png
---
### Introduzione

Tutti i sistemi che utilizziamo, in un modo o nell’altro, sono interconnessi e l’infrastruttura di rete, per chi si occupa di sicurezza informatica, non è solo lo strumento per consentire ai sistemi di dialogare ma è anche quel complesso sistema di “tubi” da cui transitano i dati da proteggere e le tracce di possibili minacce. Se per il mondo IT la rete è uno strumento per lo più funzionale alla comunicazione, per il mondo SEC la via d’accesso ai sistemi che dovremmo proteggere.

Non possiamo scollegarli, non possiamo bloccare in modo indiscriminato il traffico e dobbiamo salvaguardarne disponibilità e prestazioni, il tutto rendendo sicuro dell’accesso. Non è una cosa banale.

### Un po’ di basi sul design

Facciamo un *ripassone* assieme usando uno dei miei schemi (brutti) d’esempio :-) che vi racconto nel video che allego.

https://youtu.be/45pJ5DTnVVw

Prendiamo in esame la più classica delle reti in cui abbiamo un segmento (una VLAN) dedicata al mondo client (a destra), un segmento dedicato al mondo server (a sinistra) ed un segmento dedicato alla parte esterna della rete che nel nostro caso è una connettività internet. In questo primo esempio non tocchiamo il tema DMZ e supponiamo di dover gestire una rete i cui servizi sono disponibili solo agli utenti interni.

Sul piano funzionale quello che ci aspettiamo è che:

- gli ambienti client siano in grado di navigare
- gli ambienti client siano in grado di accedere ai servizi della rete server
- i sistemi server siano in grado di accedere ai servizi esterni, qualora sia necessario

Sul piano della sicurezza quello che dobbiamo garantire è che:

- i sistemi server siano protetti da eventuali compromissioni della rete client e viceversa
- i sistemi della rete siano protetti da eventuali compromissioni dall’esterno

Per ottenere questi semplici risultati dobbiamo fare un bel po’ di cose su quel firewall. L’accesso alle risorse deve essere garantito dalle funzionalità di routing tra le reti e per l’accesso ad internet è anche necessario applicare un NAT al traffico in uscita in modo da consentire ai sistemi di presentarsi alla rete pubblica con l’indirizzo IP pubblico della sede di appartenenza.

Eventuali limiti all’accesso ai sistemi vanno gestiti con delle policies, ovvero delle configurazioni che mettano in visibilità/disposizione ciò che deve essere raggiunto e nascondano eventuali servizi che non devono essere acceduti. Questo è il minimo indispensabile a cui si aggiungere anche il controllo del traffico che abiliteremo, ma di questo ne parliamo più avanti.

### Visibilità

In questo semplice disegno abbiamo un punto di controllo comodo, il firewall, che viene attraversato da tutto il traffico tra le reti. Al netto delle policies che applicheremo sicuramente possiamo dire di avere visibilità sulle comunicazioni tra client e server e verso internet, ma design troppo “grezzi” applicati a reti complesse possono limitare la visibilità su ciò che sta accadendo in rete.

Se la rete client è popolata da centinaia di sistemi tra workstation ed altri dispositivi (stampanti, NAS, ecc.) il firewall non è in grado di sapere che dialoghi ci sono all’interno di una specifico segmento di rete L2 (una subnet specifica o una VLAN). Un disegno che preveda una corretta segmentazione e l’utilizzo di altri strumenti - che vedremo più avanti - ci consente di migliorare il livello di visibilità sul traffico di rete e di conseguenza ci consente di applicare regole di detection o prevention meglio contestualizzate ed efficaci.

### Prossimo step

Mi è sembrato utile partire da alcuni concetti di base prima di buttarci sulla conf. di un oggetto senza sapere dove vogliamo andare a parare. Nel prossimo post+video configuriamo la prima macchina virtuale del laboratorio: il firewall pfSense.
