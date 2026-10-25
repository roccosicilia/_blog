---
layout:     post
title:      "L’illusione del controllo e la ricerca del punto debole."
date:       2020-09-22 09:00:00 +0200
categories: [cyber-security]
image:
---

Vi confido un *segreto*: nella progettazione e realizzazione di un attacco informatico è fondamentale individuare il “punto debole” perché è da lì che si guadagnerà un accesso a sistemi e informazioni.

Banale? Sì, ma a quanto pare poco chiaro. Sin dai primi confronti sul percorso di analisi della sicurezza di una struttura percepisco chiaramente nei miei interlocutori la certezza del controllo, talvolta con frasi un po’ sconcertanti tipo:

> *“La password di quel sistema la conosco solo io.”  
> “Abbiamo il miglior Firewall sul mercato.”  
> “Le porte USB delle workstation non consentono l’utilizzo di pen-drive.”*

Tutte cose sagge e sicuramente vere, ma **non si considera che dal punto di vista dell’attacker** le password talvolta non servono, i firewall si eludono (o addirittura si *by-passano*) e non ho ancora visto un sistema bloccare una *usb-rubber-ducky* (e spesso quando ne parlo l’interlocutore non sa cosa sia).

Comprensibilmente, se abbiamo lavorato bene, riteniamo di aver pensato a tutto o quasi. Diamo per scontato che tutte le porte siano state ben chiuse e di essere ben consapevoli di quali siano i punti deboli della nostra struttura.

Questa è una tipica **posizione pericolosa** che rischia di mettere seriamente a rischio la vostra infrastruttura. Un attacker ben motivato non si fermerà al *deny* del firewall ma semplicemente cercherà altre vie. Nella progettazione di un attacco è fondamentale il rapporto costo/beneficio: l’attacker è consapevole che non ha senso accanirsi contro un punto del perimetro ben presidiato e prenderà in considerazione altri punti potenzialmente vulnerabili che non necessariamente saranno dei sistemi informatici.

E’ una consuetudine utilizzare il mezzo informatico per ingannare la vittima al fine di estorcere le informazioni utili, uno dei primi bersagli è infatti l’utente inesperto da utilizzare come “ariete”. E sono sempre gli utenti che portano in rete device di ogni tipo spesso non controllabili dall’amministratore di rete. Per farla breve: **il controllo è pura illusione**, si può controllare molto ma non tutto.

<img src="{{ '/assets/images-posts/black-hat-def.png' | relative_url }}" alt="Black Hat" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Per l’attacker questo è un dato di fatto, è l’assunto su cui si costruisce l’attacco, il motivo per il quale **il successo di un’intrusione è, sempre più spesso, una questione di tempo**. Quindi, visto che la motivazione degli attacker è, stando alle statistiche, per lo più economica (parlerò più avanti del tema di Business che si è sviluppato) diventa importantissimo rendere questo processo efficiente investendo risorse nella ricerca del punto debole (e che ci crediate o meno, c’è sempre) per poi sferrare un attacco specifico e mirato.

Personalmente ho incontrato molte realtà ben strutturate con eccellenti professionisti in campo IT e Security, **ma non ho trovato nessuno di invulnerabile**.
