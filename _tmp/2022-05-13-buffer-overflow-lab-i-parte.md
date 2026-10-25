---
layout:     post
title:      "Buffer Overflow lab [I parte]"
date:       2022-05-13 09:00:00 +0200
categories: [cyber-security, hacking, ita]
image:
---
Premessa doverosa: tratto il tema perché mi piace e appassiona molto ma non sono certo un esperto, mi rivolgo quindi a chi come me è affascinato dall'argomento ed ha interesse ad approfondire passando per un esercizio pratico.

Durante una sessione live di qualche settimana fa (l'argomento era una simulazione di attacco) si è un po' discusso e sono emerse domande circa lo sfruttamento delle vulnerabilità e le tecniche di exploiting. Ho quindi pensato di dedicare una live (ma ne serviranno almeno due) all'argomento con lo scopo di semplificare il semplificabile e fare qualcosa di molto pratico. La live di giovedì 5 maggio, ancora disponibile sul mio **[canale Twitch](https://www.twitch.tv/roccosicilia)**, introduce quindi l'argomento con un piccolo laboratorio estremamente realistico che chiunque può replicare. In questo post provo a mettere "in fila" i vari step visti durante la prima parte in live.

## Intro: un grammo di teoria

Resistete, sono due cose ma fondamentali. Dobbiamo necessariamente capire come si manifesta un buffer overflow. Partiamo da un esempio molto semplice ed immaginiamo un programma base che ha una funzione `main()` dove avvengono "cose" ed una funzione `task()` che fa altre "cose":

```
int main() {
    task();
    other_task();
}

int task() {
    char buff[42];
    ...
}
```

Cose succede nella memoria del nostro elaboratore quando un programma come questo viene eseguito? L'area di memoria interessata è chiamata stack (pila) perché si comporta proprio come una pila di byte nel momento in cui viene riempita di informazioni.

<img src="{{ '/assets/images-posts/image-3.png' | relative_url }}" alt="image 3" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Sul "fondo" viene posizionata la funziona `main()` e le relative variabili locali, subito sopra si trova l'area di memoria che contiene l'indirizzo a cui andare per tornare alla funzione `main()` ed infine l'area dedicata alla funzione `task()`.

Ciò che avviene quando il programma viene eseguito è sintetizzabile con i seguenti step:

1. la funzione `main()` viene eseguita
2. viene chiamata la funzione `task()`
3. viene salvato il **return address** nel registro così da riprendere la funzione `main()` da dove si è fermata una volta eseguita la funzione `task()`
4. viene eseguita la funzione `task()`
5. viene letto il valore del **return address**
6. il programma prosegue dall'istruzione successiva alla chiamata della funzione `task()`

Se tutto procede senza errori il programma terminerà con successo. In questo passaggio è importante comprendere che durante l'esecuzione della funzione `task()` l'area di memoria allocata dipende dalle esigenze della funzione in termini di "consumo". Come si nota dallo pseudo-codice la variabile `buff[42]` è un array che può contenere 42 elementi. Cosa succederebbe se provassimo a scrivere 200 caratteri e non controllassimo questo evento a livello di codice?

<img src="{{ '/assets/images-posts/image-5.png' | relative_url }}" alt="image 5" style="float: left; width: 400px; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Il contenuto del registro dove era stato salvato il **return address** viene sovrascritto ed il programma tenterebbe di riprendere da una posizione di memoria (*AAAA* nell'esempio) inesistente o non valida con relativo crash.

## Exploiting

Capita la teoria vediamo come è potenzialmente sfruttabile questo meccanismo. Se potessimo controllare il valore del return address potremmo indirizzare il programma altrove ed eseguire le istruzioni presenti in altre aree di memoria. Con la stessa logica se potessimo scrivere istruzioni arbitrarie, invece delle "AAAA...", nelle aree di memoria disponibili potremmo impostare il return address così da eseguire un *jump* esattamente dove sono state posizionate le nostre istruzioni arbitrarie.

<img src="{{ '/assets/images-posts/exploit_shellcode.png' | relative_url }}" alt="exploit_shellcode" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Per ottenere questo risultato dobbiamo ovviamente sapere quanti byte scrivere nelle differenti aree di memoria. Ci serve quindi calcolare l'esatta dimensione del buffer, l'esatta posizione del registro EIP che contiene il citato return address ed infine l'inizio e la fine dalla successiva area di memoria.

Per ottenere tutte queste informazioni bisogna lavorare un po' di debug e qualche calcolo esadecimale. Il modo migliore per comprenderlo è vederlo dal vivo, quindi il prossimo step è mettere le mani in pasta in un lab.

## Lab Setup

Come accennato ad inizio post il laboratorio in questione ha il vantaggio di essere molto il linea con la realtà. Abbiamo un sistema che ospita un'applicazione vulnerabile la quale espone un servizio contattabile remotamente. Per mettere in piedi il sistema target dobbiamo quindi semplicemente predisporre una VM con sistema operativo Windows e scaricare l'applicazione vulnerabile.

Una volta preparata la vostra VM target dovete procurarvi l'applicazione che presenta la vulnerabilità: <https://github.com/stephenbradshaw/vulnserver>. Di base è un eseguibile che può essere lanciato direttamente dal prompt dei comandi:

<img src="{{ '/assets/images-posts/vulnserver.png' | relative_url }}" alt="vulnserver" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Abbiamo quindi la nostra applicazione avviata e pronta a ricevere delle connessioni. Per fare qualche prova e come base anche per le successive operazioni di analisi possiamo usare la solita Kali che ci darà un mano anche successivamente grazie ad alcuni tools comodi. In questo scenario è necessario che le due VMs siano in comunicazione. Nel mio laboratorio condividono anche la stessa network ma non è un requisito.

## Testing dell'applicazione

Dalla nostra Kali possiamo quindi provare a connetterci al server che risponde sulla porta 9999 utilizzando semplicemente netcat:

```
nc 192.168.1.7 9999
```

Il risultato dovrebbe essere qualcosa di simile:

<img src="{{ '/assets/images-posts/nc2vulnserv.png' | relative_url }}" alt="nc2vulnserv" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

A sinistra la sessione netcat, a destra la console del servizio.

Il servizio mette a disposizione diversi comandi in grado di ricevere dei valori. Nel caso specifico noi sappiano già qual è la funzione vulnerabile mentre in una situazione reale l'analista dovrebbe andare a caccia prima di tutto della vulnerabilità o del bug da sfruttare. In questa sessione non tocchiamo il tema *bug hunting* quindi ci limitiamo a saltare al momento in cui, tramite una tecnica molto usata che è il [fuzzing](https://en.wikipedia.org/wiki/Fuzzing), scoviamo il bug nella funziona TRUN del programma.

Mettiamoci quindi per un attimo nei panni del bug hunter (tra l'altro attività meravigliosa che richiede molta abilità) che arriva al test del comando TRUN del server ed utilizziamo un tool della nostra Kali: *generic_send_tcp*. Questo piccolo software ci consente di creare ed inviare pacchetti TCP al target per vedere cosa succede, dobbiamo prima definire le istruzioni da passare al programma che possiamo mettere in un file di configurazione che io chiamerò fuzz.spk:

```
s_readline();
s_string("TRUN ");
s_string_variable("FUZZ");
```

Il file ha tre semplici direttive abbastanza chiare:

- leggiamo l'output del server così da vedere cosa risponde alle nostre sollecitazioni
- chiamiamo il comando TRUN
- "spariamo" del contenuto per vedere come reagisce

Una volta pronto il file con le configurazioni possiamo fare fuoco:

```
generic_send_tcp 192.168.1.7 9999 fuzz.spk 0 0
```

Dovremmo ottenere il crash dell'applicazione sul server Windows:

<img src="{{ '/assets/images-posts/vulnserv_crash.png' | relative_url }}" alt="vulnserv_crash" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

A sinistra lo script di fuzzing in esecuzione, a destra il servizio andato in crash.

Il programma va in crash e abbiamo quindi la conferma del bug. Nel nostro caso sappiamo già essere un buffer overflow e in questo lab ci comporteremo di conseguenza cercando questo specifico comportamento.

## Analisi della memoria

Abbiamo un servizio che va in crash se sollecitato in un certo modo... andiamo a vedere cosa succede in memoria quando si verifica il crash. Per questo lab utilizzo sulla macchina Windows il software Immunity Debugger; è una scelta di comodo che assolve al compito specifico di farci vedere cosa viene caricato in memoria quando il programma è in esecuzione e quando va in crash.

Immunity consente di avviare il servizio direttamente dalla propria interfaccia così da "pilotarne" ed analizzarne i singoli step, anche una istruzione alla volta. Avviamo quindi il servizio da Immunity ed avviamo il servizio:

<img src="{{ '/assets/images-posts/immunity-1.png' | relative_url }}" alt="immunity 1" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Sulla destra troviamo lo stato dei registri del processore e in questa fase è interessante vedere che, oltre a non esserci errori, il registro EIP contiene una posizione di memoria che corrisponde a dove "mandare" il puntatore delle istruzioni una volta eseguita l'istruzione in gestione. E' quini il **return address** di cui si parlava prima.

Vediamo cosa succede quando lanciamo il nostro fuzzer e mandiamo in crash il programma:

<img src="{{ '/assets/images-posts/immunity-2.png' | relative_url }}" alt="immunity 2" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Su questo screenshot si potrebbe parlare per diverse ore. Cosa sta succedendo?

Subito in cima vediamo chiaramente la nostra richiesta: la chiamata alla funzione TRUN arriva direttamente da nostro fuzzer e subito dopo vediamo i valori passati alla funzione, una serie di caratteri "A".

Altro elemento da notare è il contenuto dell'area a cui punta il registro **ESP**, porzione di memoria destinata alle variabili locali del programma in esecuzione. Anche qui vediamo una serie di caratteri "A".

Infine, forse l'elemento più interessante, il contenuto del registro **EIP**: 41414141 ovviamente esadecimale. A cosa corrisponde 41 esadecimale? Al carattere "A". Interessante! **Le "A" che abbiamo sparato con il fuzzer sono andate praticamente dappertutto**: hanno riempito la porzione di memoria destinata alle variabili della funzione, hanno sovrascritto il registro EIP e sono arrivate a riempire l'area di memoria destinata alle variabili del programma. Quale delle precedenti immagini vi ricorda? Siamo chiaramente davanti ad un **buffer overflow**.

---

Per questa prima parte mi fermo qui. Nella seconda parte vediamo come manipolare in modo preciso il contenuto dei registri ed iniziare a scrivere il nostro **exploit** ora che abbiamo individuato la vulnerabilità.
