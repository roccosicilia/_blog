---
layout:     post
title:      "Non trascurare la raccolta delle informazioni: port scan."
date:       2024-11-09 09:00:00 +0100
categories: [hacking, ita, study-with-me]
image:      /assets/images-posts/nmap-scan.png
---
Molte tipologie di test di sicurezza, sia in contesti offensivi che in attività di controllo periodico, si basano su un set di informazioni che preleviamo direttamente dai sistema. il concetto è semplice: più ho dettagli rispetto al mio target e meglio posso valutarne le possibili vie per attaccarlo e, di conseguenza, ipotizzare strategia di riduzione dei rischi.

In questo post tocco un elemento puramente tecnico di questo processo: la scansione delle porte disponibili. Mettiamoci nei panni del Threat Actor che per capire dove colpire, ipotizzando un perimetro prettamente informatico, deve necessariamente identificare i servizi esposti. Di solito l'azione richiede due macro-fasi: una scansione passiva del perimetro, che ci permette anche di identificarne i "confini" del target, seguita da una scansione attiva che dovrebbe permetterci di ottenere un elenco di host (server o dispositivi di altra natura) e di "porte". Ogni porta corrisponde ad un servizio, un elemento software che ci permette di comunicare con il dispositivo che la espone.

La "porta logica" ed il servizio che la utilizza sono da considerarsi elementi potenzialmente sfruttabili. Il task procede quindi con l'identificazione del servizio e la verifica di eventuali vulnerabilità note. In questo processo è evidente che se, per qualche ragione, l'elenco delle porte rilevate è incompleto, ci stiamo giocando delle possibilità di attacco. Questo task, che tecnicamente è semplicissimo, deve essere approcciato con la stessa cura di qualsiasi altra fase offensiva.

In contesti in cui l'amministratore ha configurato i propri servizi per essere esposti su porte non standard (pratica diffusa) rischieremmo di perderci dei pezzi se non utilizziamo le opportune tecniche di scansione.  
Contemporaneamente dobbiamo fare i conti con il tempo a disposizione che solitamente non è infinito: chiunque si sia mai azzardato a lanciare una scansione su tutte le porte con il nostro amico ***nmap*** sa che l'operazione potrebbe richiedere tempo.

Ogni servizio merita di essere considerato singolarmente, in questa occasione preoccupiamoci sono di accertarci di trovare tutto quello che è effettivamente esposto in rete. Un possibile approccio è partire dalle porte effettivamente aperte senza preoccuparsi subito di capire cosa c'è dietro. Con ***netcat*** possiamo eseguire richieste tcp ed udp molto semplici e, in base alla risposta possiamo dedurre lo stato della porta remota.

```
nc -nvv -w 1 -z 192.168.1.1 80
(UNKNOWN) [192.168.1.1] 80 (http) open
sent 0, rcvd 0
```

Il tempo di attesa per la singola porta è molto basso, possiamo quindi chiedere un range anche molto ampio ed ottenere il risultato in poco tempo, sicuramente in meno tempo rispetto ad ***nmap***.

```
nc -nvv -w 1 -z 192.168.1.1 1-20000 > output.txt 2>&1
...
```

Ovviamente non avremo particolari dettagli sui servizi ma in pochi minuti ci saremo fatti un'idea delle porte disponibili. L'output non è particolarmente comodo da utilizzare, conviene mettere tutti in un file e a colpi di ***grep*** cercare le porte aperte (open).

Ora è il turno di nmap con i suoi script a cui possiamo chiedere di darci una prima idea di quello che c'è dietro le porte aperte. Avendo sono un set specifico di porte da analizzare possiamo permetterci di fare scansioni anche molto approfondite.

```
nmap -sS -sC -sV -p 80,443,2222 -oN nmap.txt 192.168.1.1
```

Anche in questo caso conviene conservare l'output in un file da analizzare con calma e su cui fare ulteriori approfondimenti. Come accennavo ***nmap*** ci da molte informazioni ma resta un tool generico, per ogni servizi individuato dovremo fare un ulteriore passaggio di enumeration con tools specifici.

Ho raccolto qualche appunto sulla scansione del enumerazione dei servizi in questa repo: <https://github.com/roccosicilia/OSCP_cheatsheet/tree/main>.
