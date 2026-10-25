---
layout:     post
title:      "Esercizi su DNS recon"
date:       2025-06-23 23:42:42 +0200
categories: [cyber-security, hacking, ita, study-with-me]
image:      /assets/images-posts/ejpt_copertina.png
---
Sul canale Patreon, come annunciato qualche settimana fa, sto pubblicando una serie di video con i [miei appunti relativi ai temi della eJPT](https://www.patreon.com/collection/1375290?view=expanded). Per ogni video condivido degli esercizi pratici con l'obiettivo di far pratica con i concetti che racconto e di cui scrivo nei post di approfondimento. Sul tema della DNS recon ho già scritto in passato, qui riporto la "soluzione" agli esercizi proposti nel video.

#### Esercizio 1: record SRV

I record SRV vengono utilizzati per identificare specifici servizi tramite precise informazioni inserire nel record. Il tool *dnsrecon* può essere utile a tale scopo.

```
$ dnsrecon -d microsoft.com
```

La richiesta consente di individuare diversi record DNS tra cui quelli relativi ai servizi.

<img src="{{ '/assets/images-posts/image-12.png' | relative_url }}" alt="image 12" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

dnsrecon output

Rispetto ai record "A" si ha qualche informazione in più in merito all'host definito nel record, ammesso che si tratti di hosts ancora in uso.

#### Esercizio 2: intere subnet dichiarate come SPF

Come discusso nel video della sessione, in alcuni casi chi si occupa della configurazione della zona DNS e dei relativi record non sempre mantiene le configurazioni "pulite". Le attività di DNS recon puntano ad individuare nuovi host della rete target: trovare quindi configurazioni DNS che dichiarano intere subnet è, dal punto di vista dell'attacker, un vantaggio non trascurabile.

```
dig TXT nomedominio.xyz | grep -i spf1
```

#### Esercizio 3: DNS multi uso

Domanda bonus: come può essere utilizzato il servizio DNS in un contesto C2? Ci sono diverse tecniche che consentono di utilizzare le query DNS come mezzo di comunicazione tra un host compromesso ed il C2 server.

Un trucco abbastanza semplice è utilizzare i record TXT per posizionare online dei contenuti, ad esempio dei comandi powershell o bash all'interno del record. Per eseguire i comandi localmente l'utente devo solo "scaricare" il contenuto del record in una variabile e poi passarlo come comando locale.

```
$ dig TXT bithorn.org|grep -i test
bithorn.org.   422  IN  TXT	"TEST_CONTENT_LABZ"
```

Il comando *dig* interroga il DNS, in questo esempio ho volutamente cerato un record TXT che contenesse la stringa "test". Con lo stesso principio possiamo cercare un record specifico al cui interno abbiamo posizionalo la stringa di un comando e salvarla in una variabile.

```
TEST=$(dig TXT bithorn.org|grep -i test|awk '{print $5}')
```

Una volta "raccolto" il comando tramite la query possiamo chiedere allo script di eseguirlo localmente.  
In un prossimo post di approfondimento dedico un po' di spazio al tema e parliamo anche di come inviare gli output sempre via DNS.

---

Il video completo è disponibile sul mio canale Patreon:

[<img src="{{ '/assets/images-posts/image-13.png' | relative_url }}" alt="image 13" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />](https://www.patreon.com/posts/ejpt-02-passive-130528250)

video completo su DNS recon.

---

#### Prossimo video

In programma per la prossima sessione ho messo la parte di Web Application Firewall e le tecniche di subdomain enumeration, in parte anticipate in questa sessione.
