---
layout:     post
title:      "Riflettendo su alcuni recenti attacchi cyber."
date:       2020-10-18 09:00:00 +0200
categories: [cyber-security]
image:
---

Una premessa doverosa prima di addentrarci nel tema di questo mio intervento. La condivisione delle idee e la crescita della cultura è, in assoluto, lo strumento per risolvere i problemi ed affrontare in generale nuove sfide. Sviluppare una cultura della sicurezza informatica vi permetterà di affrontare il problema delle minacce cyber. Buona lettura.

Analizzando alcuni attacchi su cui recentemente mi sono trovato a lavorare (purtroppo solo nelle complesse ore immediatamente successive al rilevamento dell’incident) ho potuto osservare alcuni modelli di attacco che presentano molti tratti in comune e sui quali è saggio riflettere.

## Quando la tua azienda è nel mirino

Per ovvie ragioni non farò riferimento a nessun evento specifico, gli elementi che vorrei condividere sono individuabili in decine di attacchi anche del passato, ho comunque trovato interessante come il modello si sia, in alcuni contesti, uniformato.

Primo elemento che emerge è che gli attacchi in questione sono chiaramente “targeted”, ovvero l’attacker ha colpito un target specifico, selezionato appositamente in relazione a dei requisiti solo in parte deducibili. I tratti in comune che si possono osservare, in questo tentativo di ricostruire il ragionamento dell’attacker — inteso come l’entità che ha deciso l’attacco e non necessariamente chi lo ha eseguito materialmente — sono relativi alla dimensione dell’azienda ed all’impatto sul business.

Il contesto è infatti quello dell’azienda strutturata con fatturato milionario e migliaia di utenti. Aziende non certo sprovviste di sistemi di sicurezza o di personale IT competente, anzi… sempre più spesso sono aziende che hanno operato delle scelte sul fronte della protezione dei sistemi — protezione, non necessariamente difesa — adottando soluzioni specifiche, dialogando con partner tecnologici di tutto rispetto. Tutti elementi che portano a pensare che l’attacco sia stato ben progettato, ipotesi confermata da alcune evidenze sfuggite a chi ha materialmente eseguito l’attacco durante la fase di “cancellazione delle tracce”.

> Potrebbe sembrare un controsenso il fatto che un attacco bel progettato si lasci dietro tracce che consentano di fare analisi anche molto dettagliate. E’ da considerare che le reti in oggetto sono molto complesse e spesso ben strutturate in quanto a sistemi di analisi e raccolta delle informazioni.

## La posta in gioco: il buon nome dell’azienda

Non possiamo ignorare il tema della reputazione. Il modello usato spesso abbina un’azione di sabotaggio dell’infrastruttura informatica — con inevitabili impatti operativi come il blocco della produzione o delle attività correlate, come la logistica o la gestione degli ordini — a richieste di tipo estorsivo in caso di mancata collaborazione. Una tipica formula prevede infatti la minaccia di divulgare informazioni trafugate al target a seguito del data breach, spesso con qualche forzatura sull’applicazione del GDPR citato come se fosse una sorta di spauracchio.

Il tema è molto complesso in quanto mette le aziende nelle condizioni di dover necessariamente indagare sull’eventualità che vi sia stato effettivamente un data breach. Va detto che dopo un attacco che ha le connotazioni di un’azione mirata, a prescindere dalle metodologie e dal vettore, è saggio appurare se non vi sia stato un data breach (non mi dilungo oltre).

L’impatto in questo caso, ammesso che le aziende e gli enti interessati si organizzino per una corretta gestione a livello normativo del security incident, va valutato su due principali fronti: l’immagine del brand ed i dati strategici potenzialmente trafugati. E’ ovvio che la magnitudo degli impatti è strettamente legata al business dell’azienda target: ci sono aziende enormi che sono delle vere perle rare per competenze e proposte nel loro settore, ma sono inserite in un contesto dove la reputazione qualitativa del prodotto è tale da non temere un impatto di immagine. La stessa azienda potrebbe però essere seriamente penalizzata se fossero resi pubblici i piani strategici interni. E’ complicato generare consapevolezza su questo fronte; da tenere bene a mente che non sono informazioni particolarmente difficili da trafugare in un contesto di attacco mirato.

## Cosa ci dice il coroner

Toccati gli aspetti più tattici andiamo sui temi tecnici: ci sono evidenze che non si possono ignorare. In molti casi è stato possibile appurare che gli accessi sono avvenuto tramite l’utilizzo di credenziali di utenti autorizzati (a più livello) ad accedere alla rete da remoto tramite servizi che lo stesso target mette a disposizione della propria utenza: accessi remoti a portali, VPN, piattaforme applicative.

L’azione molto chirurgica fa pensare che le credenziali fossero state trafugate in precedenti azioni non necessariamente condotte verso il target. E’ persino difficile oggi contare quanti siti e portali abbiano subito un data breach che ha coinvolto i dati degli utenti iscritti al servizio, con relativo dump dei Database che contiene username e hash delle password, dati più che sufficienti per ricostruire una credenziale da provare su più piattaforme, compresa la VPN aziendale.

Come si fa a trovare il “portal” di accesso per la VPN? Ci pensa Google con qualche ricerca mirata:

<img src="{{ '/assets/images-posts/riflettendo-su-alcuni-recenti-attacchi.png' | relative_url }}" alt="OSInt" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Tralasciando in questo post il vasto tema delle azioni offensive tanto semplici quanto efficaci (OSInt è uno strumento potentissimo per la raccolta di dati anche molto dettagliati) il metodo di accesso scelto ci deve far riflettere. Appare evidente una preparazione all’attacco con lo scopo di essere estremamente silenziosi. Azioni troppo evidenti come tentativi di Brute Forcing sarebbero state quasi certamente intercettate dai sistemi di protezione, una sessione VPN di un utente qualsiasi (o quasi), con credenziali corrette desta molti meno sospetti ed è anche complesso chiedere alla tecnologia di discriminare un accesso con intenzioni malevole da un accesso di un utente autorizzato.

Terzo elemento sempre presente, ed ultimo in questa trattazione anche se ve ne sono altri che meriterebbero di essere approfonditi, è l’elevata penetrazione all’interno della rete. I target in questione hanno reti molto estese ed articolate: centinaia di sistemi tra server e device di rete, migliaia di sistemi client, decine di sedi operative. Nonostante l’estensione della rete è interessante notare come l’attacker sia riuscito ad esplorarla in buona parte: non è raro trovare tracce di accesso, o tentativi di accesso, in moltissimi sistemi.

E’ ormai estremamente frequente constatare che i sistemi di backup siano stati compromessi anche molto in profondità fino a rimuovere le snapshot dagli storage system e ad eseguire l’erase dei tape. Questo livello di profondità richiede tempo e, ancora una volta, l’accesso a diversi sistemi che spesso hanno — dovrebbero avere — credenziali differenti.

Non passa inosservata, inoltre la tendenza a mantenere dei punti di presenza su alcuni sistemi solo all’apparenza non compromessi: una tattica molto astuta che spesso consente all’attacker di avviare nuove sessioni offensive contando sul fatto che i sistemi apparentemente “sani” non verranno bonificati. A tal proposito una questione ancora aperta e su cui sto ancora eseguendo delle verifiche è relativa al fatto che spesso il sistema a rimanere apparentemente non compromesso è uno dei Domain Controller… a buon intenditore poche parole.

## Con gli occhi dell’hacker

Mi piacerebbe chiudere con un consiglio che possa, da subito, aiutare gli IT Manager chiamati a difendere grandi infrastrutture, ma sono sempre più convinto che il passo da fare sia un gesto di assoluta volontà: **dovete voler affrontare il problema cambiando punto di vista**. Una volta che vi sarete convinti di questo potrete iniziare a costruire una strategia di difesa efficace. Fino ad allora dovrete accontentarvi di cercare di parare i colpi.
