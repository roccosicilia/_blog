---
layout:     post
title:      "Capacità di reagire: modi e tempi."
date:       2021-04-16 09:00:00 +0200
categories: [cyber-security]
image:
---
Nelle ultime settimane ho avuto modo di osservare e riflettere sulla capacità, di organizzazioni ed aziende, di reagire a specifici eventi legati alla sicurezza informatica. In particolare ho preso in esame la reattività ad eventi di segnalazione di una minaccia e la reattività ad eventi di rilevamento di un incident.

i tratta di due casistiche molto diverse tra loro in quanto la prima genera (o dovrebbe generare) valutazioni di rischio ed eventuali azioni di prevenzione mentre la seconda innesca (o dovrebbe innescare) azioni di gestione dell’incident.

## La percezione del rischio

Ciò che è chiaro è che non tutti percepiscono il rischio allo stesso modo: la segnalazione di una minaccia, per quanto contestualizzata, viene spesso qualificata secondo la propria percezione personale e soggettiva di quanto il rischio sia elevato. Non sempre viene eseguita una valutazione di merito sui dati a disposizione secondo criteri oggettivi.

<img src="{{ '/assets/images-posts/cve-2021-26855.webp' | relative_url }}" alt="e6e16 1mmjupvcufbka3dazqv9uxw" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Ve la ricordate questa, vero?

Un buon metodo, secondo la mia esperienza ovviamente, è quello di mettere a fattor comune dati oggettivi come lo score della minaccia / vulnerabilità (dato che è facilmente reperibile dai security bulletins che voi tutti controllate) con il coefficiente di impatto che l’asset ha nella vostra infrastruttura. Questo secondo dato, che effettivamente non tutti gestiscono, deriva da una valutazione che le organizzazioni devono fare per comprendere quanto un asset ha impatto sul proprio business (si, è la Business Impact Analysis). Per semplificare il dato che serve avere è un coefficiente che vi aiuti a comprendere quanto un certo asset (o gruppo di asset) è critico per il funzionamento della vostra organizzazione o di uno specifico servizio. Facciamo un esempio facile facile: quanto è critica la posta elettronica per la vostra azienda? O meglio: quanto del vostro business viene impattato da un fermo dei servizi di posta o da un data breach che impatta i servizi di posta? Sulla base di questa informazione oggettiva che l’IT assieme al Management deve definire sarà possibile dedurre l’impatto del servizio in oggetto.

Ora è più facile: se mi viene notificata una minaccia con score elevato (9/10 è elevato nel caso ci siano dubbi) che coinvolge un asset che è stato classificato di elevato impatto (secondo la scala che avete deciso di applicare)… bhe, c’è poco da dire, siete di fronte ad un rischio elevato e dovere intervenire a prescindere dalle vostre opinioni soggettive.

> Nota: l’ho molto semplificata, l’obiettivo in questa sede è trasferire il concetto di obiettività della valutazione.

## La qualifica dell’impatto

In un contesto di security incident ovviamente la faccenda è un po’ diversa: non si parla più di minaccia e rischio ma di impatti e conseguenze e ancora una volta torna utile avere una mappa di impatto per comprendere dove mettere le mani e che azioni intraprendere.

Non serve aver gestito security incident (tema su cui ho un po’ di esperienza) o averne subiti (tema su cui chi vuole può contribuire in forma anonima per condividere la propria esperienza) per comprendere come sia complesso prendere decisioni razionali durante un evento di questo tipo. Mettersi a qualificare l’impatto sulla base della propria comprensione dell’aziende e dell’infrastruttura ad incident in corso è qualcosa di poco proponibile. La qualifica dell’impatto deve essere snella e definibile su dati oggettivi come la valutazione di impatto dei sistemi coinvolti (che dovrebbe già esistere), la classificazione dei dati presente sui sistemi coinvolti (che dovrebbe già esistere), l’elenco delle risorse da coinvolgere in relazione ai sistemi/servizi impattati. Vietato improvvisare… o meglio, chi non ha dati oggettivi e si trova a dover improvvisare si espone a rischi elevatissimi.

## Reazione

Arrivo al vero tema del post… la reazione in termini di tempi e modi. E’ ovvio che se non c’è una procedura per gestire un evento come un incident o una notifica di potenziale vulnerabilità dei sistemi i team interessati agiranno a propria discrezione: chi subito, chi quando ha tempo, chi mai. E’ inoltre ovvio che, anche nel caso di una reazione immediata, l’assenza di una procedura porta ad azioni a discrezione della singola persona la cui efficacia dipenderà dal grado di competenza e conoscenza del sistema e del contesto. Quindi si ottengono risultati apprezzabili o meno a seconda di chi opera. Non lo trovo uno scenario accettabile per un’organizzazione il cui business potrebbe essere pesantemente impattato da un security incident.

L’assenza di procedure a supporto di una reazione commisurata all’evento spesso porta con se l’assenza di una metodologia per la gestione di un evento di incident e, per ovvia ragioni, l’assenza di strumenti adeguati sia a livello di tools che a livello di skills specifiche.

Come sempre faccio degli esempi idioti ma molto reali: nel corso di azioni di mitigation può capitare di dover eseguire azioni con impatti su grandi quantità di sistemi come il cambio di una policy o un banale reset password di decine di server e apparati. Eseguire queste operazioni in 25 secondi grazie a procedure e strumenti già definiti o eseguirle in 4 ore a mano (con relative implicazioni legate al fattore umano) è ciò che può cambiare gli esiti e gli impatti dell’incident sul business. **In alcuni casi basterebbero poche procedure ben strutturate e qualche script in python per ribaltare la situazione (voglio essere provocatorio ma non è un’affermazione così lontana dalla realtà)**.

Ciò che trovo paradossale è il fatto che in molte aziende trovo le tecnologie abilitanti ad una gestione virtuosa della sicurezza informatica ma spesso mancano i processi per una efficiente ed efficacie gestione del proprio patrimonio digitale. La domanda su cui riflettere che vi lascio per il week-end è: quanta tecnologia avete adottato senza una strategia di gestione e delle procedure dedicate?