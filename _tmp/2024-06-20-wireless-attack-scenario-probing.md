---
layout:     post
title:      "Wireless attack scenario: probing"
date:       2024-06-20 16:00:00 +0200
categories: [cyber-security, hacking, ita]
image:
---
Una digressione sul tema del probing che non avevo previsto di trattare in questa serie. L'approfondimento parte da un comportamento che inizialmente non avevo compreso da parte della WiFi Pineapple con cui stiamo giocando che, nella versione attuale, ha aggiunto funzionalità che in passato non c'erano, o meglio, erano presenti ma dietro configurazione specifica. Nota: non è un post sul funzionamento della WiFi Pineapple di cui prendo in considerazione solo una specifica funzione.

Parto dal comportamento osservato. Dopo alcuni utilizzi su campo in cui avevo attivato lo spoofing delle reti da "replicare" in un contesto di Evil Twin Attack, ho notato un insolito numero di SSID pubblicati dal rogue access point. Analizzandoli molti SSID non era tra quelli visibili a seguito di una scansione delle reti in zona. Da dove venivano?

<img src="{{ '/assets/images-posts/screenshot-2024-05-19-at-12.09.00.png' | relative_url }}" alt="screenshot 2024 05 19 at 12.09.00" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Configurazione del PineAP

Le nuove versioni del device impersonano anche le reti che appaiono tra quelle "sondate" dai clienti intercettati. Sul piano tattico è una estensione del classico Evil Twin definito KARMA Attack, da un punto di vista pratico così come è implementata la funzione si rischia di fare una gran confusione in quanto, solitamente, preferisco di gran lunga io scegliere che SSID impersonare in base al contesto. Inoltre l'interfaccia non consente di comprendere quali reti si riferiscono alle letture degli AP disponibili e quali ai dati provenienti dal probing. Come dicevo, tutto molto bello ma l'interfaccia semplificata lascia poco spazio di manovra su valutazioni che solitamente l'analista vorrebbe fare per preparare al meglio l'attacco.

Questo post di approfondimenti mi è quindi utile per mettere un po' di ordine negli appunti e strutturare meglio l'utilizzo dei dati di probing in un contesto reale, anche perché sono effettivamente utili per diverse attività.

---

Nelle [twitch live del 17 e 18 maggio](https://twitch.tv/roccosicilia) ho iniziato un lab sul tema del probing per raccogliere ed analizzare una serie di dati. Le registrazioni sono sempre archiviate su Patreon per i supporter: <https://pratreon.com/roccosicilia>.

Se l'argomento ti interessa e vuoi ricevere i prossimi update puoi registrarti al blog lasciando la tua email.

---

## Meta-dati e OSInt

Cercando informazioni sul comportamento dei client wireless ho trovato molte riflessioni sull'utilizzo dei meta-dati derivanti dalle scansioni. Considerando che monitorando un dispositivo possiamo registrare con certezza MAC address (e quindi Vendor nella maggior parte dei casi), rete a cui è associato, reti note (grazie al probing), non è difficile fare delle deduzioni sul target o quanto meno speculare su eventuali location visitate dagli utenti.

Di fatto possiamo affermare che se un dispositivo fa probing di una certa rete, significa che almeno una volta ci si è connesso. Quindi se il mio smartphone fa probing della rete "*BitHorn Free WiFi*" può significare solo che quella rete la conosce e ci si è connesso almeno una volta per mia volontà. Il nome della rete, in molti casi, può indicare un luogo ben preciso come un hotel, un aeroporto, un bar o un ristorante, un'azienda. La verifica del probing di un dispositivo potrebbe quindi darci un elenco di luoghi visitati dal suo possessore. Un dato interessante per un'attività di ricognizione o di analisi OSInt.

Le stesse informazioni posso essere utilizzate per sviluppare un attacco noto come KARMA Attack.

## KARMA Attack

Le informazioni relative alle attività di probing sono la base di questa tipologia di attacco: l'attacker analizza le reti a cui i device vorrebbero connettersi e predispone il suo rogue access point di conseguenza, potendo contare di essere l'unico dispositivo in zona che pubblica quel SSID. I device configurati per connettersi automaticamente a queste reti (es: la propria home network) lo faranno senza particolari problemi dando all'attacker la possibilità di sviluppare altre azioni offensive verso un dispositivo che di fatto si trova in una rete gestita da quest'ultimo.

Il comportamento dei device può variare a seconda della versione del sistema operativo, anche versione relativamente recenti di Android e iOS (per restare nel mondo mobile) possono cadere facilmente in trappola.

## Raccolta ed analisi dei dati

Avremo modo di discutere la realizzazione degli attacchi nei prossimi post. In questa parte dello studio mi concentro sulla raccolta e sull'elaborazione delle informazioni, tutte azioni che richiedono un po' di operatività.

Per raccogliere i dati dobbiamo programmare una sessione di ricognizione (vedi precedente post) presso la zona del target. Per i miei test un caro amico (IT manager di un'azienda che posso raggiungere senza fare ore di viaggio) mi ha concesso di usare i suoi dati per le mie analisi, ovviamente opportunamente censurati. Durante una delle prime sessioni di ricognizione ho avuto modo di raccogliere i dati relativi alle attività di probing di diversi device di cui ho estratto circa 60 min. di monitoraggio prelevati direttamente dalle statistiche di airodump in CSV.

L'attività è stata eseguita simulando un'azione di ricognizione con una Raspberry PI3 nascosta in un piccolo sacchetto di stoffa che portavo con me. Il device era alimentato da un piccolo powerbank ed era dotato di antenna supplementare, una Alpha AWUS036ACM.

<img src="{{ '/assets/images-posts/image-5.png' | relative_url }}" alt="image 5" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Operativamente l'attività è abbastanza semplice: si predispone in monitor mode la NIC wireless, si mette tutto nel "sacchetto tattico" e ci si fa una passeggiata.

```
# comado utilizzato sulla Raspberry
sudo nohup airodump-ng -w file.out --output-format csv wlan1mon &
```

Nel primo giro mi sono accontentato dei dati di probing che ammontano a qualche centinaio di device e qualche decina di reti da questi cercate:

<img src="{{ '/assets/images-posts/probing-ex1.png' | relative_url }}" alt="probing ex1" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Estratto del CSV generato durante il sopralluogo.

Con questo elenco in mano dobbiamo identificare i client potenzialmente interessanti per un attacco tenendo in considerazione che devono essere client verosimilmente utilizzati all'interno della struttura target e con un livello di segnale accettabile. A tal fine l'azione di ricognizione deve essere relativamente chirurgica per non rischiare di trovarsi in elenco client non riconducibili al target. Vanno poi esclusi tutti i device che sono associati ad un SSID con le relative reti e tutti i device con un segnale troppo basso, la mia soglia sarà -75 db.

<img src="{{ '/assets/images-posts/image.png' | relative_url }}" alt="image" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Estratto dei possibili client target.

Ci sono tutti gli ingredienti: i mac address dei client interessanti da filtrare durante l'attacco (per evitare di coinvolgere altri client fuori scope), le reti da impersonare, l'area di interesse in cui posizionare il rogue access point (quella del sopralluogo).

## Approfondimento sul probing

Aver raccolto il pcap ci consente di analizzare in dettaglio il comportamento del client quando esegue il probing di una rete. Come esempio uso un dispositivo che ha catturato la mia attenzione in quanto non sono riuscito a trovare il vendor di riferimento, il MAC (parziale) è 2a:09:d8:XX:XX:XX. Ti questo dispositivo abbiamo catturato 9 pacchetti, tutti di probing. Di questi 5 sono richieste "Wildcard" e 4 direct probing.

<img src="{{ '/assets/images-posts/image-1.png' | relative_url }}" alt="image 1" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Radio Info da Wireshark.

Primo dato utile è il PHY type, ovvero il livello fisico di comunicazione che nel mondo radio si riferisce al protocollo di trasmissione: 802.11b. Una versione abbastanza datata dello standard (1999) che fa uso unicamente di frequenze nella fascia dei 2.4 GHz.

Una verifica "off topic" rispetto al tipo di attacco che stiamo discutendo è relativa alla quantità di pacchetti di probing a 2.4 GHz sono stati rilevati rispetto ai pacchetti a 5 GHz. Come anticipo anche nel video il sospetto, rilevato anche in altri studi da parte di altri ricercatori, è che in questo scenario sia relativamente difficile far affidamento sui protocolli a 5 GHz a causa della distanza fisica, fatto che limiterebbe anche le possibilità del threat actor.

<img src="{{ '/assets/images-posts/probe-request.png' | relative_url }}" alt="probe request" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Probe Request.

In questo caso specifico si vede come il device abbia eseguito, in rapida sequenza, una serie di probe request dove è possibile osservare le reti (campo SSID) cercate del device. Anche queste richieste sono in broadcast, ovvero vengono inviate a tutti i dispositivi radio nel raggio di copertura, ma riportano uno specifico SSID a cui i device si collegherebbe se fosse disponibile.

La conseguenza di questo comportamento è quella discussa nel contesto del KARMA attack: se un rogue access point iniziasse a pubblicare un SSID cercato da questo dispositivo potremmo ottenere una connessione diretta con il target.

## Test su campo

Assieme a questo post esce un video in due versioni di un test su campo di una attività di ricognizione in cui ho raccolto alcuni dati di probing. La versione sintetica è disponibile su YouTube mentre [**per i supporter di PATREON è disponibile la full version**](https://www.patreon.com/posts/wireless-attack-106541682).

https://www.youtube.com/watch?v=9E-DfQSZIdU

DEMO - Wireless probing

Sempre su PATREON sono disponibili anche le registrazioni di due LIVE sul tema wireless attack in cui abbiamo analizzato alcuni dati. L'argomento non si esaurisce qui, in preparazione la sessione di attacco.
