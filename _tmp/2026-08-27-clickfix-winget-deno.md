---
layout:     post
title:      "ClickFix + winget + Deno"
date:       2026-08-27 10:34:24 +0200
categories: [cyber-security, hacking, ita]
image:      /assets/images-posts/create-a-featured-image-for-a-blog-post-titled-homelab.png
---
#### Intro

Di ClickFix è molto probabile che se ne sia sentito parlare: l'attaccante crea pagine che propongono dei finti CAPTCHA con cui si induce l'utente ad eseguire un'azione sul proprio sistema per "risolvere il task" ed ottenere così l'accesso ad un sito/risorsa dimostrando di non essere un Bot.

Ne avevo parlato in questo post analizzando il comportamento degli stage ed i payload successivi alla prima azione:

[<img src="{{ '/assets/images-posts/image-4.png' | relative_url }}" alt="image 4" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />](https://roccosicilia.com/2026/02/17/analisi-di-un-c2-per-osx/)

In occasione di questo nuovo post volevo invece discutere uno scenario relativamente facile da realizzare e particolarmente subdolo che riguarda il mondo Microsoft Windows.

Di base tramite ClickFix l'attaccante induce l'utente a digitare dei comandi sulla propria postazione e molto spesso si tratta di un comando powershell offuscato o encoded:

```
powershell -enc <base64string>
```

Alcuni EDR possono presentare delle regole di detection (by design) sull'utilizzo di questa sintassi e paradossalmente mi è capitato di poter eseguire senza tanti problemi piccoli script/comandi non encoded, dipende dal contesto operativo e dal livello di attenzione degli analisti ad eventuali segnalazione non critiche da parte dei sistemi di detection.

Come detto in diverse occasioni ed in alcuni lab/video la capacità di detection degli EDR dipende da quanta telemetria sono in grado di raccogliere e dalle regole di correlazione attive. Nel blog trovate diversi post in merito.

---

Se trovi interessanti i miei contenuti e vuoi supportare il mio progetto di divulgazione puoi iscriverti al blog ed alla mia [newsletter](https://roccosicilia.substack.com):

---

Ad ogni modo la stringa solitamente contiene un set di comandi molto semplice come primo "stage" del tentativo di compromissione del sistema. Alcuni gruppi tentano di installare sul sistema locale delle componenti aggiuntive per eseguire poi script sul sistema riducendo la possibilità di essere intercettati dall'EDR e contando sul fatto che non ci siano regole di detection pensate per questa casistica.

Un caso molto interessante che mi ha appassionato, analizzato da [Sophos](https://www.sophos.com/en-us/blog/deno-case-studies) e di cui ho trovato delle interessanti riflessioni a livello di metodologia su [CyberPress](https://cyberpress.org/dindoor-evades-security-tools/), si riferisce all'utilizzo di ***Deno***, una runtime JS che consente di eseguire codice javascript e typescript sul sistema target.

Come sottolineato proprio da CyberPress:

> Because Deno is a legitimate developer tool, its execution often bypasses behavioral alerts, creating a dangerous blind spot for defenders in environments where monitoring is strictly tuned for PowerShell or Python.

È assolutamente vero che PowerShell è uno degli strumenti più sorvegliati e anche Python (che io uso molto) comincia ad essere controllato. Ovviamente se i bad actor si spostano su altri tools leciti per veicolare i proprio script malevoli bisogna adeguare gli strumenti di detection alle nuove varianti.

#### Struttura dell'attacco

Come ho spesso raccontato, nella mia chain utilizzo spesso Python per eseguire comandi sul sistema target ed in passato ho usato molto PowerShell nella stessa modalità. Il motivo è sempre lo stesso: meno "rumore", meno "detection".

Con queste premesse diventa relativamente semplice creare una "sequenza" di attacco secondo il seguente flow:

- Campagna ClickFix con un payload PowerShell che installa *Deno* tramite *winget* ed esegue un set di comandi TypeScript.
- Avvio del client del C2 scritto in TypeScript con le informazioni di contesto utili alle primissime azioni sul sistema: possibilità di comunicare, possibilità di accedere alle risorse locali.
- Una volta aperto il canale C2 si possono impartire comandi alla macchina invocando PowerShell dal TypeScript.

La detection di questo tipo di minaccia è molto complessa in quanto si basa sull'utilizzo di tools leciti e considerati non malevoli perché di fatto sono strumenti di uso comune. È interessante notare che nella "stramenzionata" [MITRE Enterprise Matrix](https://attack.mitre.org/techniques/T1105/) tools come winget sono già stati mappati come utilizzati/abusati dai bad actor:

<img src="{{ '/assets/images-posts/winget.png' | relative_url }}" alt="winget" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Considerando il "flusso" che l'attacco richiede è sicuramente possibile valutare dei meccanismi di detection dedicati: è possibile analizzare il contesto in cui *winget* viene chiamato come è possibile valutare di analizzare l'utilizzo di scripting sui sistemi, come già lo si fa per PowerShell e Python, anche per Deno con JS e TypeScript.

#### Demo

Assieme al blog post esce anche un video in cui spiego e mostro alcuni dettagli della tecnica in un contesto di laboratorio:

https://youtu.be/ZinB9F0gwFQ

Se si dispone di una infrastruttura C2 con un minimo di integrazioni diventa relativamente semplice costruire un payload da eseguire con Deno. Come in altre occasioni sfrutto il lab che utilizzo abitualmente per fare una piccola demo.

La componente server è sempre quella del mio progetto [HAPpy](https://github.com/roccosicilia/HAPpy):

[<img src="{{ '/assets/images-posts/c2_server.png' | relative_url }}" alt="c2_server" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />](https://github.com/roccosicilia/HAPpy)

Questo progetto nasce con un payload in python che gestisce la comunicazione con il C2 e l'esecuzione dei comandi locali. In questa occasione questa componente viene riscritta in TypeScript: il funzionamento non cambia ma cambia il linguaggio e l'interprete, quindi un eventuale EDR riceverebbe informazioni in merito a processi *deno.exe* in esecuzione sul sistema.

La riscrittura del payload l'ho delegata a Claude (non conosco TypeScript) che mi ha proposto una prima versione parzialmente funzionante. Una volta capita la struttura del linguaggio è stato facile correggere gli errori ed ottenere lo stello comportamento della versione in python senza modificare nulla a livello server.

Una volta avviato lo script sul client il funzionamento è quello classico: il programma avvia il ciclo all'interno del quale vengono eseguire le chiamate HTTP per leggere i comandi dal C2, eseguirli localmente ed inviare l'output nuovamente al C2 che lo visualizza in *console*.

<img src="{{ '/assets/images-posts/c2_demo_types.png' | relative_url }}" alt="c2_demo_types" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Sul piano funzionale tutto fila liscio ed è interessante analizzare cosa è visibile a livello EDR, ma questo tema lo sviluppo in un prossimo post.

#### Conclusioni

ClickFix è una minaccia veramente insidiosa e fastidiosa, va sicuramente inserita della formazione agli utenti come è stato fatto per il phishing. Sappiamo bene che generare consapevolezza richiede tempo e lato IT non possiamo permetterci di aspettare. Qualche contromisura va messa in campo prima.
