---
layout: post
title:  "Sistemi non vulnerabili e tecniche di “elusione”."
date:   2019-02-12 09:00:00 +0200
categories: [cyber-security]
---
Discutendo con il mitico [Fabio](https://www.ciscozine.com/?utm_source=roccosicilia) di 802.1x e MITM, ed in particolare del fatto che esistono protocolli/tecnologie che al momento non presentano bug specifici, risultando così non attaccabili dirittemente, mi è venuto in mente che nello sviluppo di un attacco informatico questo scenario si presenta abbastanza spesso e nel tempo si sono sviluppate tecniche specifiche per “aggirare” l’ostacolo.

Chi si occupa di progettare e realizzare infrastrutture informatiche cerca di utilizzare soluzioni ovviamente sicure, resilienti, con funzionalità evolute anche in relazione alla sicurezza informatica. Il tal senso il livello di sicurezza di una certa soluzione, presa a se, è identificabile dalle funzionalità specifiche che offre e dalla presenza o meno di vulnerabilità note censibili nel tempo e, si spera, prontamente corrette.

Si tende quindi a credere che la somma di strumenti e soluzioni sicure generi, automaticamente, sistemi sicuri. Ma il processo che porta ad un incremento della sicurezza non può passare solo dall’avere prodotti validi, è sicuramente un passo necessario ma non è la soluzione definitiva. Non a caso aziende ed enti, con fior di tecnologie implementate, subiscono attacchi anche con impatti elevati sul proprio business.

Mettiamoci il “cappello nero” e cerchiamo di affrontare la questione in un contesto reale di progettazione di un attacco. Per praticità uso casi di studio reali e scenari anche molto diffusi, alcuni dei quali sperimentati personalmente in passate attività di Ethical Hacking (sono certo che chi fa questo mestiere da tempo potrebbe raccontarne molte).

Capita spesso — fortunatamente — di operare in contesti dove i sistemi sono stati dotati di dispositivi di sicurezza: servizi di analisi e monitoraggio del traffico, sistemi di detection, sistemi di autenticazione, fino ad arrivare a SIEM, SOC, ecc… Tutto molto bello.

Prima di iniziare a “martellare” sui sistemi (lo so, lo ripeto sempre, ma non è mai abbastanza) di solito si eseguono una serie di ricognizioni atte a comprendere il perimetro attaccabile (che è sempre più ampio di quello che si crede) e raccogliere informazioni sul target.

> A tal proposito: è inutile chiedere assessment o penetration testing su specifici perimetri. Non esiste un attacker che, individuato un target, si scaglia solo su un fronte da noi selezionato, meglio se quello appena aggiornato e protetto… non sono così fessi.

La raccolta di informazioni, assieme alle successive fasi, consente di creare un modello rappresentativo del target anche molto dettagliato: ovviamente l’individuazione di sistemi di sicurezza fa parte del gioco e spesso, per stanarli, vengono eseguiti volutamente attacchi inutili al mero scopo di verificare come i sistemi rispondono.

Capito il perimetro, fatto di sistemi/persone/device/procedure/ecc, e ipotizzate le aree ben presidiate da sistemi di sicurezza efficienti, di solito molte ma mai tutte, si inizia a lavorare sulle aree scoperte o su quei sistemi di sicurezza che consentono tecniche “evasive”. Non è scritto da nessuna parte che si debba attaccare frontalmente il proprio bersaglio, è molto più logico sfruttare i punti deboli o, nei casi più complessi, errori di design nell’implementazione di un sistema di sicurezza.

Due esempi reali e chiarificatori. In relazione al tema dei “punti deboli”, devo prendere atto della tendenze — errata — a non dare la stessa importanza ai diversi device che si connettono alla rete. Tornando al caso che discutevo con Fabio: è verissimo che EAP-TLS al momento non presenta vulnerabilità apprezzabili che si possano sfruttare, ma è anche vero che le aziende si trovano a dover utilizzare sistemi che non supportano protocolli sicuri: stampanti, SmartTV, mi è capitato di trovare una PlayStation4. Per non parlare del tema SmartPhone: ottimo avere i NAC più potenti dell’universo, ma se poi gli utenti possono usare la rete WiFi aziendale con il proprio SmartPhone, che immancabilmente non gestiamo, abbiamo un bel problema.

> L’introduzione di una tecnologia deve essere supportata da una corretta contestualizzazione a livello di DESIGN e PROCEDURE al fine di gestire le immancabili eccezioni.

Altro scenario abbastanza frequente è relativo all’utilizzo quanto meno curioso che si fa di alcune tipologie di sistemi di protezione evoluta come i Web Application Firewall (WAF) o vari servizi/sistemi anti DDoS. Si tratta di oggeti meravigliosi che per ragioni ignote usiamo malissimo lasciando la porta aperta a tecniche di “evasion”. Senza scomodare le tecniche più astute e anche più complesse da realizzare (quindi costose in termini di effort per l’attacker) spesso si sfruttano banali errori di design: ho perso il conto che WAF configurati per controllore il traffico di “www.sito-target.test” e non quello di “demo.sito-target.test” dove entrambi i nomi dominio puntano allo stesso sistema. Se posso bypassare il WAF non me lo faccio dire due volte.

E anche oggi non parlo di Social Engineering, ma ci arriviamo.