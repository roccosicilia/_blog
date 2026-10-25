---
layout:     post
title:      "Pivoting: prove in lab"
date:       2022-07-03 01:48:44 +0200
categories: [hacking, ita]
image:
---
Ci sono molti scenari che varrebbe la pena di provare, in questa sessione, con riferimento alla Twitch Live del 17 giugno, partiamo dalla base di questa tecnica.

<img src="{{ '/assets/images-posts/image.png' | relative_url }}" alt="image" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

net schema

La struttura del lab base è molto semplice ma ben mette in evidenza l'utilità della tecnica in se. Lo schema mostra, da sinistra verso destra, il laptop del potenziale attacker posizionato sul segmento di rete di un server Windows (ws1) di cui abbiamo le informazioni di base restituite dalla scansione nmap:

<img src="{{ '/assets/images-posts/image-4.png' | relative_url }}" alt="image 4" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

nmap

Oltre il primo server Windows vi è un altro sistema, anch'esso Windows con hostname ws2, che condivide una rete con ws1 ma non con il sistema dell'attacker che in questo esempio è la più classica delle Kali.

Ciò che vogliamo ottenere è "toccare" il sistema ws2 passando per ws1 utilizzando appunto l'arsenale che abbiamo a disposizione sul sistema dell'attacker. Non potendo comunicare direttamente con ws2 dobbiamo prima accedere a ws1 per utilizzare la macchina come "ponte" per le nostre azioni. Per prima cosa dobbiamo guadagnarci un accesso al sistema ws1; in questo semplice lab abbiamo utilizzato O.S. volutamente vulnerabili per praticità ed in particolare le macchine presentano la vulnerabilità a tutti nota per il famigerato exploit EternalBlue:

<img src="{{ '/assets/images-posts/image-5.png' | relative_url }}" alt="image 5" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

set exploit in metasploit

Senza dilungarci troppo sull'utilizzo di metasploit (mi avete già in molti chiesto una sessione su questo strumento, la preparerò), utilizzeremo la vulnerabilità CVE-2017-0144, che consente una Remote Code Execution (RCE) sul sistema target al quale faremo eseguire uno specifico payload: una reverse shell di meterpreter.

<img src="{{ '/assets/images-posts/image-6.png' | relative_url }}" alt="image 6" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

conf. payload

La configurazione delle opzioni del payload è in questo caso molto semplice, è infatti sufficiente definire l'IP del target ed essere certi di essere su un segmento di rete che il target possa raggiungere direttamente per consentire alla sessione della reverse shell di instaurarsi. Il comando per definire l'host target è il seguente:

```
set rhost <IP>
```

Come ultima azione con il comando "run" verrà lanciato l'exploit:

<img src="{{ '/assets/images-posts/image-7.png' | relative_url }}" alt="image 7" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

esempio tratto da un altro lab. con la stessa vulnerabilità

Meterpreter mette a disposizione moltissimi comandi/strumenti che possono essere eseguiti sulla macchina target, ne cito alcuni:

- load: consente di avviare/caricare ulteriori plugin e relative funzionalità (es kiwi)
- ps: presenta l'elenco dei processi attivi sulla macchina target
- clearev: cancella gli eventi dai registri della macchina target
- shell: accede alla command shell della macchina target
- ipconfig: visualizza le configurazioni delle NIC della macchina target

Una volta ottenuto un accesso sul sistema target è necessario ottenere rapidamente informazioni di base come la configurazione di rete del sistema. Con il comando ipconfig possiamo visualizzare la configurazione delle NIC a bordo macchina. Il sistema presenta, come capita spesso, più device di rete, ma in questo caso ci interessano solo i device associati alle reti locali:

```
meterpreter > ipconfig
Interface 11
============
Name         : Connessione di rete Intel(R) PRO/1000 MT
Hardware MAC : 00:0c:29:34:1e:11
MTU          : 1500
IPv4 Address : 192.168.1.10
IPv4 Netmask : 255.255.255.0
[...]
Interface 16
============
Name         : Connessione di rete Intel(R) PRO/1000 MT #2
Hardware MAC : 00:0c:29:34:1e:1b
MTU          : 1500
IPv4 Address : 192.168.19.163
IPv4 Netmask : 255.255.255.0
IPv6 Address : fe80::356c:5658:599c:5774
IPv6 Netmask : ffff:ffff:ffff:ffff::
```

L'interfaccia 11 è configurata sullo stesso dominio di broadcast della macchina da cui stiamo simulando gli attacchi (192.168.1.0/24) e la macchina target presenta almeno un'altra subnet configurata: 192.168.19.0/24. Questa subnet non è raggiungibile direttamente dal sistema Kali in quanto non abbiamo un gateway che ci consenta di raggiungere la porzione di rete individuata.

<img src="{{ '/assets/images-posts/image-8.png' | relative_url }}" alt="image 8" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

conf. di rete dell'attacker: la seconda network non è raggiungibile direttamente

Essendo un'intera /24 è plausibile ipotizzare che vi siano altri endpoint all'interno del segmento di rete ed è quindi utile indagare ulteriormente. Alcune informazioni possono essere rilevate direttamente dalla macchina target con semplici comandi locali: è probabile che il sistema a cui abbiamo avuto accesso abbia fatto traffico verso altri sistemi della rete e ne potremmo trovare traccia nella arp-table:

<img src="{{ '/assets/images-posts/image-9.png' | relative_url }}" alt="image 9" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

arp cache tramite il comando "arp"

Dalle informazioni in nostro possesso possiamo ipotizzare che vi siano effettivamente altri sistemi sulla rete "interna" ed è quindi utile indagare ulteriormente attraverso una scansione di rete. Per eseguire questa operazione dovremmo poter lanciare la scan dalla macchina compromessa in quando ha diretta visibilità della rete. Questa operazione, per quanto fattibile, non è particolarmente comoda. Il pivoting ci consente di utilizzare la macchina "esterna" come ponte per la rete interna esattamente come farebbe un router. Con il comando "background" possiamo uscire dalla sessione di meterpreter senza chiuderla ed aggiungere una nuova rotta al solo sistema affinché la rete 192.168.19.0/24 sia raggiungile a Level 3.

<img src="{{ '/assets/images-posts/image-10.png' | relative_url }}" alt="image 10" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

session background

Il comando per aggiungere la rotta è "route add":

<img src="{{ '/assets/images-posts/image-11.png' | relative_url }}" alt="image 11" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

route add

Una volta definita la sessione da utilizzare per instradare il traffico (la reverse shell in questo caso) è possibile eseguire azioni direttamente verso la macchina interna. Un modulo comodo potrebbe essere il portscan per eseguire ulteriori scansioni all'interno della rete:

```
> use auxiliary/scanner/portscan/tcp
> set RHOSTS 192.168.19.170-179
> set PORTS 445
> run
```

Una volta lanciata la scansione (potrebbe richiedere un po' di tempo) verranno riportati i risultati direttamente nell'output di metasploit:

<img src="{{ '/assets/images-posts/image.png' | relative_url }}" alt="image" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

scan attraverso la sessione meterpreter

Nel caso specifico la scansione ha individuato un sistema raggiungibile dalla macchina compromessa con il 192.168.19.175 con la porta 445 in ascolto. Una prova per verificare questo risultato potrebbe essere un tentativo di comunicazione dalla macchina target, sarà sufficiente tornare nella sessione meterpreter relativa:

<img src="{{ '/assets/images-posts/image-1.png' | relative_url }}" alt="image 1" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

ping internal host

Il risultato dell'operazione è quindi la possibilità di eseguire azioni sulla macchina interna alla rete sfruttando il canale aperto della sessione meterpreter sul sistema di "periferia".

La tecnica consente di proseguire nelle azioni di ricognizione da una posizione estremamente comoda: se la visibilità della rete lo consente il sistema potrebbe essere utilizzato per individuare apparati interni come network appliance o altri device, con il semplice comando "arp" possiamo farci un'idea dei sistemi con cui la macchina target comunica così da tentare di ricostruire una topologia.

Di solito è normale che i sistemi interni di una rete siano in grado di comunicare tra loro. Questa tecnica ci ricorda però quanto sia indispensabile la segregazione con particolare riferimento alle policies che devono, di fatto, bloccare il traffico proveniente da reti "untrusted". In uno scenario come quello analizzato la visibilità tra una ipotetica rete DMZ e la rete LAN rappresenterebbe un reale problema: concedere ai sistemi "esposti" di dialogare direttamente con i sistemi interni porta inevitabili rischi per la sicurezza cyber.

Il passaggio successivo è solitamente quello di mantenere una presenza all'interno della rete target senza dover eseguire ripetutamente l'exploiting della macchina vulnerabile. Questa parte del laboratorio, con la relativa costruzione di un rudimentale C2, è stata trattata nelle live di fine giugno per le quali scriverò un altro post dedicato.
