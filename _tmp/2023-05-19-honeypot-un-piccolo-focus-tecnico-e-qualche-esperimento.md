---
layout:     post
title:      "Honeypot: un piccolo focus tecnico e qualche esperimento"
date:       2023-05-19 13:00:00 +0200
categories: [cyber-security, hacking, ita]
image:
---
Altro argomento affascinante che vale la pena approfondire. Il mio interesse su fronte degli honeypot e' duplice: da un lato - quello ***blue*** sono uno strumento che ritengo utile in una strategia di gestione delle minacce cyber, da un altro lato - quello ***red*** - sono una trappola da imparare a riconoscere ed aggirare.

Giusto un cenno sulle motivazioni che stanno dietro l'utilizzo di questo strumento. Di base abbiamo due ambiti:

- Ricerca, vengono utilizzati per analizzare i comportamenti dei threat actor dai big player della cyber sec. al fine di catalogare nuove tecniche e mogliorare la detection dei prodotti di mercato
- Produzione, vengono utilizzati dalle aziende per intercettare eventuali tentativi di compromissione anche nelle fasi iniziali

Sono entrambi contesti molto interessanti, il mio focus in questo periodo e' il contesto di produzione e, come ho scritto in [questo post](https://www.linkedin.com/posts/roccosicilia_cybersecurity-honeypot-activity-7064148816010051584-SgAk?utm_source=share&utm_medium=member_desktop), e' indispensabile per chi approccia questo strumento aver bene in mente che si tratta di qualcosa che va gestito per renderlo utile. Gli honeypot di base espongono dei servizi pensati per attrarre l'attacker che, se ingannato, andra' a sollecitare il sistema il quale produrra' un notifica. Queste notifiche devono ovviamente essere trattate esattamente con un security incident, altrimenti il gioco non funziona.

E' possibile anche spingersi oltre, ad esempio costruendo servizi che consantano all'attacker di interagire cosi' da leggere anche i comportamenti successivi alla compromossione del sistema come l'installazione di un C2 o i tentativi di lateral movement.

## Progetti open souce

Ci sono diversi progetti open source che possiamo prendere in considerazione per "giocare" o anche per mettere in produzione una soluzione custom che non necessiti di decine di honeypot. Opinione mia: se abbiamo intenzione di dotarci di questo strumento valutiamo tra le prime cose l'estensione del progetto prima di scegliere il tipo di soluzione; le soluzione open source attualmente disponibili non prevedono particolari sistemi di gestione centralizzata e sono piu' indicate per chi dovra' gestire un numeno non alto di items.

Qui un elenco di alcuni honeypot dai cui puo' aver senso iniziare: <https://github.com/paralax/awesome-honeypots>. Nel lavoratorio che sto attrezzando ne utilizzero' alcuni per studiarne il comportamento. Cito anche due progetti molto strutturati per chi ha esigenze, a mio parere, piu' di ricerca che di detection:

- T-POT https://github.com/telekom-security/tpotce
- OWASP Honeypot https://owasp.org/www-project-honeypot/

## Soluzioni di mercato

I vendor si sono ovviamente mossi anche in questa direzione e propongono per lo piu' soluzioni che sono in grado di distribuire e gestire honeypot configurabili. E' abbastanza evidente, alcmeno per me, che si tratta di soluzioni particolarmente calzanti per chi deve "seminare" diversi honeypot nelle proprie reti. Qui un elenco non completo di soluzioni di mercato: <https://www.g2.com/categories/deception-technology>.

## Laboratorio di base

Giochiamo un po' con un piccolo laboratorio costituito da una semplice VM linux che espone unicamente il servizio SSH "reale" (che non prendiamo di mira) e proviamo a dotarla di un po' di elementi tipici di un honeypot. Il contesto del mio studio e' l'ambiente enterprise con esigenze di detection, non la Threat Intelligence.

Come primo esperimento ho deciso di simulare un servizio molto semplice e credo abbastanza appetibile: telnet. Per diverse ragioni il servizio viene spesso preso di mira: solitamente lo si trova in uso in sistemi relativamente datati dove e' plausibile supporre ci siano delle falle da sfruttare, se non in remoto almeno localmente.

Mi sono fatto dare una mano dalla libreria socket di Python 3. Il funzionamento di base e' semplice: una socket aperta sulla porta TCP 23, un loop per ricevere i dati dal client e dare degli output lato server. Come primo esperimento il risultato non e' pessimo ma ci sono dei dettagli al codice che vanno migliorati. Di base lo script simula il comportamento di una sessione telnet: presenta un banner e chiede una credenziale. Ogni tentativo di connessione e di inserimento dati viene riportato in un log. Anche una sollecitazione non prevista come una scansione registra il tentativo di accesso al servizio:

<img src="{{ '/assets/images-posts/honeypot-scan.png' | relative_url }}" alt="honeypot scan" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

scan con flag -sT e -sS

Da notare che una SYN scan non viene rilevata in questa versione del programma: utilizzando la libreria socket per avviare un servizio in TCP la sessione viene instaurata sono al termine di tutto il processo di handshake, in questo caso non c'è nessuna sollecitazione a parte il primo SYN e di sconseguenza non c'è tracciamento alcuno.

Come accennavo uno degli obiettivi del lab è cercare di capire quanto siano riconoscibili gli honeypot. In questo caso la scansione ci da solo informazioni in relazione al fatto che la porta TCP 23 è aperta, per capire qualcosa di più dovremmo dare un'occhiata al traffico che scambiamo con il nostro target. Possiamo usare wireshark per analizzare il traffico e constatare che abbiamo davanti una vera sessione telnet o meno.

Per fare la prova da un punto di vista obiettivo dobbiamo utilizzare wireshark dalla macchina dell'attacker, in questo lab utilizzo una classico Ubuntu 22.10 server come base per l'honeypot ed una Kali Purple (la sto provando in queste settimane) per l'analisi del target. Il comportamento di nmap lo abbiamo gia' visto: se facciamo una scansione TCP rileviamo il servizio ma ci facciamo anche individuare, passiamo ad analizzare il traffico con una connessione alla socket:

<img src="{{ '/assets/images-posts/wireshark-telnet-honeypot.png' | relative_url }}" alt="wireshark telnet honeypot" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

wireshark verso honeypot

La sessione e' molto semplice, appare esattamente come una sessione TCP sulla porta 23 e dopo il three-way handshake il finto server telnet manda al client il banner di login. Vediamo ora una vera sessione telnet su un altro server linux su cui ho installato il demone:

<img src="{{ '/assets/images-posts/wireshark-telnet-srv.png' | relative_url }}" alt="wireshark telnet srv" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

wireshark verso telnetd

La differenza e' abbastanza evidente, pur trattandosi di una sessione TCP sulla porta 23 il server telnetd invia diversi dati al client che risponde con altrettante informazioni. Solo alla fine di questo scambio il server invia al client il banner di login.

Ci portiamo a casa che se vogliamo costruire un servizio a media o elevata interazione il dialogo deve necessariamente rispettare il protocollo. Resta comunque vero il fatto che per smascherare la trappola tramite l'analisi del traffico bisogna farla scattare. In contesto enterprise con gli honeypot posizionati all'interno della rete potrebbe essere un NON problema in quanto qualsiasi cosa faccia scattare una trappola interna probabilmente e' un evento degno di nota.

## Un lab un pelo piu' avanzato (anticipazione)

Usare protocolli come telnet o ssh richede di "ricostruire" la comunicazione per essere credibili. Se ci spostiamo su un protocollo come http il gioco si fa un po' piu' interessante. Creare un http server in python anche solo con una socket e' molto semplice e anche la conversazione tra client e server non e' nulla di particolarmente complesso. La versione http dell'honeypot potrebbe quindi essere molto piu' credibile ed interessante.

Ho preparato una p-o-c per http disponibile nella stessa repo della versione telnet: <https://github.com/roccosicilia/my-papers/tree/main/poc-honeypot>. Nella live di questa sera parto dal server http in python per provare a costruire un servizio ad alta interazione, nella seconda parte di questo post riportero' gli esiti.
