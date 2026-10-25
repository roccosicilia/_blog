---
layout:     post
title:      "rootstash"
date:       2025-07-12 09:00:00 +0200
categories: [hacking, ita]
image:      /assets/images-posts/coding.png
---
Riprendo un mio vecchio progetto, vediamo se riesco a tenere il ritmo. Tempo fa avevo iniziato a strutturate scripts, utility e note tecniche in relazione alle mie attività di pentesting e red teaming. Tra i miei appunti c'è una montagna di info destrutturate, utili sono a me in quanto so cosa cercare e dove cercare: se incontro una certa vuln. in un certo contesto mi basta scartabellare un attimo tra le mie note per vedere come avevo già deciso di affrontare il tema e se scopro qualcosa di nuovo lo aggiorno.

Per ovvie ragioni non possono pubblicare in blocco i miei appunti, sono un vero guazzabuglio in cui solo io saprei orientarmi. Sono certo che molti hanno questo "pregio". Il progetto [rootstash](https://github.com/roccosicilia/rootstash), una repo pubblica che ho recentemente creato, ha come obiettivo quello di raccogliere, in modo strutturato, questi appunti.

Se aspetto di trovare il tempo di fare una review di tutto il destino di questa idea è già segnato... non lo farò mai. Cambio approccio: man mano che rimetto mano ad una sezione dei miei appunti ne faccio la review e li porto nella repo, una "case study" alla volta.  
  
Esempio. Oggi avevo l'esigenza di spippolare con l'output di ShapHound, un bel set di JSON file. Avevo già abbozzato qualcosa per leggere i dati ed eseguire operazioni di discovery in rete con le info prelevare da Active Directory, l'occasione è stata utile per rivedere un po' quel semplice python script e pubblicarlo:

[<img src="{{ '/assets/images-posts/image-1.png' | relative_url }}" alt="image 1" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />](https://github.com/roccosicilia/rootstash/blob/main/scripts/export_bloodhound_info.py)

...

Anche se non ancora completo con tutte le funzioni che vorrei implementare la versione online è già funzionante ed utilizzabile.
