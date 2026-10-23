---
layout: post
title:  "Se il target sono i Sistemi Industriali e le Infrastrutture Critiche."
date:   2019-02-25 09:00:00 +0200
categories: [cyber-security]
image:  "/assets/images-posts/ot-sec-generic.jpeg"
---
Con Operation Technology (OT) ci riferiamo alle infrastrutture tecnologiche (hardwaere e software) che consentono il funzionamento di un sistema “fisico”, tipicamente in ambito industriale o di automazione e gestione di sistemi elettro-attuali. Il tema spazia dal sistema di controllo e gestione delle pompe di un acquedotto alla linea di produzione industriale completamente robotizzata. I sistemi coinvolti oggi dialogano con protocolli molto specifici (es: SCADA) e di fatto sono costituiti da Endpoint di una rete TCP/IP, tipicamente dei computer in diverse forme su cui vengono installate le componenti client dei software, da dei sistemi server e da una rete di sensori/rivelatori/attuatori/*ori utilizzata dai sistemi di controllo per leggere dati (telemetrie, rilevazioni, immagini, ecc.) ed eseguire azioni nel mondo fisico. Oggi le reti OT dialogano con le reti IT e spesso il confine tra questi due mondi non è ben definito in quanto l’evoluzione tecnologica li ha portati a condividere tecnologie e risorse a vari livelli.

Non è quindi una sorpresa che gli attacker prendano di mira i sistemi OT tanto quanto i sistemi IT, anzi, di fatto non vi è discriminante per attaccare l’uno o l’altro in quanto vi sono eguali opportunità di mettere in scacco una realtà produttiva (nel caso migliore) o un’infrastruttura critica (nel caso peggiore). Gli impatti sono evidenti: nel caso della realtà produttiva un fermo della produzione ha un impatto diretto sul ciclo di Business (si perdono soldi), nel caso di un’infrastruttura critica (trasporti, sistemi logistici, sistemi di comunicazione, distrubizione elettrica, ecc) vi è un impatto diretto sulla vita dei cittadini, sulle persone (in alcuni contesti si rischia di perdere vite).

Ovviamente queste evidenze massimizzano il modello di Business del criminale informatico. Quanto è disposta a pagare un’azienda per vedere sbloccati i sistemi di produzione messi fuori uso da un attacco informatico? Quanto è disposto a pagare un Ente/Governo per vedere ripristinato il traffico ferroviario nazionale manomesso da un attacker? Purtroppo il problema è reale. Purtroppo è ancora preso troppo alla leggera e l’epilogo tocca leggerlo sulle prime pagine dei giornali quando qualcosa — che si poteva evitare — va storto.

## Mettiamoci il cappello bianco

La nota positiva, parlando con aziende strutturate del panorama industriale italiano, è che gli addetti ai lavori se ne sono resi conto e non da poco. La nota negativa è che il management fa ancora fatica a mettere a fuoco il tema. In questa differenza di vedute i criminali informatici prosperano.

Qualificare un’azienda come potenziale target è relativamente semplice, basta fare delle verifiche sul fatturato negli ultimi anni ed analizzare qualche dato sulla reputazione del brand per farsi un’idea. Se l’azienda piace e sta bene economicamente probabilmente ha tanto da perdere e quindi l’attacker ha tanto da guadagnare. Ragionamenti tanto banali quanto reali che si mescolano ad un tema che avevo trattato in passato legato alla “reputazione”.

Che la produzione non si debba fermare non è un’ipotesi, è una certezza. Ci sono aziende che basano il proprio modello di Business proprio sulla velocità della produzione, ovvero competono sul tempo che impiegano a trasformare l’ordine, che spesso arriva dall’e-commerce, in prodotto da consegnare. Perdere un ordine significa perdere soldi se non addirittura il cliente.

Questi sono esempi di modelli di Business che reppresentano reali opportunità per il cyber-crime, sono modelli che richiedono spesso una forte esposizione per funzionare e dove l’automazione del processo produttivo è moltissima e trasversale.

La progettazione di un attacco, in questi contesti, non è molto differente dal puro contesto IT ma lo scenario propone delle differenze: abbiamo a che fare con una rete non sempre segmentata, che interconnette sistemi spesso non aggiornabili (ambienti legacy) dove non è consentito l’utilizzo di appositi strumenti di protezione, il tutto interconnesso in qualche modo a parte dei sistemi IT e dove l’utilizzatore potrebbe non sapere nulla di informatica.

La superficie aggredibile è vastissima, ma è opinione — errata — comune che non vi siano particolari strumenti attaccabili in un rete OT. La realtà è che ogni sistema automatizzato funziona grazie ad un computer (di varie tipologie) con a bordo un sistema operativo e applicazioni anche molto datate, perfettamente funzionanti ma spesso molto vulnerabili. Esistono tecniche e vottori d’attacco studiati appositamente per il mondo OT: con il Red Team di VERSIVO abbiamo avuto modo di sperimentare alcuni vettori d’attacco specifici che mescolano tecniche di code injection e DNS tunneling, tecniche relativamente semplici da intercettare e bloccare ma che in un contesto di automazione industriale rischiano di attecchire con estrema facilità.

Piccola parentesi tecnica. Un attacco particolarmente interessante prevede la manomissione dei file di progetto dei sistemi industriali, formati proprietari che contengono le informazioni su come la macchina dovrà comportarsi per la lavorazione di un “pezzo” o di un “prodotto”. Questi file di base contengono istruzioni e alcuni formati consentono l’injection di codice arbitrario (es: javascript) o a livello scripting interpretabile poi dal software che utilizza il file in oggetto.

La tecnica è molto simile a quella utilizzata con file PDF (JS Injection) o sui file del pacchetto Office (Macro Injection) ma riportata in un contesto dove non si utilizzano né PDF né file di Word. Inoltre i formati utilizzati nel mondo OT raramente sono “compresi” dai sistemi di sendboxing, risulta quindi molto difficile verificare la presenza di codice malevolo.

## Rischio elevato / Impatto elevato

Su questo fronte non possiamo non considerare l’impatto che avrebbe un Security Incident: perdere un dato è un conto, perdere il controllo di un sistema industriale o di un’infrastruttura critica è un altro paio di maniche. Non voglio fare paragoni sull’importanza a livello Business, mi riferisco all’impatto diretto e potenzialmente devastante che potrebbe avere un attacco sferrato contro un target critico. Penso il tema sia meritevo di considerazione a tutti i livelli.