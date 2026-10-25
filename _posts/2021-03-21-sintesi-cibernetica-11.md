---
layout:     post
title:      "Sintesi cibernetica #11"
date:       2021-03-21 09:00:00 +0100
categories: [update]
image:
---

Gestire un incident, che si tratti di un fault, un attacco o un malfunzionamento di un sistema critico, è una pratica che richiede elevate competenze tecniche ed una buona dose di sangue freddo. Non bisogna solo sapere ciò che c’è da fare, bisogna anche sapere perché va fatto in un modo specifico, applicando “quella procedura” e non “l’altra”. Serve esperienza e pratica acquisibile grazie a tecniche come l’addestramento. Improvvisare non aiuta, anzi, si rischia di trasformare l’incidente in un disastro.

Bisogna anche rendersi conto che esistono situazione che non sono ripristinabili, nel senso che non esiste il processo che annulla quanto accaduto, è però possibile, con la giusta strategia, *ricostruire* e ripartire.

La settimana appena trascorsa ha dato diversi spunti di riflessione sulla gestione degli incident, in particolare OVH è alle prese con le prime ripartenze ma a quanto pare ieri (20 marzo) i sistemi sono stati nuovamente spenti a causa di un principio di incendio in uno del locali dove erano posizionate delle batterie UPS in quel momento non operative. La prossima settimana doveva essere quella dell’accensione dei sistemi ma questo nuovo incidente rischia di generare nuovi ritardi.

La vicenda OVH va seguita lasciando da parte il pensiero critico, è una scuola per tutti coloro che lavorano nel campo delle infrastrutture ad alta disponibilità di servizio. Osserviamo ed impariamo dagli errori tanto quanto dai successi… e consiglio di partire proprio dalle scelte comunicative che CEO che in prima persona aggiorna gli utenti tramite Twiter: <https://twitter.com/olesovhcom>.

Su Exchange non dico nulla se non di stare in campana, questa settimana si è parlato di DearCry, un crypto malware in grado di sfruttare la vulnerabilità ProxyLogon… evidentemente in molto stanno cercando una scusa per lanciare qualche job di restore dei dati.

Nuovi interessanti movimenti li ho trovati sul fronte SolarWinds, a distanza di settimane si sono osservate delle ingegnose tecniche per guadagnare un accesso permanente alle mailbox Office 365 di alcune delle aziende interessate dall’attacco (miglia di aziende). La tecniche è spiegata [in questo articolo](https://www.darkreading.com/attacks-breaches/solarwinds-linked-attackers-target-microsoft-365-mailboxes/d/d-id/1340467) ed è molto semplice: l’attacker utilizza credenziali legittime, ovviamente sottratte tramite l’attacco già in corso, per eseguire una modifica alla configurazione delle mailbox rendendole accessibili in read-only. Silenziosi ed efficaci.

Qualche riflessione in più [**sul podcast**](https://www.spreaker.com/episode/43988010).

> Il mio vecchio podcast non esiste più. Oggi porto aventi un nuovo progetto podcast che puoi trovare [qui](https://www.infosecunplugged.it).