---
layout:     post
title:      "HomeLab - Intro"
date:       2026-02-10 17:52:51 +0100
categories: [cyber-security, hacking, ita, study-with-me]
image:      /assets/images-posts/create-a-featured-image-for-a-blog-post-titled-homelab.png
---
Come detto in [questo post su LinkedIn](https://www.linkedin.com/posts/roccosicilia_ids-ips-ed-analisi-del-traffico-share-7423779325562355713-nHq4?utm_source=share&utm_medium=member_desktop&rcm=ACoAAATK5U0By2qlNbOT_QThQp0s692DGhr_JfU) dedico qualche articolo (e video) al mio HomeLab con lo scopo di pubblicare i dettagli tecnici della struttura che ho scelto e renderlo replicabile per chiunque sia interessato a *smanettare* con dei test di laboratorio in ambito info sec. Nel mio caso l'esigenza specifica è disporre di un ambiente completo in cui eseguire e migliorare tecniche di attacco specifiche (per chi non sa mi occupo di security test sia come attività lavorativa che come campo di ricerca) in un contesto controllato da sistemi di detection a vari livelli.

#### Perché un HomeLab?

Chi lavora in un ambito tecnico informatico (come capita per molte discipline tecniche) hai bisogno di studiare (molto) e fare pratica (molta). Non importa l'età anagrafica raggiunta o gli anni di esperienza, lo studio è una costante anche a 44 anni (la mia età attuale) e con poco più di 20 anni di servizio alle spalle.

Disporre di un proprio HomeLab diventa presto una necessità. Epoche diverse hanno portato a strumenti e possibilità diversi: pre-virtualizzazione avere un HomeLab significava avere hardware, tanto hardware, su cui installare *cose*. Virtualizzazione e cloud computing hanno modificato enormemente il paradigma e oggi tutti noi possiamo disporre anche di molte risorse senza dover acquisire hardware di proprietà.

L'[azienda per cui lavoro](https://www.linkedin.com/company/nts-italy-gmbh-srl/) (che, sottolineo, è molto attenta alla preparazione dei team tecnici e mette a disposizione molti strumenti) mi mette a disposizione un ricco laboratorio con la possibilità di creare guest ed utilizzare prodotto commerciali. Da anni utilizzo anche risorse in cloud (in particolare AWS) per alcuni test. Nonostante l'abbondanza di risorse ci sono dei vincoli di cui devo tener conto e probabilmente tutti quelli che si occupano di cyber sec. e di security test hanno incontrato: le infrastruttura messe a disposizione dalla propria azienda o dai cloud provider sono sistemi che devono aderire a determinati standard di sicurezza, cosa che "cozza" con l'esigenza di simulare ambienti con vulnerabilità per spararci contro attacchi specifici. Mi è capitato più di una volta di trovarmi una istanza AWS isolata perché avvenivano cose "strane" o sospette dal punto di vista della sicurezza... ed effettivamente i miei test ad un sistema di controllo esterno sembrano ciò che sono, attacchi informatici (anche se simulati).

È per me stato naturale, ad un certo punto, riconsiderare la possibilità di disporre di un HomeLab in cui fare serenamente ***disastri***: far girare payload, far crashare sistemi, saturare le risorse, ecc., senza che questo si traduca in "risposte di prevenzione" da parte del provider o fastidi verso i miei colleghi con cui condivido il lab aziendale.

https://youtu.be/eyPFMt5YwrE

#### Struttura di base: hardware

<img src="{{ '/assets/images-posts/image-1.png' | relative_url }}" alt="image 1" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Schema di sintesi

In questo primo post descrivo l'infrastruttura di base. L'obiettivo è quindi consentire il setup iniziale dell'host e delle VMs con i sistemi operativi che sto utilizzando. Ovviamente avete pienamente titolo di valutare delle variazioni, le mie scelte sono legate a specifiche esigenze che vi riporto in modo che possiate fare una scelta soggettiva sul replicare la mia configurazione o apportare delle variazioni.

Partirei dall'hardware coinvolto. Il cuore del lab è un host che fa parte della mia dotazione aziendale (come dicevo [NTS Italy](https://www.linkedin.com/company/nts-italy-gmbh-srl/) ed in generale il gruppo [NTS Netzwerk Telekom Service](https://nts.eu) è molto attento alle esigenze tecniche ed agli strumenti di lavoro) che utilizzo come base per diverse operazioni di security test. L'host ha di fatto il compito di far girare diverse macchine virtuali che, a seconda dell'attività che devo svolgere, attivo e configuro opportunamente. Inizialmente usavo un device molto piccolo, un Raspberry PI che in realtà utilizzo ancora per alcune attività, ma con la crescita della complessità delle azioni ho avuto l'esigenza di cambiare device.

Ho scelto, dopo averlo già visto all'opera, un miniPC T9 pro (il riferimento al prodotto non ha scopi pubblicitari, per il lab potete prendere una qualsiasi macchina x86 64bit).

[<img src="{{ '/assets/images-posts/image-2.png' | relative_url }}" alt="image 2" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />](https://www.instagram.com/p/DS4yAkWioLm/)

Instagram post del setup

La macchina ha un onesto processore [Intel N95](https://www.intel.com/content/www/us/en/products/sku/231800/intel-processor-n95-6m-cache-up-to-3-40-ghz/specifications.html) con 4 core, 16 GB di RAM (aumentabili), SSD da 512 GB (la GPU è integrata). Come I/O ports ha 2 NIC Ethernet 1 Gbps + 1 NIC Wireless, 3 USB ports e 3 HDMI (che onestamente al momento non ho pensato di usare).

Per una mia esigenza personale ho mantenuto il sistema operativo Windows 11 (mi serve un sistema operativo Microsoft installato *bare metal* per alcuni test) ma per molti potrebbe avere più senso utilizzare una distro Linux o un hypervisor. Se come me decidete di mantenere Windows 11 suggerisco di lavorare un po' sull'ottimizzazione delle risorse in modo da "contenere" la RAM che il sistema utilizzerebbe per l'avvio di Apps e servizio che probabilmente poi non userete. Lo so che è banale ma semplicemente disattivando qualche servizio e desktop app ho ridotto il consumo di memoria RAM "a sistema fermo" di quasi 2 GB e visto che l'obiettivo è far girare più VMs possibile su un singolo host la RAM va gestita bene.

Oltre al miniPC l'altro "pezzo di ferro" è lo switch, o meglio il router che utilizzo come uno switch. Si tratta di un RouterBoard che svariati anni fa ebbi in dono durante un corso MikroTik. Qui faccio una nota: per quanto riguarda il mondo enterprise ho sempre usato o cercato di usare tecnologia Cisco per la parte network e datacenter per un tema di affidabilità e funzionalità, non è un segreto il fatto che Cisco è stato uno dei vendor che ho approcciato per primo in ambito network e che ho ritrovato in moltissimi step del mio percorso professionale. La tecnologia Cisco come molte altre tecnologie è *virtualizzabile* ([Andrea mostra spesso](https://www.adainese.it/blog/) network lab completamente virtuali) ma le mie esigenze non sono compatibili con quelle di un host dedicato ad un tool come EVE-NG, per questo ho deciso di ripiegare sull'oggetto più piccolo che avevo e che mi consentisse di disporre di molte funzionalità mentre a costo di perdere in affidabilità e prestazioni. Fine della nota.

Torniamo al RouterBoard che per le esigenze del lab di base, quello che ho intenzione di descrivere in questa mini serie di post, deve fungere da switch per interconnettere gli host fisici (cioè quello che appoggio sulla mia scrivania) con gli host software, le virtual machines.

Nel mondo MikroTik questa configurazione è possibile assegnando ad uno stesso Bridge le porte del RouterBoard:

<img src="{{ '/assets/images-posts/image-3.png' | relative_url }}" alt="image 3" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Conf. da interfaccia

A dirla tutta non è strettamente necessario disporre di uno switch, potreste anche collegarvi direttamente alla porte ethernet del miniPC con una configurazione di rete corretta ed il dialogo con l'host è garantito. Nel mio caso ci sono altri devices che occasionalmente ho bisogno di accendere e far partecipare al lab. e questa è la configurazione più logica ed utile.

---

Se questo articolo ti è stato utile puoi sostenere il progetto tramite il mio canale [Patreon](https://patreon.com/roccosicilia). Registrati al blog per rimanere aggioranto.

---

#### Le macchine virtuali

In questo primo post ve le elenco in modo che possiamo predisporre il lab con gli elementi di base, la configurazione dei singoli elementi sarà oggetto dei prossimi post.

Sempre con riferimento allo schema partiamo dal Firewall che nel mio caso è un pfSense v2.7.2 community edition a cui ho assegnato 512 MB di RAM, 1 vCPU core e 20 GB di vHDD. Nota importante: la macchina deve avere due NIC. La prima vNIC, nel mio lab, è il bridge-mode con l'interfaccia Wireless del miniPC e sarà la WAN del Firewall, la seconda vNIC è in bridge-mode con una delle interfacce Gigabit Ethernet e sarà la LAN del Firewall.

<img src="{{ '/assets/images-posts/image-4.png' | relative_url }}" alt="image 4" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Gestione text-based di pfSense

Una volta installato sarà possibile eseguire la prima configurazione a livelli rete dall'interfaccia text-based disponibile tramite la *console* della VM. Una volta definito l'IP lato LAN sarà possibile accedere all'interfaccia di gestione via web tramite la rete LAN.

Come si intravedere dalla mia configurazione anche lato WAN il mio sistema ha un IP privato: si tratta di una rete Wireless appositamente creata per il lab all'interno della mia rete domestica tramite cui il lab stesso naviga verso internet. In questa configurazione sarà ovviamente possibile gestire NAT sulla rete WAN 192.168.1.0/24 ma non sarà possibile pubblicare servizi verso internet (salvo "doppi NAT", ma questa è un'altra storia).

Dopo di che abbiamo due ambienti Microsoft Windows. Il primo funge da Domain Controller ed è un Windows Server 2016 con 2 vCPU (cap all'80%), 2 GB di RAM e 80 GB di vHDD. Questo sistema non dovrà essere particolarmente caricato, l'AD in un lab fa sempre poco, ma lavorarci in remote desktop potrebbe risultare un po' fastidioso se limitiamo troppo la RAM. Il secondo sistema Microsoft è, nel mio caso, un Windows 7 che uso spesso anche per diverse demo. Per le finalità del lab va benissimo un qualsiasi sistema operativo client Microsoft che possa poi unirsi al dominio Active Directory.

Per la macchina Ubuntu dedicata ai sistemi di detection è meglio abbondare un po' con le risorse. Nella mia installazione ho trovato un buon equilibrio assegnando 6 GB di RAM (ma 8 non le fanno male), 4 vCPU e 60 GB di vHDD. Anche per questa macchina ho previsto due NIC ma per ora solo una è attiva e configurata.

Per la macchina Kali (o Parrot o qualsiasi altri sistemi desideriate usare come base per gli "attacchi" in lab) mi sono limitato molto nelle risorse ed ho assegnato 1 GB di RAM e 2 vCPU. Nel mio caso questa macchina verrà usata per lo più da cli.

#### La rete

Nel setup iniziale tutte le VMs sono sulla stessa subnet che nel mio lab è la 10.10.10.0/24. Tutti i sistemi hanno IP statico e come DNS (vedremo poi il motivo) usano il Domain Controller. Ovviamente con la prima accensione ed i primi update vi converrà usare la vostra rete domestica non avendo ancora configurato il Firewall di laboratorio.

#### Prossimo step

Una volta create la VMs si può passare alla configurazione ed iniziamo con il Firewall ed i servizi di rete nel prossimo post/video.
