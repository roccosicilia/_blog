---
layout:     post
title:      "IT awareness: analisi della superficie di attacco"
date:       2024-01-26 18:00:00 +0100
categories: [cyber-security, ita, vlog-podcast]
image:
---
Con "superficie di attacco" (che io spesso vario in "superficie attaccabile") ci si riferisce solitamente a tutti quegli elementi dell'azienda che sono esposti pubblicamente: informazioni, dati, asset, servizi, ...

https://youtu.be/FcG1mrgmR-U

VLOG dedicato al tema

Non e' la prima volta che tratto questo tema: in passati blog-post e in diversi video (su [Patreon](https://patreon.com/roccosicilia) e [YouTube](https://youtube.com/@roccosicilia)) ne abbiamo parlato, ma in questa occasione vorrei cambiare approccio. Mi e' stato esplicitamente chiesto di descrivere un workflow operativo che potrebbe essere seguito per condurre un'analisi della superficie attaccabile ed approfitto della richiesta per dare un suggerimento metodologico che viene dalla mia personale esperienza. Non voglio metterla in termini di giusto o sbagliato, e' semplicemente uno dei tanti modelli che si possono prendere in considerazione.

## Qualche cenno storico

Come dicevo vorrei scrivere della mia esperienza sul tema, quindi parto dal periodo in cui ho iniziato a strutturare la fase di "ricognizione" (vedi [video di approfondimento](https://www.patreon.com/posts/concetti-di-per-95721880)) nelle mie attivita' di security test. Tra il 2016 ed i 2018 ho iniziato a (ri)discutere con IT Manager/CIO/CISO il modello con cui eseguivano i security test, in particolare i vuln. assessment ed i penetration test. Non vi sto a raccontare le sterminate paludi di inconsapevolezza che ho incontrato, ad ogni modo in quel periodo ho iniziato ad introdurre delle variazioni di scope: mi va benissimo che l'assessment sia mirato, ma era evidente che ragionare di range di IP non aveva piu' senso, come se lo spazio "digitale" occupato dall'organizzazione fosse rappresentabile con una manciata di IP. Non e' piu' cosi' da anni.

Il grande tema che sarebbe diventato poi di moda era OSInt e il modello ho iniziato ad utilizzare prevedeva un importante utilizzo delle tecniche di ricerca utilizzante anche in OSInt assieme alle piu' classiche attivita' di scansione passiva. Nel mondo della formazione il tema era gia' presente ma decisamente poco applicato, almeno in Italia (all'epoca non avevo visibilita' verso l'estero).

## Il flusso di lavoro

Lavorando sul campo mi sono reso conto che esistono dati che, una volta elaborati, consentono di sviluppare diversi approfondimenti sul target. Ho quindi strutturato quello che di fatto e' un workflow che segue il flusso delle informazioni, da quelle piu' evidenti e direttamente individuabili a quelle ricostruibili o deducibili, ma la dura realta' e' che questa fase e' difficilmente definibile con uno step-by-step predefinito in quanto i dati che possono emergere sono estremamente eterogenei e apro a diverse speculazioni. Qualsiasi flusso di lavoro va quindi preso con le pinze e riadattato alle specifiche esigenze. Una sintesi abbastanza rappresentativa di come opero la riporto in questa immagine:

<img src="{{ '/assets/images-posts/image-4.png' | relative_url }}" alt="image 4" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

sintesi del workflow di base

In verde ho evidenziato gli elementi che solitamente vengono raccolti durante l'analisi OSInt mentre in arancione gli elementi che per essere analizzati prevedono un minimo di contatto con la superficie attaccabile, anche solo a livello di banali richiesta client/server.

Durante la raccolta delle informazioni non e' raro tornare a precedenti fasi di analisi in quanto tutte le informazioni che verranno raccolte potrebbe richiedere ulteriori analisi. Es: una meta-informazione derivante da un file potrebbe mettere far emergere un nuovo asset o un nuovo contatto su avviare un approfondimento. Non c'e' un flusso di lavoro lineare quindi e molto sta anche all'esperienza dell'analista e ad una buona dose di intuito che puo' guidare la ricerca.

## Documentazione

Anche questo tema lo abbiamo trattato in diverse occasioni e su questo fronte vedo poche alternative: serve qualcosa che vi aiuti a catalogare e mettere in relazione i dati tra loro. Da qualche tempo uso essenzialmente due tools: **Notion** e **Maltego**. Il primo per gli appunti puri, il secondo per i grafi.

Tutto cio' che emerge dalle ricerche deve poi essere analizzato ed approfondito e la quantita' di dati solitamente e' piuttosto alta. Senza uno strumento che metta ordine diventa molto difficile svolgere l'analisi.

## Output

Unendo i puntini spesso si riesce a tracciare un perimetro abbastanza credibile - anche se inevitabilmente incompleto - della componente tecnologica dell'organizzazione, dei dati e dei file che ha deciso di esporre (piu' o meno consciamente) e le relative ripercussioni, delle persone che vi lavorano sia come dipendenti che come consulenti o fornitori.

L'attivita' di analisi e' puramente deduttiva e speculativa, ovvero si possono fare anche delle supposizioni sulla base di una serie di evidenze. Faccio un esempio: se dalle ricerche tramite Google Dorks emerge la presenza di un file in formato PDF che nei suoi meta dati riporta come software di creazione una versione di MS Word, possiamo ipotizzare che all'interno della struttura target sia presente tale software e quindi annotarlo tra le tecnologie in dotazione. Questo semplice ragionamento e' applicabile a moltissimi elementi che emergono dalle ricerche sul target.

## Considerazioni sulle fonti CLOSInt e zone grigie

Nel mio flusso non compare nulla in relazione a dati provenienti da fonti non pubbliche o da data breach anche se, a mio parere, anche questi dati sono da prendere in considerazione o quanto meno la presenza accertata in un precedente breach di informazioni sul target e' un elemento da tenere in considerazione anche se non si hanno i dati precisi.

La ritengo un'attivita' da valutare in relazione al contesto e che non e' necessariamente da legare al tema dell'analisi della superficie attaccabile. Questo argomento sarebbe piu' affine al contesto della Threat Intelligence in quanto la presenza di dati dell'organizzazione in eventuali data breach e' qualcosa da controllare costantemente, non solo il fase di security test, ma su questo tema ci torno un'altra volta.
