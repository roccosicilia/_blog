---
layout:     post
title:      "Gestione degli IoC #1"
date:       2024-07-23 10:00:00 +0200
categories: [cyber-security, ita, update]
image:
---
Potrebbe essere una serie di post per un motivo tecnico-operativo: qualche giorno fa ho introdotto il tema della gestione degli IoC in un [post su LinkedIn](https://www.linkedin.com/posts/roccosicilia_ybersecurity-ioc-activity-7217450035943227394-X_E5?utm_source=share&utm_medium=member_desktop) ed in una [live](https://twitch.tv/roccosicilia) in cui abbiamo discusso con i presenti in relazione alla difficoltà di molte realtà nel definire un modello di gestione e portarlo avanti. Il problema è molto semplice da comprende ma, a quanto pare, difficile da realizzare per le realtà del mondo enterprise e, in qualche caso, anche dagli addetti ai lavori. Ho personalmente discusso con strutture che erogano servizi di detection and response che hanno manifestato qualche difficoltà.

Per varie ragioni chi lavora in ambito info. sec. si trova a collezionare diverse tipologie di IoC. Nel mio caso, considerando solo l'ambito in cui opero direttamente, ho accumulato molti dati provenienti da ricerche OSInt, vulnerabilità analizzare, artefatti, exploit, p-o-c, ecc. Ho sempre cercato di tenere organizzato questo archivio che è sempre stato ad uso personale, recentemente ho avuto modo di lavorare in contesti dove la condivisione degli IoC è stata un valore aggiunto ma ho notato che la mancanza di regole per la gestione ha generato qualche difficoltà.

Ne viene fuori un piccolo progetto personale che mi piacerebbe condividere: una repo pubblica di IoC a cui aggiungere un modello di gestione e degli strumenti per agevolare le Operations. Per l'occasione condivideremo questa repo: <https://github.com/b1th0rn/BitIoC>.

---

Se vuoi supportare i progetti di divulgazione che porto avanti ho messo a disposizione un [programma su Patreon](https://www.patreon.com/roccosicilia) dove archivio tutte le live assieme a contenuti dedicati ai supporter. Per restare sempre aggiornat* iscriviti al blog:

---

Durante la live, che ho già archiviato su Patreon e [la trovate qui](https://www.patreon.com/posts/study-session-12-108112540), abbiamo discusso qualche punto fisso:

- per praticità la struttura la manterremo su github in modo da dare a chiunque la possibilità di accedere a contribuire
- come formato utilizzeremo STIX v2, largamente adottato dagli strumenti di cyber security
- la repo degli IoC è solo il risultato di un processo di validazione, l'obiettivo a livello community è quello di definire un modello di gestione ed organizzare gli IoC di conseguenza

E' un progetto contributivo quindi quello che qui vado a definire potrebbe essere ridiscusso domani, anzi lo spero.

## Organizzazione di base

Al momento la repo è organizzata con tre contenitori:

- data: conterrà gli IoC in formato STIX già sottoposti a processo di validazione
- pending_data_validation: conterrà gli IoC in formato STIX candidati dalla community
- utility: script per la creazione degli IoC e la loro gestione

L'idea di base è questa:

- Chi vuole collaborare [deve farsi vivo su Discord](https://discord.gg/Ys5AAbsyyH) per avere accesso attivo alla repo
- Una volta avuto accesso nella repo troverà gli script per generare gli IoC (quando ci saranno ovviamente) nel formato definito
- A livello organizzativo ho pianificato una sessione di discussione bisettimanale su Discord, il venerdì mattina salvo imprevisti

Al momento la sessione di discussione la tengo aperta ma per ovvie ragioni è probabile che nel tempo venga limitata ai partecipanti attivi del progetto.

Seguiranno aggiornamenti.
