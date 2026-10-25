---
layout:     post
title:      "Disponibilità dei dati/servizi e gestione del rischio"
date:       2024-07-22 15:00:00 +0200
categories: [cyber-security, ita, vlog-podcast]
image:
---
Utilizzo i fatti che hanno riguardato *CrowdStrike*, noto vendor in ambito EDR/XDR, per parlare di disponibilità dei dati e dei servizi. I fatto sono abbastanza noti e non mi metto a commentarli, vado direttamente al tema.

https://www.youtube.com/watch?v=HB4b7ykD-0k

VLOG dedicato al tema.

---

Se sei interessato ai temi che tratto e vuoi rimanere aggiornato ho messo a disposizione diversi canali tra cui un profilo [Patreon](https://patreon.com/roccosicilia) per gli argomenti più tecnici. Puoi rimanere aggiornato seguendo il mio blog:

Sono inoltre disponibili un canale [Telegram](https://t.me/+a7sF3JQV4bMzY2Nk) e un server [Discord](https://discord.gg/Ys5AAbsyyH).

---

## Premessa: è complesso ma non si vede

Le tecnologie che oggi utilizziamo in ambito informatico (anche in relazione alla sicurezza informatica) sono spesso progettate per nascondere un elevato livello di complessità. Le reti moderne sono complesse, i sistemi su cui girano i servizi utilizzati da tutto il mondo sono enormemente complessi, una qualsiasi azienda enterprise con più di 500 dipendenti (anche nella nostra piccola Italia sono più di 1600, [dati istat](https://www.istat.it/it/files//2023/11/REPORTCensimprese.pdf)) dipende da questi sistemi complessi:

- tante workstation e mobile quanti sono i dipendenti
- server farm con centinaia di sistemi
- reti aziendali e geografiche quante sono le sedi
- servizi in cloud di vario tipo spesso gestiti esternamente

Tutta questa "robe" richiede molta gestione, competenze verticali in diversi campi, specialisti sia in organico all'azienda che esterni e, ovviamente, strumenti per agevolare il processo di gestione.

Per i non addetti ai lavori questa complessità è invisibile oltre che spesso incomprensibile: a nessuno frega dei meandri dei sistemi informatici quando tutto va come deve andare. Le stesse aziende, con ragione, si interrogano su quali complessità mantenere i gestione interna e quali delegare: alcuni temi sono di una complessità tale da risultare più efficace ed efficiente una delega a team/aziende di settore (servizi gestiti, cloud, ecc.).

Ci siamo **abituati a non vedere la complessità e la fragilità** di questi sistemi. Lo ritengo un fatto e ovviamente è un errore.

## Gestione del rischio

In ambito sicurezza informatica mi capita spesso di dover sottolineare quando sia importante gestire il rischio cosa che transita da un elemento fondamentale: saper misurare il rischio.

Il mio sospetto è che si sia iniziato a trasferire il rischio sulla soluzione tecnica individuata senza aver considerato che questa più fallire. In tal caso è comunque necessario gestire un rischio a cui la tecnologia da sola non può far fronte: se è la tecnologia che ho scelto ad innescare il problema (cosa possibile anche se poco probabile) chi mi aiuta?

Chi fornisce il servizio è il vero attore con cui bisogna discutere di rischio e di piani di contenimento, i team operativi (interni o esterni nel caso di servizi gestiti da un provider) sono gli attori coinvolti. La tecnologia non si fa carico della gestione del rischio, è uno strumento, un facilitatore, un acceleratore.

## In contesto cyber sec.

La sicurezza informatica è uno dei tanti temi che, per sua natura, è iper-complesso. In pochi anno l'evoluzione delle minacce informatiche ci ha costretti ad incrementare competenze e strumenti e, pensi la cosa sia evidente, l'accelerazione tecnologica ha generato anche un po' di confusione. Vendo tantissime realtà che delegano alla tecnologia quando dovrebbero delegare ad un team in grado di governare le tecnologie. Il copione è sempre lo stesso: acquisizione di tecnologie bellissime ma sotto-utilizzate o gestite malissimo, tanto da causare anche danni.

Ora, il caso CrowdStrike è la tempesta perfetta: tecnologia gestita centralmente e distribuita su molti sistemi a cui si tende a delegare molto come tutti fate con i vostri EDR/XDR (vi vedo). Ma diciamoci la verità: quanti prodotti avete in esercizio che, in caso dovessero sfuggire di mano, vi metterebbero in ginocchio perché non avete valutato l'impatto di un potenziale problema?

E' improbabile? Certo che lo è, ma non per questo è impossibile. Il caso di cui si sta discutendo in questi giorni ci deve servire solo da promemoria: gestiamo sistemi iper-complessi ed iper-connessi che non sono infallibili. Questo è il punto di partenza di qualsiasi strategia di sviluppo e gestione delle nostre infrastrutture.
