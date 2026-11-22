---
layout:     post
title:      "Attack Simulation, preparazione di uno scenario"
date:       2022-04-26 00:13:19 +0200
categories: [cyber-security, hacking, ita]
image:
---
A seguito di specifici Security Assessment è normale che emergano vulnerabilità anche gravi per le quali, tipicamente, si suggerisce di eseguire un patching del sistema o altre azioni di mitigazione. Purtroppo va considerato che in alcune situazioni in patching non è applicabile, spesso per ragioni non tecniche. Per portare un esempio particolarmente emblematico basta far riferimento all'evoluzione dei sistemi di automazione industriale, macchine o intere linee di produzione realizzate per restare operative per decenni e che spesso presentano componenti software che, semplicemente, non si possono aggiornare perché non è mai stata rilasciata una nuova versione. In questi casi non è raro trovare sistemi operativi particolarmente datati con tutti i problemi a livello di gestione della sicurezza che questo comporta.

E' opportuno essere pragmatici ed agire in un'attica di gestione del rischio, cosa che non significa - purtroppo - necessariamente eliminare ogni tipo di rischio. Una volta rilevata una possibile debolezza per la quale non è possibile applicare le più classiche remediation potrebbe essere utile approfondire l'analisi per cercare di stimare nel modo più preciso possibile quanto sia sfruttabile la falla ed i possibili impatti sul business del potenziale target.

Progettare e realizzare simulazioni di attacco può essere un utile strumento di verifica in quanto da la possibilità di esplorare realisticamente ciò che potrebbe avvenire e come gli eventuali sistemi di sicurezza reagirebbero a certe sollecitazioni. Inoltre, in caso di detection, l'attività è utile anche per verificare l'efficienza delle procedure di incident responce dei team operativi.

In questi giorni sto preparando uno scenario molto semplice che coinvolgerà parte del team target in qualità osservatori al fine di comprendere alcuni aspetti delle attività offensive. Vista la natura in parte didattica dell'attività ho pensato di condividere parte dello scenario ed approfittare di una delle sessioni live su Twitch per giocare un po' con lo scenario.

## Elementi base del lab

Come accennavo lo scenario è molto semplice in quanto presenta sistemi molto obsoleti che devono necessariamente esporre servizi vulnerabili. Nel caso specifico si tratta di sistemi Microsoft Windows fuori supporto e non aggiornabili che presentano le vulnerabilità note Blue Keep ([CVE-2019-0708](https://nvd.nist.gov/vuln/detail/cve-2019-0708)) e Ethernal Blue ([CVE-2017-0144](https://nvd.nist.gov/vuln/detail/CVE-2017-0144)), le macchine server utilizzano proprio uno dei servizi vulnerabili in quando espongono delle share folder.

I sistemi vulnerabili sono confinati in una rete server (*blue* network nello schema) e sono raggiungibili solo da alcuni sistemi client che per ragioni operative devono accedere alle share dei citati server. La visibilità tra le reti è garantita da un firewall che, nella configurazione di base, non applica controlli specifici per il controllo delle minacce.

<img src="{{ '/assets/images-posts/image-8.png' | relative_url }}" alt="image 8" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Per il lab di base utilizzo quindi i seguenti sistemi:

- Virtual Machine "client" con sistema operativo Microsoft Windows 7
- Virtual Machine "server" con sistema operativo Microsoft Windows 7
- Virtual Machine "server" con sistema operativo Ubuntu Linux 22.04 LTS
- Virtual Machine "firewall" con vAppliance Endian (v3.3.2) Community Edition

### Preparazione macchina client

Il sistema client è veramente base, una semplice installazione di Windows 7 va benissimo. Le uniche configurazione della macchina sono a livello rete e gli utenti. La configurazione di rete del mio sistema è la seguente:

<img src="{{ '/assets/images-posts/image-12.png' | relative_url }}" alt="image 12" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Dettaglio conf. di rete

Nel mio lab il gateway della rete client è il Firewall che a sua volta ha un gateway per le reti esterne. In questo modo dando ai sistemi che compongono il laboratorio un DNS è possibile farli accedere alla rete internet. La configurazione rispecchia lo scenario reale.

<img src="{{ '/assets/images-posts/image-13.png' | relative_url }}" alt="image 13" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Traceroute dalla macchina client

Per quanto riguarda gli utenti l'esigenza è di avere un utente amministratore locale ed un utente non privilegiato. Nello scenario reale questo sistema sarebbe membro di un dominio Active Directory ma in questo caso ci accontentiamo della doppia utenza. E' ovviamente previsto, in fase di attacco, l'accesso fisico al sistema con una sessione attiva dell'utente non privilegiato.

Nota a margine: il client nello scenario reale potrebbe essere una macchina Windows 7 o Windows 10. In questa sessione ci accomodiamo sul sistema operativo più datata.

### Preparazione macchina server Windows

Di base si tratta di una macchina praticamente identica alla macchina client se non per la posizione nella rete (come da schema), la configurazione della share e le relative regole del firewall locale. A dire il vero nello scenario reale il firewall locale è disabilitato, quindi questa sarà la configurazione di partenza anche nel lab.

### Preparazione macchina server Linux

Si tratta di un semplice ambiente LAMP basato su Ubuntu Linux e in questo scenario probabilmente non verrà utilizzato, ma visto che l'obiettivo è sfruttare il laboratorio anche per altre sessioni ha senso tenerla pronta.

### Preparazione macchina Firewall

Come accennato nel mio caso ho scelto una semplice vAppliance Endian per la quale ho configurato tre zone e relative reti:

- Green: corrisponde alla LAN della rete di laboratorio e su questa interfaccia è anche attiva la Management Console disponibile alla URL https://ip:10443
- Blue: corrisponde al segmento SERVER della rete di laboratorio
- Uplink: corrisponde alla WAN della rete di laboratorio

<img src="{{ '/assets/images-posts/image-14.png' | relative_url }}" alt="image 14" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Endian Console

In configurazione di default la zone Green e la zona Blue sono in piena visibilità, quindi il sistema client potrà dialogare da subito con il sistema server e il traffico potrà essere registrato nei logs del firewall:

<img src="{{ '/assets/images-posts/image-15.png' | relative_url }}" alt="image 15" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

### Preparazione macchina c&c

Come accennato anche nella live del 21 aprile ([online ancora per qualche giorno](https://www.twitch.tv/roccosicilia)) per pura comodità la macchina che utilizzeremo come c&c sarà il sistema Kali del mio lab ma, visto l'utilizzo che vogliamo farle nei primi test, va benissimo una qualsiasi macchina linux che sia in grado di ospitare un web server. Nel laboratorio utilizzerò Apache con Php e Python.

Questo sistema verrà utilizzato come una macchina già compromessa o comunque sotto il controller dell'attacker che è in grado di accedervi remotamente e comodamente via ssh.

## Prima fase dell'attacco

Come anticipato lo scenario prevede un accesso fisico al sistema *client* da cui si dovrà poi sviluppare l'attacco. Partirei quindi da una serie di rilevamenti sul sistema di partenza per poi usare la macchina come base per una scansione mirata nella rete target.

Una delle ipotesi di partenza è che l'attacker sia ragionevolmente certo di trovare le vulnerabilità citate, il sistema di scansione dovrà quindi operare in modo chirurgico. Una volta individuati i sistemi potenzialmente vulnerabili si dovrà procedere con l'exploiting del sistema con lo scopo di creare un accesso permanente alla macchina.

Oltre alla definizione dei singoli strumenti per eseguire le azioni offensive l'obiettivo di questa prima fase è quello di costruire i tools da eseguire rapidamente sul sistema su cui si ha la possibilità di accedere fisicamente. Per verificare l'efficienza dell'operazione l'azione verrà cronometrata.

Il base ai risultati della prima fase, che in parte potremo discutere nella prossima live del 28 aprile, valuteremo le attività della seconda fase in cui coinvolgeremo il sistema c&c.
