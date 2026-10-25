---
layout:     post
title:      "IDS, IPS ed analisi del traffico"
date:       2026-01-31 21:00:00 +0100
categories: [cyber-security, hacking, ita, study-with-me]
image:      /assets/images-posts/image-1.png
---
Qualche giorno fa ho parlato di [traffic sniffing](https://roccosicilia.com/2025/12/31/punto-di-sniffing/), argomento che mi avrebbe portato a parlare di Intrusion Detection/Prevention System e ad una ulteriore evoluzione del lab e dei test che potrò/potremo fare. Ho parlato di questi strumenti nella [serie dedicata ai temi Defense](https://www.patreon.com/collection/1640938?view=expanded) su Patreon che eventualmente potete utilizzare per approfondire la questione, in questo post andiamo direttamente sui temi operativi ed utilizziamo solo la componente IDS per i test. L'obiettivo di questo LAB è mettersi nelle condizioni di analizzare il traffico all'interno di una rete ed intercettare anomalie riconoscibili dalle peculiarità del traffico che si sta osservando.

## Lab Setup

<img src="{{ '/assets/images-posts/image-7.png' | relative_url }}" alt="image 7" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Schema di rete

Cercherò di dare più dettagli possibili così da consentire una replica del setup che ho utilizzato pur considerando che non è necessaria una replica esatta. Il mio lab si sta arricchendo di diversi elementi per i miei esperimenti di Penetration Testing e Detection in ambienti controllati e in questa occasione si è aggiunta la macchina che nello schema ho chiamato "detection1". Si tratta di una guest Ubuntu Server che ho intensione di utilizzare come base per gli strumenti di detection ed per il lab in questione è stato installato l'IDS Suricata.

> Nota: ci sono mille guide per installare Suricata a cui si aggiunge questo mio video in cui ho deciso di fare uno spiegone da zero:

Lo strumento IDS per funzionare deve ricevere una copia del traffico che transita in rete per poi analizzarlo a caccia di elementi che indichino una minaccia. Si può trattare di firme statiche, come uno specifico pacchetto o payload noto, o di pattern riconducibili ad azioni malevole. L'elemento da considerare per il setup del lab è il fatto che la sonda deve ricevere una copia del traffico, cose relativamente semplice in un ambiente virtualizzato in quanto possiamo configurare la porta della macchina sonda in modalità promiscua al fine di ottenere l'invio di tutti i frame relativi al traffico delle VMs anche alla NIC della sonda oltre che verso la porta di destinazione. Considerando lo schema di rete allegato sopra, la sonda sarà in grado di vedere tutto il traffico delle guest collegate al vSwitch.

<img src="{{ '/assets/images-posts/screenshot-2026-02-01-at-17.34.30.png' | relative_url }}" alt="screenshot 2026 02 01 at 17.34.30" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Conf. della NIC su vBox

Per rendere l'esperienza fedele ad un contesto reale ci servono anche altre due guest su cui indagare: nel caso del mio lab sono la macchina virtuale "kali" e la macchina virtuale "win 7" che, come suggeriscono i nomi, sono rispettivamente la macchina che useremo come base per lanciare gli attacchi e la macchina su cui predisporremo delle vulnerabilità *exploitabili* comodamente.

Per come è configurato il mio lab, con il firewall che è una guest sullo stesso host VirtualBox con la NIC "interna" sullo stesso vSwitch delle guest, anche il traffico da e verso internet per le guests del server viene replicato verso l'IDS. Questa configurazione ci tornerà utile nei labs in cui giocare con i C2.

## Suricata

Come detto nel mio home lab ho deciso di utilizzare Suricata come IDS configurato in modo da osservare tutto il traffico che transita dal vSwitch. In particolare nella mia configurazine ho attivato EVE (Extensible Event Format) che mi permette di avere il dettaglio JSON del traffico (utilissimo per portare poi i dati sul SIEM, ma sarà oggetto di altro post).

<img src="{{ '/assets/images-posts/screenshot-2026-02-01-at-17.44.38.png' | relative_url }}" alt="screenshot 2026 02 01 at 17.44.38" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Con questa configurazione, al netto delle regole di detection, disponiamo di un file di log in JSON che ci permette di avere un'ottimo livello di comprensione dei dati.

<img src="{{ '/assets/images-posts/image.png' | relative_url }}" alt="image" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Contenuto del log eve.json filtrando per la stringa "dns"

Ora che Suricata può vedere tutto il traffico e noi ci siamo messi nelle condizioni di poter visualizzare almeno i metadati (e qualcosa di più) possiamo istruire l'IDS con delle regole che cerchino specifici pattern o dati.

Ho pubblicato in video in cui ho illustrato alcune semplici regole che qui vi riporto, in particolare può essere interessante come creare una regola per intercettare uno specifico exploit come eternalblue:

```
  alert tcp any any -> any 445 (msg:"Possible ETERNALBLUE Remote Code Execution Attempt - Metasploit"; content:"|FF 53 4D 42|"; content:"|51 00|"; classtype:trojan-activity; sid:1000004; rev:1;)
```

In questo semplice esempio (che deriva da alcune analisi di hackers-arise.com) la regola genera un alert in caso venga osservato uno specifico contenuto definito con una sequenza di byte in un pacchetto TCP verso la porta 445.

https://www.youtube.com/watch?v=SHExfwfyj0Q

Video di sintesi

Questo tipo di regola è molto semplice, ma Suricata consente di creare regole molto più complesso basate su varie condizioni o comportamenti.

## Next step

Mentre scrivevo questo post e registravo il video mi sono reso conto che potrebbe essere utile per chi segue questi contenuti disporre di un lab minimale con cui giocare. Ho deciso che nelle prossime settimane preparerò degli articoli tecnici con lo step by spet per la creazione del lab di base. Ci metterò un po' ma è anche la scusa per discutere delle diverse tecnologie utilizzate.

---

Se questo tipo di contenuti ti interessa e lo trovi utili per i tuoi studi o il tuo lavoro puoi sostenere il mio progetto di divulgazione iscrivendoti ai miei canali, in particolare su [YuoTube](https://youtube.com/@roccosicilia) e [Patreon](https://patreon.com/roccosicilia). Puoi rimanere aggiornato su quello che faccio iscrivendoti a questo blog:
