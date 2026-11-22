---
layout:     post
title:      "Prendetevi cura della vostra zona DNS"
date:       2023-04-12 13:00:00 +0200
categories: [cyber-security, hacking, ita]
image:
---
Per vari motivi sto riprendendo in mano varie tecniche di "ricognizione" nei confronti di un potenziale target ed è sorprendente quante informazioni vengano lasciate a disposizione di chiunque per banale mancanza di manutenzione.

Oggi è stato il turno delle zone DNS, elemento interessante per un'attacker in quanto avere a disposizione un elenco di domain e subdomain rappresenta un ottimo punto di partenza per comprendere parte del perimetro del target.

Facciamo una prova? Da una kali potete utilizzare uno dei tanti tools di enumeration:

```
-- amass enum -passive -d roccosicilia.com
```

Otterrete l'elenco di ciò che è configurato a livello di zona per il dominio indicato. Il mio dominio ha ovviamente poco essendo utilizzato esclusivamente per questo blog, ma se fate la prova sul vostro dominio corporate sono abbastanza certo che il risultato sarà più interessante.

Possono sembrare informazioni assolutamente innocenti, dopo tutto questi record sono stati creati appositamente per essere utilizzabili dagli utenti che desiderano accedere ad un sistema. Il problema infatti non si riferisce a ciò che è in uso dall'organizzazione ma a **ciò che è in uso solo internamente o non più utilizzato e dimenticato**.

Non è raro trovare subdomain che si riferiscono a sistemi di test - spesso dimenticati - o a sistemi in una fase di staging che espongono elementi di debugging dell'applicazione (trovati tantissimi in queste condizioni). Arricchendo un po' il risultato si possono ottenere informazioni aggiuntive sui provider in uso per i vari domini così da mappare qualche fornitore o collaboratore. Aggregando un po' di dati pubblici il risultato diventa parecchio interessante.

<img src="{{ '/assets/images-posts/dnsmap-sample.png' | relative_url }}" alt="dnsmap sample" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

un mio test di aggregazione dati (script sul mio GitHub)

Un altro elemento da non sottovalutare è la tendenza, non diffusissima, a dare un nome dominio pubblico ad asset infrastrutturali come alcuni elementi di perimetro: il firewall, i router del provider o i proprio BGP router. Sono elementi che un attacker potrebbe individuare in molti modi più o meno complessi, se gli viene assegnato un record DNS ovviamente è un po' più facile.

La pratica di per se non è una cattiva idea, personalmente la trovo utile dal punto di vista della gestione IT ma potrebbe essere fatto su un nome dominio "di servizio" così da evitare di rendere questi asset immediatamente individuabili. Lo stesso principio vale per i sistemi non in esercizio: perché pubblicare le informazioni sulla zona dove ci sono i record dei servizi attivi quando possiamo parcheggiarli in una zona di servizio sconosciuta. Ovviamente questo accorgimento non renderà questi host invisibili, sarà però necessaria qualche azione in più per identificarli ed associarli al perimetro del target.

Nella mia repo GitHub ho messo a disposizione uno script che sto sistemando per aggregare dati provenienti da diverse fonti pubbliche, utile per chi lavora in ambito Penetration Testing e Red Teaming ma altrettanto utile per chi vuole farsi un veloce self-check: <https://github.com/roccosicilia/my-papers/blob/main/poc-recon/SubDomainDiscovery.py>. Lo script è in continua evoluzione quindi occhio alle note in cima.

Qualche suggerimento per ridurre il perimetro osservabile:

- banalmente pulite i record non più in uso, il DNS è un asset e va gestito come qualsiasi altro asset dell'organizzazione;
- utilizzate zone di servizio per scopi infrastrutturali;
- valutate cosa potete mettere dietro ad un proxy o ad un WAF in cloud;

Il principio è quello del tenere visibile solo lo stretto necessario evitando di regalare qualche appiglio a chi utilizzerebbe queste informazioni per affinare una strategia di attacco.
