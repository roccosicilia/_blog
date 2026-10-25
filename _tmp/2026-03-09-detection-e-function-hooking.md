---
layout:     post
title:      "Detection e function hooking"
date:       2026-03-09 12:00:00 +0100
categories: [cyber-security, hacking, ita]
image:      /assets/images-posts/ida.png
---
L'introduzione fatta ai [concetti di detection](https://roccosicilia.com/2026/03/01/il-concetto-di-detection-e-il-punto-di-vista-offensivo/) mi serviva per iniziare a discutere del funzionamento degli EDR partendo da una base comune di comprensione dell'architettura. Come ho anticipato questi post hanno lo scopo di discutere anche le possibile tecniche di bypass delle logiche di detection con degli esempi pratici e mi baserò molto sul funzionamento di EDR e SIEM.

Un aspetto che ho citato in diverse occasioni è la capacità degli EDR di mettere a disposizione molta telemetria riguardo a ciò che avviene sugli host. Le informazioni vengono raccolte dai sensori attivi sugli endpoint attraverso diverse funzioni, una di queste è il function hooking: gli EDR moderni si "interpongono" tra i programmi e le chiamate di sistema al fine di intercettare le richieste alle funzioni base del sistema operativo (ho iper-semplificato, ma ora vado un po' nel dettaglio).

https://youtu.be/dXu9RfWilZg

Prendiamo una delle funzioni più monitorate dagli EDR: VirtualAlloc, usata per allocare memoria, operazione comunissima nei payload malevoli.

Un flusso normale (senza EDR) potrebbe essere:

<img src="{{ '/assets/images-posts/edr_nohooking.png' | relative_url }}" alt="edr_nohooking" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Il flusso con un EDR attivo potrebbe essere qualcosa di simile:

<img src="{{ '/assets/images-posts/edr_hooking.png' | relative_url }}" alt="edr_hooking" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Quando l'EDR si installa esegue diverse modifiche sul sistema, ad esempio modifica - in memoria - primi byte delle funzioni sensibili in ntdll.dll (la libreria che fa da ponte verso il kernel) sostituendoli con un JMP verso il proprio codice. L'EDR esegue la sua analisi, e se tutto è ok chiama la funzione originale che ha salvato da parte prima di patchare.

Possiamo verificare questa caratteristica degli EDR analizzando il comportamento a runtime di un processo che esegue una *syscall* e la verifica la possiamo fare "in profondità" analizzando il comportamento del processo con un debugger.

---

*Se il mio lavoro di divulgazione ti interessa a vuoi sostenere il mio progetto di ricerca e pubblicazione di articoli e video [puoi supportarmi tramite il mio Patreon](https://patreon.com/roccosicilia).*

---

#### Lab Test: syscall

Ma quanto utile è avere un lab e tutti gli strumenti per approfondire questi temi! Chi si occupa di ricerca pura sono certo che si diverte come un matto ad eseguire questi test :-) nel mio caso di tratta di momenti di studio e ricerca personale che cerco di condividervi e che potete replicare abbastanza facilmente (rif. al tema HomeLab).

Per prima cosa dobbiamo **analizzare il comportamento di un processo su un sistema che non ha un agent EDR installato**. Nel mio lab si tratta della macchina che simula un ambiente desktop Windows 11 che utilizzo anche per la compilazione in ambiente Microsoft.

Nel contesto di laboratorio i sistemi desktop vengono usati, solitamente, con utenti di dominio non privilegiati, ma per il test in questione non è rilevante. Va in ogni caso installato un debugger e per il lab in questione ho deciso di usare IDA Free (v9.3 al momento disponibile, richiede python) che conto di usare anche per altri test che ho in mente di fare. Ovviamente serve anche avere il necessario per compilare un piccolo programma in C, io uso Visual Studio Code sia sul mio laptop che sulla macchina Win11 in questione dove ho anche installato MSYS2 che trovo molto comodo. Voi fate come vi pare.

C'è abbondante documentazione su IDA nel web ma se volete approfittare (come ho fatto il) per un approfondimento sul mondo del *reverse engineering* vi suggerisco un libro per iniziare che mi ha dato qualche base che mi torna ancora utile considerando che io non sono un reverse engineer: "The IDA PRO book" di cui comprai la seconda edizione.

Il codice per il programma di test che dovrà eseguire l'azione di creazione di un file è il seguente:

```
#include <stdio.h>
#include <windows.h>

int main()
{
    // test output
    printf("Programma di test per creazione di un file");

    // crea un file TXT
    HANDLE hFile = CreateFileA(
        "C:\\\\Users\\\\Public\\\\test.txt",
        GENERIC_WRITE,          // scrittura
        0,                      // nessuna condivisione
        NULL,                   // security attributes default
        CREATE_ALWAYS,          // crea sempre, sovrascrive se esiste
        FILE_ATTRIBUTE_NORMAL,  // file senza attributi speciali
        NULL                    // nessun template
    );

    if (hFile == INVALID_HANDLE_VALUE) {
        printf("Errore creazione file: %d\\n", GetLastError());
        return 1;
    }

    // contenuto del file
    const char* contenuto = "test scrittura";
    DWORD bytesWritten;
    
    WriteFile(
        hFile,
        contenuto,
        (DWORD)strlen(contenuto),
        &bytesWritten,
        NULL
    );

    CloseHandle(hFile);
    getchar();

    return 0;
}
```

Compilando ed eseguendo questo programma otterremo la creazione di un file nel path "C:\Users\Public\test.txt" e se ne facciamo il debug potremo osservare la chiamata "pulita" alla *syscall* per la creazione del file: 𝑵𝒕𝑪𝒓𝒆𝒂𝒕𝒆𝑭𝒊𝒍𝒆.

Vi risparmio i singoli passaggi che troverete nel video di sintesi, faccio solo presente che per analizzare cosa avviene a livello di *syscall* bisogna eseguire il debug del programma ed andare a "scartabellare" in quello che succede quando vengono chiamate le funzioni di sistema. Ad un certo punto dell'esecuzione si arriva alla chiamata che ci interessa in quanto è una delle chiamate che, in presenza di EDR, verrebbero intercettate.

<img src="{{ '/assets/images-posts/ida_ntcreatefile_ori.png' | relative_url }}" alt="ida_ntcreatefile_ori" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Quello che si osserva nel comportamento a runtime è una chiamata alla syscall che utilizza il ***syscall number*** "55" che, per la versione di Windows che stiamo usando, corrispondere esattamente a *NtCreateFile*.

---

Piccolo approfondimento sulle *syscall* per capire questo passaggio.

Quando un'applicazione *userland* deve accedere a risorse gestite dal kernel, come il filesystem, la memoria o i socket di rete, non può farlo direttamente. Il processore lavora in due modalità distinte: user mode (ring 3), dove girano le applicazioni, e kernel mode (ring 0), dove opera il sistema operativo.

Questa separazione è un meccanismo di protezione fondamentale: un processo *userland* non può leggere o scrivere memoria del kernel, né invocare direttamente le sue funzioni. Questa netta separazione in Windows nasce con i sistemi operativi NT ed è stato ciò che ha iniziato a dare stabilità al sistema riducendo drasticamente i BSOD.

Il meccanismo che permette ai due domini di interagire è la *system call*: quando un'applicazione deve eseguire un'operazione privilegiata, carica in un registro dedicato (**eax** su architettura x64 come di vede anche nello screenshot) un numero intero che identifica univocamente l'operazione che si vuole eseguire, poi esegue l'istruzione *syscall*. Il processore salva il contesto corrente, eleva il privilegio a ring 0 e trasferisce il controllo al kernel che **legge il numero in eax per determinare quale operazione eseguire**.

Questo numero, il ***syscall number***, è la chiave del meccanismo. Microsoft non rilascia documentazione ufficiale pubblica sui *syscall number*, inoltre questo numero varia tra versioni del sistema operativo. *NtCreateFile*, ad esempio, ha *syscall number* 0x52 su Windows Server 2012 R2, 0x53 su Windows 10 fino alla versione 21H2, e **0x55 su Windows 10 22H2 e Windows 11**. Microsoft si riserva il diritto di modificarlo ad ogni release, motivo per cui il codice che lo usa (il nostro programmino) deve recuperarlo dinamicamente a runtime invece di hardcodarlo. Esistono diversi [progetti che tengono traccia dei syscall number](https://github.com/ikermit/11Syscalls?tab=readme-ov-file) in quanto una delle tecniche di bypass, che personalmente non amo in quanto la trovo parecchio macchinosa, prevedere la chiamata diretta alla funzione desiderata usando il *syscall number* specifico per il sistema operativo su cui stiamo facendo girare il nostro programma.

---

Ora che abbiamo visto cosa succede senza EDR, su un sistema di cui non abbiamo quindi nessuna telemetria, vediamo cosa succedere su una macchina dove abbiamo installato un agente che utilizza il fuction-hooking per raccogliere la telemetria del sistema.

Nota: per questo test non possiamo usare Elastic in quanto l'agente utilizza altre tecniche per registrare la telemetria considerate più difficili da aggirare.

#### Lab Test: hooking

Il comportamento di Elastic lo riprenderò più aventi in quanto per questo test ci è poco utile, infatti se verifichiamo il debug del nostro programma di test troveremo esattamente la stessa situazione - no hooking - ma il dato di telemetria è comunque disponibile sul SIEM.

<img src="{{ '/assets/images-posts/image.png' | relative_url }}" alt="image" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Per osservare quello che avviene quando si esegue una syscall in un sistema in cui l'EDR fa massiccio uso del function hooking bisogna necessariamente selezionare un prodotto che utilizzi abbondantemente questa modalità di registrazione degli eventi ed in particolare, visto il test che stiamo facendo, per la chiamata relativa a *NtCreateFile*.

Non è importante sapere di che EDR si tratta, ai fini del test uno vale l'altro, ciò che conta è confermare la presenza della jump che intercetta la *syscall*:

<img src="{{ '/assets/images-posts/image-1.png' | relative_url }}" alt="image 1" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Come ci si aspettava al posto dei comandi che chiamano la syscall troviamo un'istruzione ***jmp*** il cui scopo è deviare il programma verso il codice dell'EDR, raccogliere la telemetria e successivamente far proseguire il programma richiamando la *syscall* originale per consentire la corretta esecuzione.

Come accennavo nell'introduzione del post questo meccanismo permette all'EDR di registrare tutte le chiamate alle syscall ed i relativi parametri, cosa che da ampia visibilità su cosa fanno i processi che vengono avviati sulla macchina. Non si tratta di per se di un meccanismo di protezione, questi dati servono ad avere una visione globale del comportamento dei processi e possono essere correlati con altri dati per comprendere se quello che si sta osservando è una minaccia oppure no.

#### Aggirare il controllo

Per gli EDR la visibilità sul sistema è tutto: perdere telemetria è la peggio cosa che possa succedere in quanto le regole di detection si basano sulla disponibilità del dato. È quindi abbastanza ovvio che i bad actor siano costantemente alla ricerca di metodologie per aggirare i controlli.

Nel caso del function hooking ci sono diversi metodologie e quella che personalmente ho trovato più elegante prevede l'utilizzo di una copia pulita di ***ntdll.dll***. Considerando che le istruzioni della DLL vengono modificate in memoria (il *jmp* lo aggiunge l'EDR nel codice caricato in memoria) mentre il file originale in ***C:\Windows\System32\ntdll.dll*** non viene modificato, si potrebbe fare in modo che il nostro programma utilizzi le istruzioni della DLL originale invece che della versione patched in memoria.

Il codice che ne deriva è un po' più complesso del precedente e mi sono fatto aiutare da Claude per renderlo leggibile e commentato al meglio.

<img src="{{ '/assets/images-posts/image-2.png' | relative_url }}" alt="image 2" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Il codice è un po' lungo e lo trovate nella repo del mio [progetto HAPpy](https://github.com/roccosicilia/HAPpy) nella directory *demo*.

Su questo programmino ci sarebbero diverse cose da dire ma andiamo troppo fuori tema e rischiamo di aprire una parentesi infinita. Ci basta sapere che codice, oltre a caricare ed utilizzare la DLL da disco, esegue anche la print dei riferimenti della funzione hooked e della funzione "pulita". Seguendo l'esecuzione del codice con IDA si arriva al punto in cui troviamo la ***syscall*** che è un po' di versa da come l'avevamo vista precedentemente:

<img src="{{ '/assets/images-posts/image-3.png' | relative_url }}" alt="image 3" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Questa volta troviamo direttamente le istruzioni della DLL originale (rif. al primo debug del codice di test):

```
4C 8B D1    →  mov r10, rcx
B8 55 00 00 00  →  mov eax, 55h
F6 04 25    →  test byte ptr ...
```

Ora abbiamo la certezza che il programma ha caricato la DLL da disco con le sue istruzioni originali quindi l'EDR non sarà in grado di intercettare la chiamata alla funzione NtCreateFile e non ci sarà telemetria su questo elemento.

Per osservare meglio il comportamento a runtime ho aggiunto n *getchar()* prima della chiamata alla funzione *CleanNtCreateFile()*. In questo modo possiamo avviare il programma che si fermerà, naturalmente, dopo la lettura degli indirizzi di memoria per la funzione NtCreateFile hooked e la funzione NtCreateFile pulita.

<img src="{{ '/assets/images-posts/image-5.png' | relative_url }}" alt="image 5" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Con il programma in pausa "forzata" possiamo riprendere IDA ed agganciare il processo che nel mio caso è *test.exe*. Sapendo l'indirizzo della funzione NtCreateFile pulita possiamo mettere un ***breakpoint*** in questo punto dell'esecuzione (0x400000), in questo modo il debug si fermerà alla funzione pulita prima di eseguirla, cosa che indica che il bypass è avvenuto con successo.

<img src="{{ '/assets/images-posts/image-6.png' | relative_url }}" alt="image 6" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

In caso contrario il programma sarebbe andato alla funzione in memoria ed il breakpoint non sarebbe stato eseguito in quanto si trova in un'area che il programma avrebbe ignorato. In questo caso possiamo dire "missione compiuta": avrete sicuramente riconosciuto il ***syscall number 55*** :-)

Va comunque considerato che questo è un programma di test in laboratorio dove sono presenti diverse *syscall*, la stessa lettura del file da disco richiede chiamate di sistema che vengono ovviamente intercettate in quanto non gestiste dal codice. Un malware pensato per aggirare il function hooking dovrebbe quindi implementare diverse funzioni pulite da utilizzare e sarebbe comunque vincolato alla lettura delle DLL da disco, evento che verrebbe comunque tracciato.

#### Conclusioni

È chiaro che la tecnica, per quanto elegante, richiede la scrittura di molto codice ed una profonda conoscenza del funzionamento del sistema operativo. Inoltre, tema che ho in roadmap per i prossimi post, gli EDR moderni non si basano solo sul function hooking per raccogliere telemetria dal sistema operativo, questo è solo uno dei metodi a disposizione e come abbiamo visto è relativamente semplice da aggirare.

Personalmente ho utilizzato questa parte dello studio come la fase di riscaldamento per iniziare a mettere il naso dentro il funzionamento di questi sistemi ed iniziare a comprenderne meccanismi e limiti e con i prossimi step inizieremo ad analizzare le funzioni più evanzate.

#### Edit: qualche nota aggiuntiva in ordine sparso

Le tecniche di evasione relative al function hooking sono diverse ed in questo post ne ho voluta analizzare una in particolare ma ho pensato di citarne altre che non ho considerato in buona parte anche perché non le ho mai usate attivamente.

Giusto segnalare, anche perché è stata sfiorata nel post, la ***direct syscall*** che come si intuisce ha a che fare con il chiamare la funzione di sistema direttamente tramite il *syscall number*. In questo caso bisogna però sapere a priori quale syscall number chiamare (abbiamo visto che è un parametro che si è documentato) conoscendo a priori la versione del sistema operativo, oppure si può "risolvere dinamicamente" il *syscall number* che ci serve tramite una parte di codice che deve prima indagare questo dato dal sistema operativo (e poi lo può usare dinamicamente nel payload. Questa risulta anche essere la tecnica più utilizzata ed esiste un bellissimo blog post in cui è spiegata in dettaglio [che trovate qui](https://www.mdsec.co.uk/2020/12/bypassing-user-mode-hooks-and-direct-invocation-of-system-calls-for-red-teams/).

La comprensione del tema richiede un po' di background tecnico sul funzionamento dei sistemi operativi, in particolare Windows in questo caso, qualche nozione di C e di Assembly. Per quanto mi riguarda ho una buona base di conoscenza dei sistemi operativi, diciamo che sono abbastanza in intimità con Linux e Windows (versioni relativamente recenti). Lato C ho una conoscenza di base che mi permette di comprendere il codice scritto da altri, talvolta con il supporto della documentazione se il programma è complesso, mentre sulla scrittura di codice sono in grado di creare programmi molto semplici dove applico atomicamente quello che mi serve. Per Assembly ho una conoscenza di base delle istruzioni e di come interpretare il flusso di un programma limitatamente alle architetture intel x86, 32 e 64 bit. Questo mi ha permesso di comprendere il tema discusso, elaborarne potenzialità e limiti e creare delle demo per ottenere il bypass dopo aver studiato l'argomento. Ho voluto esplicitare le competenza a cui ho dovuto attingere o che ho dovuto rinforzare per darvi una sorta di elenco dei requisiti necessari per esplorare in modo sufficientemente esaustivo la tematica.

Lo si può fare senza un background? Diciamo di sì (sapete che non amo gli assoluti) ma con dei grossi asterischi nel senso che ci saranno dettagli che non capirete e dovrete accettare dei dogmi, cosa poco sensata in un contesto scientifico (sì, l'informatica è una scienza).

Come ulteriore risorsa per il mondo del reversing e [vi suggerisco un bel video del buon Leorando](https://www.youtube.com/watch?v=fgmFLSoVwHA) che fa una bella introduzione al tema con un task di CrackMe. Come vi suggerisco anche le sue lezioni di C.
