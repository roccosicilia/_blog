---
layout:     post
title:      "Cyber Security mindset."
date:       2020-11-12 09:00:00 +0100
categories: [cyber-security]
image:
---

C’è una tesi di base che dovrebbe diventare il nostro modus operandi generale nella gestione dei problemi, qualunque problema, a prescindere dalla natura o dal contesto.

La prima cosa che dobbiamo imparare è riconoscere il problema. È banale: se un fatto o una evidenza non viene riconosciuta come un potenziale problema è ovvio che nessuno valuterà delle azioni atte alla sua gestione e risoluzione. L’impatto dell’incapacità di gestire un problema è doverne poi gestire gli effetti, ovvero gli “incident” ad esso correlati; si rischia così di entrate in un loop estremamente inefficiente di break/fix che non aiuterà l’organizzazione, anzi, la ostacolerà.

L’inefficienza è un costo che grava sulle nostre organizzazioni e, in un contesto di cyber (in)security, è anche un rischio in quanto l’impatto di un security incident è potenzialmente disastroso. Se applichiamo la logica break/fix — aggiusto quando si rompe — facciamo poca strada in quanto la gestione di eventi come un data breach o un attacco ransomware ha risvolti assolutamente imprevedibili… e anche diventassimo bravissimi a prevedere i costi di gestione di alcuni specifici attacchi (tutti è impensabile) quanti realisticamente potremmo gestirne? Quanti data breach siamo in grado di sostenere?

<img src="{{ '/assets/images-posts/golden-circle.webp' | relative_url }}" alt="Golden Circle" style="float: left; width: 200px; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

L’approccio al problema fa tutta la differenza, **la cyber security** non può essere approcciata in modalità break/fix ma **va gestita strategicamente per trasformare quello che apparentemente è un costo in un investimento atto ad aumentare la qualità della nostra organizzazione**, del nostro lavoro e del nostro “prodotto”.

## L’approccio

Partiamo dal prendere in considerazione l’approccio che ha il mondo del cyber crime: questo ci aiuta a mettere a fuoco il problema e ci da qualche spunto per capire come gestirlo in modo efficiente oltre che efficace.  
I criminali informatici sono molto metodici ed il modello in uso è affine a quello che utilizzeremmo noi nel progettare una nuova idea di business.

Probabilmente ragioneremmo sul mercato che ci interessa approcciare, cercheremmo di identificare il nostro prototipo di cliente/target, valuteremmo una strategia di approccio per entrare in contatto con il nostro target. Un volta stabilito l’engagement ci preoccuperemmo del metodo di lavoro e degli strumenti necessari.

Ripercorriamo questo modello con un esempio molto pratico e molto realistico di come un’organizzazione criminale approccerebbe un “business digitale”.

*Il mercato*  
Esistono diversi ambiti in cui il business del cyber crime può crescere. Una macro-suddivisione che spesso propongo, non completa ma molto pragmatica, è riducibile a due grandi “mercati”: le informazioni e la produzione (per lo più in ambito industriale ma vale anche per i servizi). Quindi da una parte abbiamo le aziende e gli enti che gestiscono informazioni, più o meno riservate e sempre più strategiche, dall'altra parte abbiamo le aziende che producono, che ideano, ingegnerizzano e creano qualcosa di nuovo che viene immesso sul mercato “ordinario”.

Dal punto di vista dell’attacker la valutazione del mercato è un tema che richiede ponderazione in quanto i modelli che dovrà applicare saranno estremamente vincolati alla tipologia di mercato su cui si muoverà.

*Il target*  
Definito l’ambito viene qualificato il target: aziende di produzione ve ne sono di molti tipi e di molte dimensioni e la stessa cosa si può dire delle aziende che in qualche misura gestiscono dati sensibili ed informazioni strategiche. La qualifica del target consente di ragionare sulle strategie che possono essere utilizzate per poi definire un modello che tenga conto del costo di realizzazione dell’attacco e di conseguenza della quantità di danaro che si intende incassare dall'azione criminosa.

È ovvio che il modello funziona nel momento in cui il costo sostenuto per gli attacchi sia abbondantemente coperto dalle somme di denaro che si conta di raccogliere. Questo porta l’attacker a ragionare sull'efficienza ed a ricercare modelli di attacco relativamente poco costosi rispetto all'ipotetico incasso.

La ricerca dell’efficienza ha portato allo scenario attuale in cui gli attacchi informatici sono sempre più composti da una miscela di azioni che comportano l’uso (o l’abuso per meglio dire) della tecnologia quanto l’uso dell’inganno (Social Engineering).

Possiamo speculare all'infinito su quale target sia più appetibile, è quindi saggio valutare lo storico per farci un idea e scoprire probabilmente molte conferme in relazione alle riflessioni che mi auguro questo articolo abbia scatenato.

<img src="{{ '/assets/images-posts/attack-by-sector.webp' | relative_url }}" alt="Attack" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Industria, educazione e sanità (in senso ampio) attraggono da soli poco più del 50% degli attacchi. L’orientamento degli attacchi ci da delle ottime indicazioni circa il modello che il mondo del cyber crime sta implementando e questo ci porta direttamente alla prossima considerazione.

*La strategia*Ovviamente vi sono molte strategie che si possono applicare in un contesto di attacco ma ancora una volta è sufficiente osservare i trend e, purtroppo, leggere la cronaca per giungere a delle conclusioni molto realistiche. Nel caso degli ambienti di produzione o di erogazione di un servizio talvolta anche critico la strategia è quella di generare un’interruzione del servizio. Per un’azienda di produzione può voler dire l’incapacità di mantenere attivi i propri impianti o la propria rete logistica, per il mondo ospedaliero può voler dire il caos organizzativo o, in casi estremi, il mettere a rischio vite umane. La strategia è quindi mettere alle strette la propria vittima, colpire in modo tale da non lasciare molte scelte se non quella di sottostare alle condizioni di riscatto, con degli “incentivi” in più: la minaccia di divulgare informazioni sensibili in caso di non collaborazione.

*Il metodo*Passiamo dalla strategia alla tattica, ovvero al piano d’azione che viene messo in atto al fine di mettere alle strette il proprio target. Ci sono molti modi per colpire un’azienda individuata come potenziale vittima e tipicamente, ancora una volta, la valutazione è opportunistica. È ovvio che è più efficiente colpire là dove l’impatto sarebbe più elevato e nel modo meno “faticoso” possibile, l’analisi si sposta quindi sul modello di business dell’azienda target per valutare quale azione porrebbe essere quella più impattante.

Per un’azienda che eroga servizi online potrebbe essere particolarmente critico il portale con cui gestisce le transazioni, per un’azienda di produzione è sicuramente vitale mantenere attivi gli impianti. Nella quasi totalità dei casi il funzionamento delle aziende è saldamente legato al funzionamento dei sistemi IT, non solo per ciò che riguarda il complesso tema della gestione delle informazioni e delle comunicazioni ma sempre di più anche per la gestione e l’utilizzo degli impianti di produzione.

L’automazione industriale rappresentante un evidente vantaggio competitivo: grazie alla possibilità di far dialogare il mondo OT con il mondo IT è stato possibile portare efficienza in contesti che in passato avrebbe richiesto impianti molto complessi. Il “nuovo” scenario espande enormemente la superficie attaccabile di questa tipologia di target e non passa inosservato il fatto che sistemi sviluppati in contesti assolutamente isolati si trovano oggi ad essere interconnetti ad altri sistemi e ad altre reti. La miscela è estremamente infiammabile: molte tecnologie non sono state pensate per lavorare in contesti estremamente interconnessi come quelli delle reti IT e, va da se, non sempre sono stati progettati tenendo in considerazione temi come la sicurezza informatica, semplicemente perché prima non vi era la necessità.

*Lo strumento*In gergo il “vettore” d’attacco, il mezzo ultimo attraverso il quale l’attacker colpisce in base alla tattica scelta: si può trattare di un crypto malware, di una email a fini truffaldini (scam) o dello sfruttamento di una vulnerabilità per ottenere un accesso abusivo ai sistemi della vittima. Poco importa, stiamo parlando di uno strumento al servizio di uno scopo, dell’atto ultimo di un percorso ben più lungo ed articolato.

## Un esercizio di mindset: il perché?

Il paradosso sta nel fatto che quando si parla di cyber security troppo spesso ci si riferisce agli strumenti, alla tecnologia, alle soluzioni, ovvero il tema viene ridotto ad una specifica parte di un ben più vasto argomento. Raramente si parla di metodo o di strategia, ancor meno si parla di motivazione ed approccio.

Limitando il focus sugli strumenti e sulla tecnologia ci troviamo inevitabilmente a discutere di costi: costi per sistemi di protezione, costi per adeguamenti a procedure e regolamentazioni, costi per servizi di assessment e consulenze. È ovvio che gli strumenti sono necessari ma non possono essere di per sé il fine. È altrettanto ovvio che se restiamo ad argomentare sul costo dello strumento sarà molto complesso elaborare un piano.

Questo è il salto da fare: dobbiamo fare un piano, dobbiamo capire dove e come investire risorse — economiche e cerebrali — per sviluppare un piano che ci permetta di **generare una cultura della sicurezza informatica** nella nostra organizzazione e che questa cultura diventi un percorso qualitativo che sia di impatto sul nostro modo di lavorare e quindi sul prodotto finale.

Aumentare la qualità del nostro lavoro e del nostro prodotto è ciò che ci distinguerà quando ci presenteremo sul mercato: salvo non essere monopolisti tutti dobbiamo fare i conti con la concorrenza e **in un mondo reso complesso dalle minacce informatiche essere l’organizzazione che lavora con principi di sicurezza by design è indubbiamente un bel punto a favore per distinguersi**. **Da costo per arginare situazioni spiacevoli a vantaggio competitivo**.

> Ho investito in un percorso che ha portato la mia azienda ed il mio prodotto/servizio ad essere più resiliente, se non anti fragile, alle minacce informatiche per restituire maggior valore al mio cliente.

Questa deve essere la spinta motivazionale, competere sul valore del prodotto o servizio che proponiamo su un terreno relativamente vergine. Tutto il resto, ciò che ne consegue, sono graditissimi effetti collaterali che rappresentano parte del ritorno d’investimento: riduzione del rischio cyber, affidabilità dell’infrastruttura e degli impianti, migliore posizionamento del brand, specifiche qualifiche in ambito gestione del rischio sempre più richieste dai clienti come da interlocutori come chi opera nella sfera assicurativa e finanziaria. Frutti di un processo virtuoso che, per esser tale, va intrapreso nel modo corretto e deve diventare un percorso strutturato per l’organizzazione. Per ovvie ragioni non è pensabile di operare con budget e tempo infinito, è necessario che qualcuno venga designato a valutare una strategia, a tracciare una via.

## Come lo facciamo?

Il perché vada fatto è chiaro, non è solo un tema di rischio è un tema di vantaggio competitivo. Questa è la motivazione. Un metodo per costruire questo percorso può essere quello che dobbiamo imparare per gestire in generale i problemi — non gli incident, i problemi — e come vi avranno detto in tutti i corsi di management degli ultimi 25 anni i problemi sono… lo sapete già.

<img src="{{ '/assets/images-posts/risk-sample.webp' | relative_url }}" alt="Risk" style="float: left; width: 200px; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Per prima cosa dobbiamo comprendere il problema, in questo caso la minaccia. A cosa siamo esposti esattamente? La tendenza è quella di analizzare gli strumenti: sappiamo che ci sono i ransomware e quindi cerchiamo di arginare con strumenti di protezione specifici, sappiamo che c’è il phishing e di conseguenza adottiamo strumenti anti-phishing… Strumenti, ma non strategie. Quante aziende hanno un piano di incident management in caso di attacco? Quante aziende misurano il proprio grado di resilienza a reali minacce informatiche eseguendo dei security test e degli assessment?

Comprendere la minaccia implica la conoscenza della minaccia stessa, non delle ipotetiche “barriere” che potremmo adottare. L’approccio che personalmente ho trovato efficiente è analizzare il target, l’organizzazione in questo caso, con gli occhi dell’attacker, che analizza, valuta i punti deboli tecnici ma soprattutto umani e procedurali e sulla base di questi costruisce un modello di attacco efficacie perché va a colpire la dove siamo deboli (ed è diventato il mio lavoro, il mio impegno quotidiano).

**Una buona strategia di difesa** deve tener conto dei modelli di attacco, non solo dei vettori ultimi (il ransomware) ma dei metodi di implementazione dell’attacco, in caso contrario il rischio è di essere colpiti la dove non abbiamo presidiato.

**Una eccellente strategia di difesa** tiene conto della possibilità di essere attaccati. È poco saggio, oggi, pensare di essere invulnerabili, è molto più assennato valutare situazioni critiche e costruire dei piani di contingenza. Sapere cosa fare nel momento del bisogno fa la differenza tra il ripartire in 24 ore e non ripartire. Ancora una volta la strategia di difesa non possiamo inventarcela, va definita tenendo conto delle peculiarità dell’organizzazione partendo dal modello di business e dai processi.

È evidente che si tratta di un percorso dove le economie vanno ponderate in relazione alle criticità, ed è proprio dalle criticità che si parte, ovvero da quei rischi, grandi o piccoli, che presentano anche un elevato impatto.

L’efficienza ed efficacia devono governare questo percorso, non la tecnologia. Sia ben chiaro la tecnologia resta lo strumento indispensabile ma è appunto uno strumento. Costruire una strategia di difesa dalle minacce cyber ci consentirà di selezionare e governare correttamente la meravigliosa tecnologia che il mercato ci presenta.

> **Mindset**: approcciamo il problema con la mentalità corretta.  
> **Strategia**: analizziamo la situazione di partenza e facciamo un piano di crescita.

Il bilancio non può che essere positivo in termini di qualità e presenza sul mercato.