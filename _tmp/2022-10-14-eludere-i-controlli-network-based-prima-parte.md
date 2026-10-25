---
layout:     post
title:      "Eludere i controlli \"network-based\" [prima parte]"
date:       2022-10-14 09:00:00 +0200
categories: [cyber-security, hacking, ita]
image:
---
## Abstract

Nelle attività di Red Teaming ed Adversary Simulation vi è la necessità di condurre l'azione, se lo scenario lo richiede, senza essere individuati. Una dalle attività che vorrei meglio indagare è la creazione di una falsa "baseline" per ingannare i sistemi di detection. In questo esercizio di laboratorio metto le basi per la creazione di traffico http/https da utilizzare per coprire azioni offensive verso una web application.

## Scenario

Questo primo laboratorio nasce da una esigenza specifica che recentemente ho avuto modo di portare all'interno di una delle sessione [live su Twitch](https://www.twitch.tv/roccosicilia): dovendo analizzare un sistema target senza essere identificati - e quindi "bloccati" dall'amministratore - ho avuto la necessità di generare traffico verosimile verso il sito web. Quasi contemporaneamente ho avuto modo di discutere con diversi Red Team di approccio e metodi per condurre azioni silenziose e ho voluto fare qualche esperimento.

Il target del laboratorio è una macchina [dvwp](https://github.com/vavkamil/dvwp), sistema che stiamo utilizzando io ed [Andrea](https://www.adainese.it/) per le nostre sessioni Red vs. Blue ma va benissimo un qualsiasi web server in grado di registrare i log di accesso al sistema. Per eseguire la detection vorrei utilizzare un sistema in grado di analizzare i log in modo semplice. Mentre scrivo non so ancora se utilizzerò Splunk o Graylog.

Divido questa prima parte del lab in più step:

1. Infrastruttura *proxy* per utilizzo di più IP sorgenti
2. Script di crawling per definizione page list
3. Script di generazione traffico

Una volta portata a termina la prima fase potremo iniziare ad osservare il comportamento dello script grazie all'analisi dei log.

## Più sorgenti IP

Inizialmente avevo pensato di utilizzare una tecnica di spoofing con scapy, non ho completamente abbandonato l'idea ma facendo un po' di prove ho trovato più utile in questa fase utilizzare la rete Tor per far pervenire al web server chiamate da diversi IP. Per generare una quantità di traffico verosimile, corrispondente a più utenti che contemporaneamente accedono al sito target, non basta un singolo proxy in quanto l'IP di navigazione sarebbe unico all'interno della stessa finestra di tempo. L'idea è quindi di avviare più istanze Tor per ottenere diversi "path" di navigazione e quindi, in teoria, diversi exit node.

<img src="{{ '/assets/images-posts/attacker_tor_target.png' | relative_url }}" alt="attacker_tor_target" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Nei log del web server mi aspetto quindi vengano registrati gli accessi di almeno tre IP address, in caso di utilizzo di tre istanze proxy, che dovrebbero anche variare dopo qualche minuto.

Nota a margine: su Tor ho già [scritto qualcosa in passato](https://roccosicilia.com/2021/11/14/playing-with-tor/) di cui consiglio la lettura.

A livello di implementazione la base Tor è molto semplice, è ovviamente necessario disporre di almeno una macchina linux in cui installare il pacchetto con il comando:

```
$ apt install tor
```

Una volta installato ed avviato il servizio dovreste poter controllare lo status dello stesso. Nel mio caso la situazione post installazione (ho utilizzato un host Ubuntu LTS) è la seguente:

<img src="{{ '/assets/images-posts/image.png' | relative_url }}" alt="image" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

stato del demone Tor

Di default Tor utilizza la porta 9050 sulla loopback della macchina server su cui è installato, nel nostro laboratorio dobbiamo fare qualche modifica per ottenere tre istanze su tre differenti porte utilizzando l'IP di una delle interfacce di rete del sistema.

Il file di configurazione di base è /etc/tor/torrc di cui creeremo tre copie: torrc_1, torrc_2, torre_3. Per ogni file di configurazione imposteremo tre diverse tcp port, nel mio caso 9061, 9062, 9063:

<img src="{{ '/assets/images-posts/image-1.png' | relative_url }}" alt="image 1" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

configurazione del file torrc_1

Nello stesso file va anche definita una DataDirectory specifica, nel mio caso ho definito i path /var/lib/tor1, /var/lib/tor2, /var/lib/tor3. Una volta predisposti i file di configurazione possiamo quindi avviare le nostre tre istanze con il comando:

```
$ sudo tor -f /etc/tor/torrc_1 &
$ sudo tor -f /etc/tor/torrc_2 &
$ sudo tor -f /etc/tor/torrc_3 &
```

Il risultato deve essere di tre processi attivi e relativi servizi sulle porte definite:

<img src="{{ '/assets/images-posts/image-2.png' | relative_url }}" alt="image 2" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Giunti a questo risultato abbiamo predisposto la base proxy. Ovviamente la quantità di processi è a vostra discrezione, il consumo di per se è basso e dipende molto da quanto traffico si andrà a generare. Il sistema che ho utilizzato per questo LAB è il mio "cube-pc", non particolarmente potente ma abbastanza carrozzato a CPU. Una volta a runtime raccoglierò anche la statistiche di carico.

## Generare la lista delle pagine "valide"

Obiettivo del lab è generare traffico verosimile, non possiamo quindi permetterci di ottenere una sfilza di errori 404 come abbiamo avuto modo di osservare in una passata sessione Red vs. Blue con Andrea in occasione dell'utilizzo di DirBuster. L'idea è di utilizzare un semplice crawler per raccogliere i link disponibili in una pagina del sito target per generare poi le richieste che simuleranno il traffico di ipotetici utenti.

Di tools a questo scopo ce ne sono centinaia, ma visto che lo scopo di queste sessione sessioni è approfondire e capire ci armiamo di python e ci creiamo il nostro piccolo crawler. Nulla di particolare, dobbiamo solo accedere al contenuto di una pagina web, estrarre tutti i link (che in HTML sono definiti con <a href="https://www.sito.web/">link</a>) e posizionarli in un file di comodo. Lo script fatto per l'occasione lo trovate nella mia repo GitHub all'interno del progetto sToolz: <https://github.com/roccosicilia/sToolz/tree/master/RedTeam/AnonHttpReq>.

Il funzionamento è molto semplice, lo script va lanciato dandogli come parametro la URL del sito target ed il nome file su cui riportare i link:

<img src="{{ '/assets/images-posts/image-3.png' | relative_url }}" alt="image 3" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

test dello script su questo blog

Lo script utilizza il file generato scrivendo in "append" eventuali nuovi contenuti ed è possibile passare come paramento anche una specifica pagina ottenendo l'arricchimento della lista dei link.

## Componiamo l'arma cyber

Ora abbiamo i proxy e la lista degli URL validi da utilizzare, manca solo lo script per generare delle *requests* realistiche. Si tratta di una componente in realtà molto semplice da realizzare in quanto per utilizzare un proxy in una chiamata http/https possiamo tranquillamente utilizzare il modulo *requests* di python. Volendo essere particolarmente precisi potremmo eseguire richieste ad intervalli irregolari attingendo dalle URL in modo random.

Lo script che realizziamo deve prevedere tre parametri in input: la URL target, il file in cui sono presenti i link generati dal crawler e le iterazioni (quante richiesta fare). Si tratterà quindi di un classico ciclo in cui, per ogni iterazione, sceglieremo random il link target ed il proxy da utilizzare. Di seguito la porzione di codice del prototipo (nella repo trovate tutto):

```
while (i <= counter):
    pos = randrange(0, urls_num)
    socksp = randrange(1, 4)
    print("Select URL in pos {}, proxy {}: \t{}".format(pos, socksp, urls[pos]))
    # session.get(urls[pos]).text
    session.proxies = { 'http':  'socks5://192.168.1.6:906{}'.format(socksp), 'https': 'socks5://192.168.1.6:906{}'.format(socksp) }
    session.get(urls[pos])
    i = i+1
```

Ovviamente gli IP indicati nei socks5 si riferiscono al mio laboratorio e terminato il prototipo avrà senso portare queste info in un file di configurazione assieme a molte altre variabili.

Se abbiamo già a disposizione un elenco URL in un file precedentemente creato possiamo eseguire una prova verso il nostro target:

```
$ python ./AnonHttpReq.py http://ec2-15-161-154-157.eu-south-1.compute.amazonaws.com aws.txt 10
```

Facendo qualche test ho notato che ogni tanto i proxy vanno in timeout, c'è sicuramente del tuning da fare per rendete tutto più fluido gestendo la specifica eccezione.

## Cosa manca?

Nella repo di [sToolz](https://github.com/roccosicilia/sToolz) trovate tutti gli script aggiornati e nelle prossime ore ci rimetteremo mano assieme grazie alla Live su Twitch prevista per il 14 ottobre alle 21:30. Oltre a sistemare un po' la struttura dello script dobbiamo ovviamente sistemare un po' di dettagli come lo user agent che viene registrato dai log del web server.

Diciamo che la base è pronta, bisogna sistemare i dettagli e rendere tutto utilizzabile con un mail script unico. Dopo di che potremo mettere alla priva il risultato assieme ad Andrea e, nella seconda parte, vediamo come predisporre un controllo che rilevi questo tipo di azioni.
