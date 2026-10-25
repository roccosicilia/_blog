---
layout:     post
title:      "EDR lab: piccolo self-test #1"
date:       2024-08-10 13:00:00 +0200
categories: [cyber-security, hacking, ita]
image:      /assets/images-posts/blue-team.png
---
## Introduzione

Devo fare diverse premesse per questo post e parto dall'inizio. Da circa un paio di anni ho introdotto nei miei security test attività che richiedono di eludere sistemi/servizi di sicurezza, in particolare EDR/IDS e team SOC/MDR. Il tema mi appassiona molto ed ho cercato di approfondire alcune tecniche utili allo scopo, non ho quindi approfondito l'enorme tema dell'evasion degli EDR (argomento fantastico su cui mi sto documentando con calma e nel tempo) ma mi sono limitato a studiare alcune tecniche utili ad aggirare i principali controlli che possono essere attivi sui sistemi operativi client e a livello di sonde di rete.

L'ambito EDR mi aveva particolarmente appassionato ed avevo giocato con piccoli fileless malware da utilizzare in diverse occasioni. In particolare, sempre in riferimento alle mie esigenze operative, ho approfondito un po' il tema *exfiltration*, *covert channel* e *command and control*. Nei miei lab, alcuni dei quali fatti durante lunghe live su [Twitch](https://twitch.tv/roccosicilia) (archivio oggi disponibile su [Patreon](https://patreon.com/roccosicilia)), ho sperimentato varie tecniche e strumenti tra cui dei framework C2; uno di questi è stato Villain in quanto molto semplice da usare, personalizzabile e di semplice riproduzione, elemento che prendo spesso in considerazione per la parte divulgativa dei miei contenuti.

Sul piano professionale ho sempre fatto notare che gli EDR/XDR hanno bisogno di un certo grado di gestione: questi strumenti sono molto potenti e hanno la capacità di raccogliere una enorme quantità di dati provenienti da logs, telemetrie, eventi esterni, [...], ma per funzionare vanno correttamente configurati e gestiti nel tempo. Non mi dilungo perché ne ho parlato veramente tanto e ovunque.

Soprattutto a seguito di diversi miei post su LinkedIn mi è stato chiesto più volte un aiuto a comprendere il grado di maturazione dei più disparati EDR e anti-malware presenti sul mercato. Non sono attrezzato per rispondere a questa domanda in modo completo, ho quindi sempre proposto un minimo di test per comprendere che tipo di telemetria fisse in grado di raccogliere lo strumento e, se presente, che regole di detection fossero presenti o creabili in caso di necessità.

---

Questo post è di accompagnamento al video in cui presento un lab di test per i Patreon Supporter che me lo hanno chiesto, [il video è disponibile sulla mia pagina](https://www.patreon.com/posts/piccolo-self-per-109336393). I post su questo blog sono di pubblico accesso. Se vuoi sostenere la mia ricerca e la mia attività di divulgazione puoi farlo tramite [Patreon](https://www.patreon.com/roccosicilia/membership), per restare aggiornato sui sulle mia attività di ricerca inscriviti al blog:

---

## Un piccolo caso d'uso

Come dicevo non sono attrezzato per eseguire tutti i test possibili ed immaginabili su un EDR, quello che posso fare è definire dei casi specifici (ad esempio alcune delle tecniche che ho usato in passato) ed eseguire un semplice test da cui trarre delle conclusioni parziali e che ci possano aiutare a valutare ulteriori approfondimenti.

Parto da ciò che mi mette in difficoltà quando agisco su un endpoint: visto che tendenzialmente cerco di sfruttare *powershell* sulla macchina attaccata per eseguire diverse attività, ho pensato di **prendere una delle azioni più rumorose ed eseguirla in presenza di diversi EDR**. L'azione, nello specifico, è l'avvio di una sessione TCP verso un mio sistema C2 tramite Villain: la classica reverse shell. L'idea è di eseguire l'azione in due diverse modalità e vedere come si comporta l'EDR attivo sul sistema, in base agli esiti ognuno di noi deve fare delle valutazioni di merito sulla propria soluzione.

Nel video spiego il dettaglio dell'attività. Non voglio fare l'ennesimo tutoria su Villain (cosa che tra l'altro [avevo in parte fatto qui](https://www.patreon.com/posts/villain-c2-e-dei-99670954)), mi limito a darvi gli elementi per eseguire in autonomia il test.

Dotatevi di una macchina da usare come C2 su cui installare ed avviare Villain. Per rendere il tutto più interessante e realistico suggerisco una istanza pubblica in modo da avviare la sessione verso il C2 tramite internet, possibilmente attraverso il vostro firewall di perimetro (su questo tema ci torniamo con il secondo lab).

Il primo test è semplicissimo: generate il payload di vostro gradimento (io ho usato powershell_iex che fa esplicito uso di Invoke-Expression) ed utilizzatelo sulla macchina in cui avete predisposto il vostro EDR. Osservate cosa succede.

Qualche nota:

- praticamente tutti i payload di Villain, se usati in versione *vanilla*, sono intercettati anche dal "solo" Microsoft Defender, in particolare dalla funzione real-time protection
- da un test eseguito recentemente Microsoft Defender interviene all'avvio della reverse shell, in caso di bypass della funzione la reverse shell si avvia ed a runtime non vengono eseguite mitigation

Se il vostro EDR non blocca l'azione, prima di strapparvi le vesti accertiamoci di vedere la telemetria raccolta. Ci sono due possibili scenari: la telemetria c'è ma non ci sono regole per la detection di questo tipo di eventi, oppure non c'è telemetria sull'evento.

Nel primo caso potremmo dire "bene ma non benissimo": possiamo creare nelle regole di detection sulla base della telemetria osservata ed intercettare questo tipo di eventi... e questo è bane. Dobbiamo considerare che ci sono diversi scenari e tecniche di attacco per le quali dovremmo creare delle regole se il nostro strumento non ne ha di attive "built-in"... e questo non è benissimo, nel senso che bisogna lavorarci, a volte anche molto. Se siamo nel secondo caso - no allarmi, no telemetria - abbiamo un problema. L'utilizzo dei software presenti a bordo macchina per eseguire comandi e fileless malware è una tecnica ampiamente utilizzata dai threat actor, non avere telemetria su questi eventi ci rende ciechi. In questo caso lo strumento che stiamo usando non ci aiuta e dobbiamo seriamente valutare **alternative o aggiunte**.

Va considerato il fatto che non stiamo facendo nulla per "nascondere" la nostra azione offensiva, a differenza dei threat actor che lavorerebbero in modo meno rumoroso. E' vero che questo tipo di azione richiede un accesso al sistema e quindi l'attacker deve aver guadagnato già una posizione, ma come ho raccontato più volte dobbiamo considerare la possibilità di accedere ai locali del target (ogni tanto racconto qualche aneddoto proveniente dal mondo del red teaming) e tutti i possibili effetti collaterali dell'avere reti popolate da sistemi che entrano ed escono dall'azienda: in cima alla lista ci sono i laptop dei collaboratori che possono essere "compromessi" in diverse circostanze. Questo è un altro capitolo del mondo offensive, ci tornerò.

## Un pelo più stealth

Lo stesso payload utilizzato nel primo test possiamo renderlo meno identificabile applicando un po' di offuscamento nel nostro *comandone powershell*. Ci sono diversi strumenti e tecniche che potete provare, a titolo di esempio suggerisco [Invoke-Stealth](https://github.com/JoelGMSec/Invoke-Stealth): un tool in powershell che consente di offuscare con diverse tecniche un powershell script. Nella sua essenzialità consente comunque di generare un buon livello di confusione in grado di ingannare anche EDR di fascia alta (non tutti). Suggerisco anche di valutare [Chameleon](https://github.com/klezVirus/chameleon), da cui deriva uno dei template di Invoke-Stealth.

Quando passate in input ad Invoke-Stealth il vostro payload dovere fare un po' di attenzione alla sintassi dello script, potrebbe richiedere qualche ritocco per ottenere il risultato sperato, ne ho un po' parlato nelle passate live. Una volta ottenuto il set di comandi offuscati l'ultimo step è, ancora una volta, eseguirli sulla macchina di test.

Per questo secondo test ha senso per gli EDR che hanno intercettato il primo payload e ci è utile a verificare sia il comportamento in real team che le eventuali "deduzioni" che potremmo osservare in console. Ad oggi (10 agosto 2024), in considerazione di diverse valutazioni su campo oltre che in lavoratorio, posso dichiarare che non tutti gli EDR di fascia alta sono in grado di intercettare questa tipologia di payload, ma in quasi tutti i casi viene generato un allarme in console dopo pochi minuti dall'apertura della sessione TCP: chi dispone di una buona visibilità a livello endpoint può facilmente "unire i puntini" e riconoscere il comportamento non dall'analisi del payload ma dagli eventi che lo caratterizzano. Solitamente viene osservato un comando powershell che apre una sessione TCP verso un host esterno alla rete, questo comportamento è effettivamente classificabile come sospetto e riconducibile al classico scenario in cui l'attacker sta aprendo una connessione verso il C2.

Potremmo quindi avere degli EDR che **non riconoscono il codice malevolo ma riconoscono il comportamento generato dello script** e di conseguenza segnalano l'evento come malevolo o sospetto. In questo caso possiamo comunque creare una risposta adeguata, ad esempio fermando il processo powershell da cui ha avuto origine la sessione TCP.

Inevitabilmente si genera una finestra di tempo in cui l'endpoint sarà connesso al C2, cosa che potrebbe mettere l'attacker nelle condizioni di eseguire operazioni sul sistema, sarà quindi onere del Blue Team prendere in carico la segnalazione ed indagare sulle causa dell'anomalia segnalata. Questa fase dell'analisi è di fondamentale importanza (vado un attimo OT) in quanto se ci limitiamo a liquidare la segnalazione come mitigata, grazie al fatto che l'EDR ha agito sul processo una volta che ha individuato il comportamento malevolo, rischiamo di non accorgerci di potenziali compromissioni. Nel pochi secondi/minuti di sessione con il C2 il Threat Actor potrebbe aver estratto configurazioni, file, modificato parametri del sistema, [...], non lo sapremo mai se non indaghiamo.

Se l'EDR non si accorge di nulla in fase di esecuzione del codice e non genera telemetrie utili al riconoscimento dell'evento come sospetto o malevolo, abbiamo un problema. Significa che è bastato rendere un po' più torbide le acque per non consentire al sistema di identificare correttamente l'evento e in assenza di telemetria utile diventa molto complesso, se non impossibile, istruire la soluzione che abbiamo adottato in modo da rilevare questa tipologia di minaccia.

## Note conclusive

Le valutazioni su cui mi sono basato si riferiscono a test su campo nel periodo 2023/2024. All'interno dello stesso periodo ho potuto apprezzare comportamenti diversi anche sulle stesse piattaforme: ad esempio il payload offuscato, fino a qualche mese fa, risultava invisibile in fase di detonazione a moltissimi EDR, solo negli ultimi mesi (primavera-estate 2024) ho riscontrato le prime detections già all'esecuzione del codice. Mi aspetto quindi un ulteriore miglioramento nel prossimo futuro per quanto riguarda la detection dei fileless malware.

Resta in fatto che moltissime soluzioni sembrano poco efficaci nell'individuazione di questa tecnica che, lo ribadiamo, non è tra le più sofisticate ed è ampiamente utilizzata vista anche la relativa semplicità con cui può essere eseguita. Scopo di questo post e della piccola demo discussa con i Patreon Supporter è quello di invitare gli addetti ai lavori ad eseguire dei test facilmente riproducibili per farsi un'idea sull'efficacia della soluzione EDR in uso.

[<img src="{{ '/assets/images-posts/image-1.png' | relative_url }}" alt="image 1" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />](https://www.patreon.com/posts/piccolo-self-per-109336393)

Qui il video DEMO

Come ho avuto modo di dice un un recente VLOG: dobbiamo partire dall'assunto che questi strumenti, per quanto potenti, non sono infallibili e la continua ricerca di falle logiche o vulnerabilità è parte integrante del processo mi miglioramento. Se ci intestardiamo e cominciamo a porre dei dogmi facciamo poca strada.
