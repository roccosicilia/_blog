---
layout:     post
title:      "Air-gapped Data Exfiltration: lab e p-o-c"
date:       2023-06-04 15:00:00 +0200
categories: [cyber-security, hacking, ita]
image:
---
Premetto che mi ci vorra' un po' di tempo a mettere insieme tutti i pezzi e ad arrivare ad una conclusione (spero) degna del tema. Ho iniziato a ragionare a questo lab qualche mese fa a seguito di alcuni confronti e dialoghi nati "sotto" alcuni miei post su LinkedIn in tema di Data Exfil. poi proseguiti su canale Telegram.

In sostanza mi attirava l'idea di sperimentare, in un contesto di Red Teaming, una tecnica air-gap per sottrarre informazioni al target. Ho voluto approcciare le cose un passo alla volta e nelle ultime settimane ho, a piu' riprese, lavorato a delle p-o-c di Data Exfil. utilizzando principalmente alcune tecniche particolarmente difficili da individuare come "[Exfiltration Over Alternative Protocol](https://attack.mitre.org/techniques/T1048/)" T1048, nella mia repo di GitHub trovate un po' di esperimenti. Ho approfittato per aggiornare i miei tools di lavoro strutturando meglio i C2 che utilizzo per i test di Exfil., ma soprattutto ho verificato quanto siano applicabili queste tecniche in contesti strutturati e ben protetti.

In un contesto di attacco che preveda un accesso fisico all'infrastruttura le possibilita' di portare un malware a bordo di uno dei sistemi della rete aumentano notevolmente. Tramite una delle tecniche viste nei lab di C2 possiamo far arrivera sul target un fileless malware che esegua, ciclicamente o su richiesta da parte dei C2, dei comandi. In questo caso ciò che vorrei provare è un semplice malware che legga il contenuto di un file e lo converta in segnali lumunosi binari da inviare ai led della tastiera esterna del PC "infetto".

Durante la live del 26 maggio abbiamo analizzato lo scenario e costruito una prima p-o-c (tutti i link alle risorse a fine articolo). E' stato un lavoro di squadra in quanto si è per prima cosa discusso il modello di comunicazione: ero inizialmente confidente di poter utilizzare tutti e tre i led della tastiera per inviare i dati ma, come da discussione disponibile in live, un suggerimento attivato in diretta si è rivelato più saggio. La trasmissione delle informazioni è stata quindi limitata a due led mentre il terzo led è stato utilizzato per dare un "ritmo" al segnale. Praticamente ci fa da clock.

Non voglio usare questo post per spiegare tutta la prima parte del lab, vorrei tener fede alla mia prima idea di fare un piccolo paper.

I risultati del primo esperimento sono disponibili qui:

- **[codice della p-o-c](https://github.com/roccosicilia/my-papers/blob/main/paper-AirGapped/rubber.ps1)**
- **[video della live (sono 2h e 45m)](https://www.patreon.com/posts/84049910)**

Prossimi step: ora che abbiamo una sequenza "luminosa" dobbiamo registrarla e trasformarla nel dato originale.
