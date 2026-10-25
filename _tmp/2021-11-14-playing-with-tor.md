---
layout:     post
title:      "Playing with TOR"
date:       2021-11-14 22:59:36 +0100
categories: [hacking, ita]
image:
---
Durante la preparazione di alcuni laboratori per un workshop sulle simulazioni di attacco ho approfondito alcuni aspetti del funzionamento della rete ToR, quei dettagli che capita di leggere ma più raramente di toccare con mano fino a quando non se ne ha l'occasione. Mi piaceva l'idea di riassumere in un post *le sessioni di gioco* con la rete Tor ed un paio di utilizzi che penso possano essere utili nello svolgimento di attività offensive, ovviamente in contesti autorizzati.

<img src="{{ '/assets/images-posts/image.png' | relative_url }}" alt="image" style="float: left; width: 291px; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

installazione ed avvio del servizio Tor

Nota ovvia: il contenuto del post **ha finalità divulgative** al fine di condividere alcuni aspetti del funzionamento della rete Tor così da acquisire una maggiore consapevolezza dello strumento che, come tutti gli strumenti, può essere utilizzato anche per fini illeciti e proprio a tal proposito è bene saper riconoscere eventuali attività sospette eseguite attraverso questa rete.

Non è un how-to, per chi ha bisogno di una infarinatura ci sono moltissimi articoli che potete prendere in considerazione:

- Il forum del progetto <https://forum.torproject.net/>
- La documentazione per iniziare <https://tb-manual.torproject.org/running-tor-browser/>
- Un bel post del 2020 dove è ben spiegato il funzionamento base <https://skerritt.blog/how-does-tor-really-work/>

## Lab setup

Un minimo di infrastruttura per utilizzare il servizio. Per praticità utilizzo la mia kali box, ma potete ovviamente utilizzare quello che vi pare. L'installazione è semplicissima (vedi screenshot ad inizio post) ed una volta avviato il demone il servizio sarà immediatamente disponibile sulla local port 9050.

Per fare un po' di esperimenti assicurarsi di disporre anche dei seguenti software:

- apache2 + php
- wget / curl
- ssh-ping
- tor-browser

Oltre alla kali locale ho utilizzato un web server remoto per eseguire alcune prove, nel mio caso si tratta di un semplicissimo LAMP basato su Ubuntu (LTS) con esposto il servizio http ed ssh su porte non standard.

## Onion Site

Obiettivo del test era osservare log e traffico di un nodo Tor su cui è attivo un Onion Site, la prima cosa da fare è quindi configurare un il sito cipolla.

Premessa: i domain name .onion funzionano in modo diverso rispetto ai domain name che popolano la rete internet: un onion name corrisponde all'identità (univoca) di uno specifico nodo ([vedi rfc 7686](https://datatracker.ietf.org/doc/html/rfc7686)). In parole povere un onion name si riferisce specificatamente all'host su cui risiede il servizio in qualità di nodo della rete Tor.

Per configurare un "sito cipolla" è sufficiente accedere al file di configurazione di Tor in /etc/tor/torrc e definire la configurazione del servizio dichiarando il path per i file di configurazione. Viene inoltre dichiarata la porta del servizio da non interpretare come un sistema di pubblicazione: il servizio Tor si limiterà ad eseguire l'inoltro dei pacchetto in ingresso sulla porta 80 (visto che voglio intercettare il traffico http) vero il web server attivo sul sistema (apache2) precedentemente installato durante il setup del laboratorio.

<img src="{{ '/assets/images-posts/image-2.png' | relative_url }}" alt="image 2" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

configurazione base per un "sito cipolla"

Il mio apache non ha nessuna specifica configurazione, anzi è praticamente in configurazione di default ed il contenuto pubblicato è molto semplice, si tratta infatti di un PHP file che esegue la print dell'IP del client che accede al contenuto:

<img src="{{ '/assets/images-posts/image-3.png' | relative_url }}" alt="image 3" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Nel mio caso la macchina è una guest con un IP dietro un primo NAT per accedere alla rete locale tramite l'host (la mia workstation) e dietro un secondo NAT per accedere alla rete internet tramite la mia connettività. Il server non esegue quindi nessun tipo di pubblicazione di servizi verso la rete internet mentre è raggiungibile dalla mia LAN tramite il NAT del software di virtualizzazione. Per chiarire riporto uno schema di sintesi:

<img src="{{ '/assets/images-posts/image-9.png' | relative_url }}" alt="image 9" style="float: left; width: 400px; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

labz

Accedendo quindi al contenuto direttamente dalla guest o dalla mia workstation il sistema potrà registrare nei log l'IP del client che ha eseguito l'accesso al web server nel solito file /var/log/apache2/access.log.

Avviando il servizio Tor sulla VM hidden-server verrà generato l'indirizzo del sito .onion ed il demone si occuperà di intercettare le richieste verso la porta 80 in arrivo dalla rete Tor verso la porta 80 del servizio di pubblicazione HTTP.

Per simulare il comportamento di un utente che, attraverso la rete Tor, invii una richiesta GET ai contenuti del sito cipolla è sufficiente predisporre un ToR browser sulla workstation (o su un altro sistema esterno) così da ottenere il comportamento di un qualsiasi Tor user che voglia accedere al contenuto appena pubblicato. L'indirizzo del sito cipolla è disponibile all'interno del file ***/var/lib/tor/hidden_service/hostname***, nel mio caso:

<img src="{{ '/assets/images-posts/image-8.png' | relative_url }}" alt="image 8" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Per capire meglio cose sta accadendo sul sistema che ospita l'onion site ho verificato come prima cosa lo status delle connessione della macchina. Con i servizi apache e Tor attivi lo status delle connessione presentava poche e ben definite sessioni.

<img src="{{ '/assets/images-posts/image-11.png' | relative_url }}" alt="image 11" style="float: left; width: 400px; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Sulla porta 9050 della loopback è ovviamente in ascolto il demone Tor utilizzabile dal mio client come socks host. Già dalla seconda riga la cosa si fa interessante: il mio host contatta dal proprio IP in LAN il sistema 185.243.218.27 che, ricerche alla mano, è un ToR Node che fa riferimento a questo progetto: https://tuxli.ch/. Verificando il comportamento delle sessioni e la descrizione dei [servizi offerti da questo nodo](https://metrics.torproject.org/rs.html#search/bauruine), devo dedurne che si tratti del DirNode selezionato dal server per scaricare la lista dei Relay, inoltre il nodo stesso offre servizi di Relay. Ultimo dato utile è nella terza linea con il binding del servizio apache2 sulla porta 80, questo è il servizio che viene contattato, in definitiva, da un client che vuole accede al contenuto che il sito sta pubblicando. In un contesto standard vedremmo quindi una sessione tra il server ed il client in un formato del tipo:

```
{LocalIP}:80 <---> {RemoteIP}:{ClientPort}
```

Avviando il Tor browser su un altro host ed accedendo al sito cipolla già configurato possiamo osservare meglio il comportamento del demone ToR nel consentire l'accesso ai contenuti:

<img src="{{ '/assets/images-posts/image-13.png' | relative_url }}" alt="image 13" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Quello che accade è abbastanza chiaro: il Tor browser non compare tra i client in quanto la richiesta arriva al server all'interno della sessione già attiva con il Relay Node (*182.243.218.27*) e si presenta come una richiesta interna del sistema (*127.0.0.1:****46660***) verso il servizio http apparentemente binded sulla stessa loopback (*127.0.0.1:****80***). Questa sessione si riferisce in realtà al forward dei pacchetti eseguito dal demone Tor verso apache. Questo spiega anche come mai nell'access.log di apache compare l'IP 127.0.0.1 come client.

## Secure ssh access

<img src="{{ '/assets/images-posts/image-16.png' | relative_url }}" alt="image 16" style="float: left; width: 360px; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Qualcosa di simile a quanto fatto con la pubblicazione http è possibile farlo con ssh: in questo caso l'obiettivo molto operativo che volevo ottenere era una modalità di accesso via ssh ad un server all'interno della rete Tor.

Il vattoggio è relativamente chiaro: tenendo attivo il mio server all'intero della rete e configurando opportunamente il demone Tor potrò garantirmi un accesso in ssh alla mia macchina senza esporre il servizio ad internet nascondendo di fatto il sistema. Da questa posizione posso poi raggiungere altri sistemi anche all'esterno della rete Tor ma comunque attraversandola.

Lo scenario di base è identico al precedente con qualche aggiunta, in particolare sul server "nascosto" bisognerà necessariamente installare ed avviare il demone ssh ma, come per http, non sarà necessario eseguire un NAT sulla rete internet in quanto la raggiungibilità del servizio verrà affidata alla rete Tor. Il file di configurazione coinvolto è sempre /etc/tor/torrc in cui, poche righe sotto la configurazione del servizio http, vi sono le configurazioni per gli "altri servizi nascosti":

<img src="{{ '/assets/images-posts/image-17.png' | relative_url }}" alt="image 17" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Nel caso specifico, con la configurazione riportata nello screenshot, stiamo istruendo Tor ad inoltrare il traffico in arrivo sulla porta tcp\22 verso il servizio in ascolto sulla medesima porta del server. Nel file ***/var/lib/tor/other_hidden_service/hostname*** è riportato l'indirizzo .onion per raggiungere il servizio nascosto all'interno della rete. Una volta completata la configurazione potremo collegarci alla macchina in ssh puntando al sito cipolla corrispondente. Ovviamente il sistema da cui si vorrà eseguire la connessione dovrà essere a sua volta connesso alla rete Tor. Il comando è quindi semplicissimo:

```
torify ssh sheliak@{sitocipolla}.onion
```

Una volta avviata la connessione è molto probabile riscontrare una carta latenza nella risposta, si tratta di un effetto collaterale inevitabile in quanto i pacchetti che i due sistemi si scambiano stanno attraversando un minimo di tre Tor Node e ad ogni hop corrispondono operazioni di cifratura/decifratura. Tutto ciò introduce latenza nelle comunicazioni. Quanta?

<img src="{{ '/assets/images-posts/image-19.png' | relative_url }}" alt="image 19" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

ssh-ping verso il servizio ssh nascosto

Una volta ottenuto l'acceso al sistema, esattamente come visto per http, noteremo che i servizi di destinazione si vedono arrivare richieste di accesso dall'interfaccia di loopback. Quindi se eseguiamo delle verifiche su chi è connesso al sistema con il comando *who* ...

<img src="{{ '/assets/images-posts/image-20.png' | relative_url }}" alt="image 20" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

A sinistra la sessione ssh via Tor, a destra una console locale

... l'output mostrerà la sessione locale ed una sessione remota da 127.0.0.1 a testimoniare il nostro accesso "anonimo" quanto meno a livello di IP.

## Conclusioni e riflessioni

Il mio interesse specifico in questo laboratorio ruotava attorno all'esigenza di comprende meglio il funzionamento della rete Tor per valutare come sfruttarla in simulazioni di attacco e qualche idea me la sono fatta. Non sono da meno gli spunti a livello di incremento della sicurezza sfruttando i servizi nascosti per amministrare i propri sistemi senza esporli in nessun modo, ne con un NAT ne con una VPN che come ultimamente abbiamo visto è un servizio come gli altri e può avere dei bug.

Capito meglio il funzionamento mi è ben chiaro come si è potuta sfruttare la rete anche per fini illeciti come la creazione di botnet utilizzate per attacchi ad enti ed aziende. Ci sono degli aspetti che mi segno di approfondire in un prossimo lab come la possibilità di eseguire ricerche automatizzate in rete internet attraverso la rete Tor e la possibilità di scambiarsi informazioni e messaggi peer-to-peer.
