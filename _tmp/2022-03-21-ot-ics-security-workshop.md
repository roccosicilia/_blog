---
layout:     post
title:      "OT / ICS Security Workshop"
date:       2022-03-21 07:00:00 +0100
categories: [cyber-security, ita, ot-iot]
image:
---
Scrivo questo post il giorno prima rispetto al workshop che si terrà il 17 marzo in collaborazione con Festo Academy ma lo pubblicherò solo qualche giorno dopo. In questa occasione vorrei riassumente alcune dei temi trattati durante la sessione assieme ad [Andrea Dainese](https://www.adainese.it/) con il quale ho condiviso la conduzione.

Come da titolo il tema è la sicurezza (cyber) delle infrastrutture OT più comunemente denominate "reti di fabbrica" ma che di fatto sono qualcosa di più complesso di una infrastruttura di interconnessione tra sistemi industriali. Scopo della sessione è stato l'introduzione alle possibili minacce alle quali i sistemi industriali possono essere esposti e discutere alcune specificità che rendono questi sistemi potenzialmente più facili da aggredire.

Come accennato la sessione è stata presentata in condivisione con Andrea con il quale, a staffetta, ci siamo divisi gli argomenti. In questo post sintetizzo i temi da esposti: una introduzione, più volte argomentata anche in altri contesti, in relazione al modello di business del cyber crime con alcuni esempi "famosi" per essere stati particolarmente efficaci, seguita da una sessione dedicata ad alcune peculiarità tecniche e di gestione dei device OT/ICS che, se non correttamente presidiate, possono essere veicoli per alcune tipologie di attacchi.

## Il modello di business del cyber crime

Ne ho parlato in moltissime occasioni e non mi voglio ripetere in questo post ([qui uno degli articoli passati](https://roccosicilia.com/2021/05/14/il-fenomeno-del-crimine-informatico/)) quindi mi limito a ricordare che il cyber crime è a tutti gli effetti un business digitale, è l'estensione nel cyber spazio del crimine "tradizionale", il suo scopo è fare quattrini. Il cyber crime non centra nulla con l'attivismo e tantomeno con l'hacking e gli hacker.

## Alcune delle principali minacce in ambito OT

Andiamo dritti al centro della questione tecnico-operativa sui cui abbiamo presentato uno dei focus (non è l'unico ovviamente): l'accesso e la manutenzione remota dei devices OT. Le componenti informatiche di un impianto industriale sono molto frequentemente interconnesse alla rete locale (la rete di fabbrica) per dialogare tra loro e per consentire monitoraggio e manutenzione da parte del vendor.

Nel migliore dei casi il vendor ha pensato ad una soluzione per approcciare la gestione da remoto del device ma spesso si incontrano non poche difficoltà, o peculiarità, delle reti che ospitano tali dispositivi. In questo contesto, se non normato, avviene di tutto: dai dispositivi interconnessi ai quali viene concesso di accedere alla rete internet senza uno specifico blocco o controllo così da consentire al vendor un'accesso autonomo al device tramite VPN o tunneling, fino ad esporre il device direttamente alla rete pubblica.

E' ovvio che in qualche modo il vendor deve poter accedere al disposizioni per garantirne la manutenzione ma tale esigenza deve essere opportunamente gestita. In generale si sconsiglia di adottare metodi di accesso remoto che non siano in qualche misura controllati/presidiati dall'amministratore della rete che deve poter attivare/disattivare il tunnel e registrare l'evento di accesso al device. A tal proposito tutto ciò che in qualche misura "aggira" i controlli imposti dall'amministratore (es: Modem LTE all'interno dei dispositivi) per quanto comodo non rappresenta una buona idea dal punto di vista della sicurezza dell'infrastruttura.

Opportuno è considerare anche l'affidabilità dei sistemi informatici del personale esterno che accede ai sistemi industriali: se un dispositivo compromesso si connette al nostro impianto esiste la seria possibilità che l'attacker sfrutti questa "connessione" per accedere all'infrastruttura oggetto di manutenzione.

Particolarmente interessante è constatare l'incredibile fiducia nel prossimo che si può trovare in chi ha deciso di esporre direttamente alla rete internet sistemi ICS...

<img src="{{ '/assets/images-posts/image.png' | relative_url }}" alt="image" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

C'è poco da dire: per pubblicare un sistema industriale serve una ragione valida e viste le attuali possibilità tecnologiche a me di **ragioni valide** non me ne vengono.

Ultimo spunto in questa mini-sessione è relativo all'accesso fisico ai sistemi che, per questioni legate alla longevità degli impianti industriali, spesso sono costituiti da componenti che utilizzano software anche molto datati e non aggiornabili. Questa peculiarità mantiene viva la possibilità di sfruttare debolezze non più presenti nei recenti sistemi operativi o gestibili facilmente con policies di sicurezza o protezioni software.

Diventa così relativamente semplice introdurre in una organizzazione un USB drive infetto in grado di compromettere sistemi non particolarmente protetti come è possibile (anche in contesti IT a dire il vero) utilizzare *armi* come le USB Rubber Ducky.

## Dopo il webinar...

... ci sono un paio di aspetti che mi piacerebbe approfondire, in particolare gli scenari di accesso remoto e la discovery di impianti industriali tramite Shodan o altri strumenti di semplice accesso. Su questi temi aspettatevi una live dedicata.
