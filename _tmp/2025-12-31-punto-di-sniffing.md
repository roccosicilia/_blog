---
layout:     post
title:      "Punto di \"sniffing\""
date:       2025-12-31 18:09:26 +0100
categories: [cyber-security, hacking, ita]
image:      /assets/images-posts/youtube-live.png
---
In questi giorni ho rimesso mano al mio home lab aggiungendo qualche pezzo ed in particolare mi sono dotato di una componente hardware che solitamente, per esigenze di spazio e comodità, utilizzavo nelle sue versioni software e decisamente più limitate: lo switch.

Purtroppo non ho la possibilità di installare un vero rack con le relative componenti (spazio limitato), ho quindi ripiegato su alcuni strumenti che potessero comunque assolvere ai rispettivi ruoli mantenendo le dimensione del lab fisicamente ridotte.

> I dettagli sulla configurazione di base sono disponibili in questo post su Patreon: "[Nuovo lab (infrastruttura di base)](https://www.patreon.com/posts/nuovo-lab-di-146519953)".

L'esigenza di uno switch "vero", anche se non è esattamente uno switch quello che ho adottato, si riferisce ad alcuni test che vorrei fare sulle possibilità di detection a livello rete. In diverse occasioni, durante le attività di PenTesting, mi auto-impongo dei limiti in relazione all'utilizzo di specifiche tecniche di discovery, scansione ed enumerazione dei sistemi in quanto gli strumenti di network detection potrebbero facilmente identificare alcune tipologie di traffico.

A livello empirico so che alcune utility sono più "silenziose" di altre ma non ho mai approcciato la cosa in modo scientifico, ovvero non mi sono mai messo a controllare - sniffare - il traffico di ogni singola utility per vedere il dettaglio del traffico che genera e che tipo di detection rule fa scattare. Quello che spesso ho fatto è stato analizzare le funzionalità delle utilities e ricrearle in tools custom che utilizzo su campo. **È così che è nato il mio amore per scapy**.

Questa esigenza permane e con il tempo si estende a sempre più funzionalità presenti in diversi strumenti. Ricrearle tutte in una versione custom sarebbe estremamente inefficiente, ho quindi pensato di riprendere il task e strutturarlo meglio: tramite il mio home lab andrò ad analizzare il traffico dei tools che utilizzo più frequentemente e lo sottoporrò alle più frequenti detection rules. L'obiettivo è trovare dei setup che non facciano scattare allarmi e, laddove non possibile, trovare delle alternativa valide che mi consentano di rimanere silenzioso in rete.

Per sniffare tutto il traffico comodamente e senza rischiare di perdere pezzi ho pensato che dotare il lab di uno switch fosse la scelta migliore ed in effetti avendo la possibilità estrarre un dump completo di tutto quello che è connesso al device (tutto il lab) la scelta risulta la più logica.

https://www.youtube.com/watch?v=nCHDDqJH9BE

*Video demo*

Nota importante -- VirtualBox, come molti software di virtualizzazione, utilizza dei virtual-switch per fornire una rete virtuale alle VMs. Condividendo il virtual-switch o una NIC (ad esempio in configurazione di bridge) il traffico L2 "intra VMs" verrà gestito direttamente dall'host. Questo significa che sullo switch HW sarà possibile intercettare il traffico tra un host fisico ed una guest ma non tra due guest attive sullo stesso host.

Possiamo fare un semplice test per verificare sia la possibilità di intercettare il traffico tra un host fisico ed una guest, sia per accertarci dell'impossibilità di vedere il traffico tra due guest nella stessa rete posizionandoci sullo switch fisico.

<img src="{{ '/assets/images-posts/image-1.png' | relative_url }}" alt="image 1" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

*Dettaglio del lab*

Questo dettaglio è importante da comprendere in un contesto di Network Detection: le la sonda IDS opera "solo" sulla base del mirroring del traffico di uno switch fisico (il CORE switch ad esempio) potremmo trovarci nelle condizioni di trascurare importanti porzioni di traffico.

Nel test ho eseguito una cattura del traffico dal sistema RouterBoard ed in particolare è stato raccolto, per qualche secondo, il traffico del bridge denominato "bridge-lan" che sostanzialmente rappresenta lo switch a cui sono fisicamente cablati il mio laptop e l'host su cui gira VirtualBox (lo schema sopra è abbastanza fedele).

Le NIC in LAN delle due VMs sono in configurazione di bridge con la NIC fisica dell'host connessa direttamente al RouterBoard, questo mi consente di ottenere la comunicazione L2 tra tutti i sistemi ma, come detto, il traffico tra le due guest non transita dal mondo fisico e non può quindi essere raccolto dal RouterBoard.

<img src="{{ '/assets/images-posts/image.png' | relative_url }}" alt="image" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

*Estrazione del pcap da MikroTik*

Analizzando il pcap è infatto possibile vedere il traffico RDP tra il mio laptop e l'host su cui gira VirtualBox ma non c'è traccia del traffico che stavo generando tra le due VMs (ICMP e HTTP).

<img src="{{ '/assets/images-posts/image-2.png' | relative_url }}" alt="image 2" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

*Porzione del traffico intercettato*

Ovviamente resta possibile raccogliere ed analizzare il traffico che resta configurato all'interno del virtual switch: è sufficiente inserire nella virtual-network una macchina con una vNIC in modalità promiscua da utilizzare come sonda passiva.

---

Se i miei articoli ti interessano iscriviti al canale [YouTube](https://youtube.com/@roccosicilia) e [Patreon](https://patreon.com/roccosicilia) per supportarmi, iscriviti al blog per rimanere sempre aggiornato:
