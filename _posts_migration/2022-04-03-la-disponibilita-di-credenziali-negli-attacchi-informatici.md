---
layout:     post
title:      "La disponibilità di credenziali negli attacchi informatici"
date:       2022-04-03 21:29:26 +0200
categories: [cyber-security, hacking, ita]
image:
---
Anche in questo breve post resto sul tema della "recon" con un focus particolare: la ricerca e l'impiego di credenziali valide per l'attuazione di un attacco informatico. Tra le attività che l'attacker esegue, una volta mappate le tecnologie in uso dall'organizzazione terget ed i servizi esposti in rete pubblica (posta elettronica, accessi VPN, portali aziendali, ecc.), vi è la ricerca di credenziali valide per accedere ai servizi individuati.

E' ovvio che conoscere una credenziale valida consentirebbe all'attacker di accedere a nuove informazioni se non direttamente alla rete target. E' quindi assolutamente logico verificare se gli utenti dell'organizzazione siano già stati vittime di data breach con relativo furto di una credenziale.

A causa di una cattiva abitudine degli utenti capita ancora molto spesso che vengano utilizzare credenziali uguali o simili per accessi differenti (es: posta elettronica personale ed aziendale). Va considerato che le credenziali utilizzate in un contesto aziendale sono spesso dei veri e propri passepartout nominali che danno accesso a molte applicazioni e sistemi, compreso l'accesso VPN alla rete aziendale. Questa combinazione di fattori rende il fenomeno del "password reuse" una concreta minaccia per le organizzazioni in quanto l'attacker che entra in possesso di una credenziale proveniente da un qualsiasi data breach in cui sia stato coinvolto un membro dell'organizzazione target potrebbe trovarsi nelle condizioni di accedere a servizi dell'organizzazione stessa utilizzando la stessa identica credenziale o versioni simili di questa.

Facciamo un esempio banale. L'utente *Mario Rossi* utilizza come password una sequenza alfanumerica a cui aggiunge un progressivo nel passaggio da una piattaforma all'altra: asd23qwe!01, asd23qwe!02, asd23qwe!03, ecc. L'attacker che dovesse entrare in possesso di una delle password potrebbe tentare la generazione di diverse combinazioni da provare sulle varie piattaforme. Tools come *crunch* possono essere utilizzati per generare potenziali password utilizzando un set specifico di caratteri in modo da restringere il campo a quelli tipicamente utilizzati dalla vittima.

<img src="{{ '/assets/images-posts/image-1.png' | relative_url }}" alt="image 1" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Esempio di generazione stringe con crunch

Il concetto è semplice: si ottiene un dizionario qualificato di password per uno specifico utente da passare poi a tools di brute forcing o a semplici scripts in grado di eseguire un test di accesso all'applicazione target. Metto a disposizione un piccolo esempio per eseguire il test in sequenza di un accesso via SSH dato un utente valido ed un dizionario di password: https://github.com/roccosicilia/sToolz/tree/master/RedTeam/BruteForce. Chi ha familiarità con il mondo del pen-testing probabilmente conosce tools come Hydra, una semplice utility che può essere istruita per eseguire tentativi di accesso anche a webform sulla base di un dizionario predefinito.

L'assunto, come detto, è di disporre di un potenziale set di credenziali valide provenienti da data breach passati. Esistono diverse fonti, assolutamente legali ed utilizzate anche in contesti di difesa, da dove è possibile raccogliere informazioni in merito a passati data breach ed eventuali credenziali trafugate. Uno dei più noti è [Have I Been Pwned](https://haveibeenpwned.com/) dove è possibile verificare la presenza di una propria credenziale in un Data Breach e, accedendo alle API, è possibile anche consultare il contenuto dei dati relativi al breach, credenziali comprese. Altri due servizi molto interessanti a mio parere sono [BreachDirectory](https://breachdirectory.org/) e [LeakCheck](https://leakcheck.io/?ref=381167) (quest'ultimo è un referral link).

Su BreachDirectory vorrei organizzare un approfondimento sfruttando il piano base di rapidapi.com che mi consente di fare un paio di prove utili a comprende quanto sia fin troppo facile accedere a questa tipologia di dati.

Semplicemente accedendo dalla homr del sito al link del menu "api" si viene rediretti alla dashboard di rapidapi da dove è possibile accedere alla struttura della API ed a diversi esempi di codice utilizzabile per creare un semplice script:

<img src="{{ '/assets/images-posts/image-1.png' | relative_url }}" alt="image 1" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Tool di test delle API

Anche con competenze estremamente base in un qualsiasi linguaggio di scripting (rapidapi riporta esempi per decine di sintassi) è possibile costruire una request base per ricerche mirate o semplici automatismi per sfogliare le voci dei database a caccia di set di informazioni su più target.

## Contromisure

Come accebbato tutto ha origine da un malcostume degli utenti, avendo quindi cura di utilizzare differenti credenziali per i diversi servizi a cui ci si registra la possibilità di essere vittime di credential struffing si riduce enormemente. Un altro ausilio è l'utilizzo di sistemi di autenticazione multi fattore così da non delegare alla segretezza della password la sicurezza degli accessi ai propri sistemi/servizi.

A somma di queste sane abitudini ed in considerazione del trend in crescita dei data breach potrebbe aver senso anche monitorare, tramite i servizi disponibili anche sui portali citati, la propria presenza nei database che aggregano tali informazioni.

Ho personalmente potuto osservare l'efficacia di tecniche come il credential stuffing e non è il caso di sottovalutare il fenomeno. In generale credo si sia tutti abbastanza concordi nel considerare i meccanismi di autenticazione basati sulla coppia user/password non particolarmente sicuri. È il caso di passare oltre.
