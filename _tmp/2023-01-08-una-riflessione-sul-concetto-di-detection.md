---
layout:     post
title:      "Una riflessione sul concetto di \"detection\""
date:       2023-01-08 18:00:00 +0100
categories: [cyber-security, hacking, ita]
image:
---
Come ho avuto modo di raccontare in qualche post su LinkedIn, negli ultimi mesi ho potuto dialogare con molti attori, italiani e non, del mondo MDR. Per i non addetti ai lavori: MDR è l'acronimo di Managed **Detection** and **Response** e si riferisce ai servizi di presidio degli eventi di una rete con capacità di intercettare minacce informatiche e reagire per mitigare e/o bloccare l'eventuale compromissione. Potremmo dire che si tratta dall'evoluzione dei più tradizionali servizi di Security Operation Center che hanno sempre avuto il compito di intercettare e segnalare eventuali situazioni di compromissione.

Nel discutere i diversi scenari di applicazione del concetto di **detection** ho notato due approcci che definirei complementari. Va detto che alcuni interlocutori utilizzano entrambi gli approcci mentre altri ne prediligono uno all'altro. Il primo approccio è network-oriented: i dati su cui viene eseguita l'analisi vengono da sonde a livello rete che, potendo osservare il traffico sia a confine che all'interno della struttura, analizzano le conversazioni e, se possibile, i contenuti per scovare eventuali minacce. Il secondo approccio è event-oriented: i dati su cui viene eseguita l'analisi provengono dai logs e dagli eventi registrati dai sistemi della rete che possono inviare informazioni "grezze" o già qualificate (es: allarmi da parte di hosts o altri sistemi).

**[Nota tecnica]** Nella discussione nata su LinkedIn emerge l'esigenza di estendere il dominio dell'approccio event-oriented a ciò che è possibile analizzare a livello kernel dei sistemi operativi grazie a specifici agent. Nel post considero questa fonte assimilabile ad un evento anche se non viene segnalata attraverso i classici servizi di gestione degli eventi ma, solitamente, attraverso un agent.

Non voglio arrivare a conclusioni di preferenza, lo scopo del post è illustrare i due approcci in modo semplice così da farsi un'idea. Le valutazioni di merito vanno fatte caso per caso. Come da titolo il post si limita al concetto di **detection**, mentre per il concetto di **response** valuterò un post dedicato più avanti.

## Detection network-oriented

Alla base di questo modello vi è l'assunto di poter osservare tutto il traffico di rete, sia nord/sud che est/ovest. Di per se questo requisito non è impossibile da rispettare ma in contesti complessi potrebbe non essere così immediato. Per ragionare sul modello a prescindere dalla complessità della rete (tema comunque da non trascurare in fase di analisi) mettiamoci comodi e lavoriamo su uno scenario semplice:

<img src="{{ '/assets/images-posts/image-3.png' | relative_url }}" alt="image 3" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Nota di laboratorio: il lab mette a disposizione uno Standard Virtual Switch (su ESXi 7.x) su cui sono configurati tre Port Group in corrispondenza di tre VLAN (LAN, DMZ, WAN) a simulare una semplice rete.

In questo semplice esempio, facilmente applicabile in contesti con più reti e più apparati, vi è l'esigenza di portare tutto il traffico in visibilità di un oggetto "sonda" che si occuperà di analizzarlo a caccia di eventuali anomalie da segnalare direttamente all'amministratore di rete o, in contesti più complessi e completi, da portare a conoscenza di un sistema centralizzato e presidiato come un SIEM gestito da un security operation center (o altro team dedicato).

Virtualmente, se tutto il traffico fosse presidiato ed accessibile a livello di contenuto, dovremmo aver completa visibilità. E' opportuno considerare che **nel mondo vero** non è così semplice raccogliere tutto il traffico di una rete. In un contesto multi sede sarebbe necessario predisporre almeno una sonda per sede. Inoltre le reti delle singole sedi possono essere molto complesse e potrebbero quindi richiedere più sonde. Ciò che spesso accade è che **alcune porzioni di traffico non vengono raccolte**.

C'è un altro tema da considerare se approcciamo lo scenario dal punto di vista di un threat actor. Cosa succede se volessimo attaccare una workstation (ws1 nello schema) con un'azione locale e che non transiti necessariamente dalla rete? Ovviamente la detection sarebbe impossibile se non grazie a sistemi che lavorano a livello host. Altro esempio: cosa succede se l'attacker utilizzasse l'host ws1 per inviare dati all'esterno della rete generando traffico verso un servizio in uso dall'organizzazione come OneDrive o Google Drive?

Il modello di per se ha il vantaggio di avete un punto di osservazione molto comodo per quantità di informazioni a cui può accedere e per capillarità. Va necessariamente considerato che non tutti gli attacchi hanno bisogno di transitare dall'infrastruttura di rete del target o potrebbero essere utilizzate tecniche particolarmente *stealth* per rendere l'azione difficile da rilevare.

## Detection event-oriented

Ciò che accade sugli hosts è da diversi anni un tema di interesse: i logs delle security appliance come i Firewall sono sempre stati interessanti ma a questi si sono aggiunti gli eventi dei vari sistemi che popolano le reti. A livello cronologico si è prima svilippato in interesse verso i sistemi server per poi estendere il concetto a tutto ciò che può produrre un log: workstation, sistemi operativi, applicazioni, telefoni e caffettiere connesse alla rete LAN per contare quanti caffè vengono fatti ogni giorno (l'IoT ha avuto i suoi impatti).

Va inoltre aggiunto ciò che è possibile osservare a basso livello, in un mio recente post su LinkedIn si è discusso di quanto sia possibile andare in profondità con l'analisi a livello kernel utilizzando sistemi di controllo (es. EDR) in grado di sfruttare specifici moduli. Metto tutto, un po' impropriamente, nel calderone della detection event-oriented in considerazione del fatto che si tratta di comportamenti che possiamo osservare a bordo di un sistema e di cui possiamo centralizzare il collecting e l'analisi.

<img src="{{ '/assets/images-posts/image-4.png' | relative_url }}" alt="image 4" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

L'approccio consente di avere un elevato livello di controllo sui singoli sistemi che popolano la rete (oltre a rendere possibile l'utilizzo di agent in grado di agire attivamente sui sistemi) ed ha l'ovvio limite di non dare evidenza in relazione a ciò che succede laddove non è stato installato/configurato un agent, spesso integrato a livello di sistema operativo, per inviare le informazioni a un sistema centralizzato in grado di analizzarle, SIEM o simili.

Le due aree non presidiate sono infatti determinate da quei sistemi che non hanno la possibilità di inviare eventi o dai sistemi che hanno la possibilità di connettersi alla rete target ma non sono gestiti centralmente (guest). In questi casi, non potendo riceve eventi direttamente dal sistema, possiamo contare solo su ciò che gli altri "agent" sono in grado di osservare a seguito di movimenti laterali. Azioni complesse ma assolutamente fattibili come un attacco MITM possono essere difficili da individuare in questo contesto. Anche attività di scansione passiva della rete diventano difficili da rilevare e, come per il precedente scenario, l'utilizzo di canali "leciti" e cifrati per comunicare con l'esterno rappresenta un problema dal punto di vista della detection in quanto il SIEM deve avere degli elementi per distinguere traffico lecito da traffico illecito in assenza di informazioni sul contenuto e a parità (o quasi) di destinazione e comportamento.

Abbiamo anche in questo casa un modello che consente grande capillarità ma che da solo lascerebbe un po' di spazio di manovra se il contesto consentisse l'accesso a porte di rete ad eventuale personale ospite (autorizzato e non).

## Qualche esempio per giocare

Giusto per capire di cosa stiamo parlando riporto due esempi, semplicissimi, relativi ai due scenari in cui vediamo come vengono interpretate azioni offensive utilizzando una detection network-oriented (tramite un IDS) ed una detection event-oriented (tramite un SIEM). Per semplificare il lab e permettervi di riprodurlo in modo abbastanza semplice utilizzo una appliance Security Onion.

Partiamo dall'azione più banale che, come spesso discutiamo durante le live, non è esattamente una cosa che accade *mondo vero* (fuori dai laboratori e dai corsi di formazione)... una bella scansione con nmap :-)

<img src="{{ '/assets/images-posts/screenshot_20230105_175457.png' | relative_url }}" alt="screenshot_20230105_175457" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

nmap -sS verso il sistema Security Onion

Il traffico di una scansione è molto rumoroso, è quindi probabile che una sonda in rete possa interpretarlo per quello che è, verrebbe quindi generato un allarme sul sistema che controlla il traffico il traffico in transito nella rete:

<img src="{{ '/assets/images-posts/image-1.png' | relative_url }}" alt="image 1" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

L'allarme generato da suricata per la scansione

Anche utilizzando l'opzione -sT, un pelo meno aggressiva rispetto al primo tentativo, la quantità di rumore resta alta e comunque sufficiente a generare nuovi alert. Azioni più delicate tendono a passare invece inosservate o ad essere associate a severity più basse: un esempio è uno scan via nmap finalizzato alla sola discovery di host nella rete; di recente abbiamo utilizzato queste opzioni assieme al mio Red Team:

```
nmap -sn -PR -T5 -oA alive $target
```

Ovviamente in questo caso ci si accontenta di un obiettivo intermedio: la verifica degli host up. Anche abusando un po' di questo tool in questa modalità il traffico in questo caso è relativamente basso e "agita poco le acque", si riesci quindi ad ottenere una scansione degli host attivi senza destare sospetti:

<img src="{{ '/assets/images-posts/image-2.png' | relative_url }}" alt="image 2" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Un banale ciclo for per passare alla scansione più target

Volendo essere estremamente chirurgici, una volta estratti silenziosamente gli host attivi potremmo passare a scansioni mirate su specifiche porte a caccia di servizi, questa volta usando uno semplice script in Python per verificare se le porte rispondono o no.

Il livello di sensibilità la sonda può ovviamente essere configurata così da individuare anche comportamenti come quelli utilizzati negli esempi in cui suricata, in qualità di IDS attivo nella rete, non ha segnalato allarmi. Il rovescio della medaglia, in caso si renda troppo sensibile la sonda, è ovviamente ricevere potenzialmente troppi falsi positivi.

Sul fronte di ciò che è possibile osservare a livello host il principio è simile. Come precedentemente discusso solitamente si utilizzano delle componenti, native o facendo uso di agent, che raccolgono ed analizzano ciò che accade a bordo di un sistema.

Facciamo un esempio molto semplice:

<img src="{{ '/assets/images-posts/image-3.png' | relative_url }}" alt="image 3" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Tentativo di accesso in SSH si un sistema con agent attivo

Le regole di base per Security Onion identificano un accesso SSH fallito come un allarme con severity ***low***:

<img src="{{ '/assets/images-posts/image-4.png' | relative_url }}" alt="image 4" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

In questo caso è il modulo ossec ad intercettare l'evento

Cambiamo punto di osservazione e posizioniamoci a bordo di un sistema, esattamente come se fossimo l'attacker che ha guadagnato un primo accesso con un utente qualsiasi di sistema e deve mettersi comodo. Ci sono un migliaio di cose che potremmo fare in questa situazione (sto preparando un post al riguardo). Tipicamente ci si muove sul sistema compromesso, si raccolgono info sulle configurazioni e sui tools presenti per poi arrivare, solitamente, a portare qualcosa dentro e/o fuori dall'ambiente.

Queste azioni, ancora una volta in base alla sensibilità dei sistemi di detection, possono far scattare degli allarmi o meno. Ad esempio se porto uno zip file sul sistema, tenendo sempre in considerazione che siamo in una configurazione base, il sistema SIEM non segnala nessun evento, ma se porto un binary file via HTTP ...

<img src="{{ '/assets/images-posts/image-5.png' | relative_url }}" alt="image 5" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

wget di ncat da un host all'interno della stessa rete

... l'azione diventa chiaramente molto sospetta e potrebbe far scattare qualche regola di detection.

<img src="{{ '/assets/images-posts/image-6.png' | relative_url }}" alt="image 6" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Nell'attuale configurazione del lab possiamo invece modificare i permessi del file scaricato ed eseguirlo senza generare allarmi a livello host, azione effettivamente pericolosa che in un sistema di produzione dovrebbe generare degli allarmi.

Ancora una volta dobbiamo ricordare che queste regole sono modificabili e che stiamo lavorando solo a livello di detection senza fare analisi dei contenuti di un file, cosa che un EDR farebbe sicuramente e molto probabilmente piallerebbe il file *ncat* alla velocità della luce. Qualche settimana fa in una live abbiamo visto come si è comportato l'EDR del mio laptop quando abbiamo provato ad eseguire un *nc.exe*. Quello che sicuramente metterebbe in difficoltà il sistema di detection è l'utilizzo di ciò che è già a bordo della macchina in modo tale da generare log del tutto simili a quelli che il sistema genera abitualmente.

## Arriviamo al dunque

Nel mio lavoro e nel mio ambito di ricerca passo molto tempo a cercare i punti deboli dei sistemi e sono giunto alla conclusione che non ci si può affidare ad un singolo modello o ad un singolo approccio. Come spesso scrivo qui e nei miei post su LinkedIn, è necessario partire da un'analisi dei punti deboli per poi individuare gli strumenti idonei - in questo caso alla detection delle minacce - per il vostro specifico contesto. Troppo spesso ho trovato sistemi che potenzialmente avrebbero potuto rilevare qualsiasi cosa ma, a causa di una errata analisi, erano stati configurati con mille eccezioni fino a renderli inefficaci.

L'altro elemento da cui far partire i ragionamenti è una valutazione sui modelli di attacco che potrebbero interessare il target: dobbiamo smetterla di ragionare sulla presenza della singola vulnerabilità, gli attacchi sono singole azioni di exploiting. Dobbiamo lavorare sulla base di scenari offensivi realistici in grado di sfruttare le falle evidenziate in analisi.
