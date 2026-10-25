---
layout:     post
title:      "EDR lab: setup di base"
date:       2024-01-06 18:00:00 +0100
categories: [cyber-security, hacking, ita, study-with-me]
image:
---
Mi sono un po' intestardito con il tema EDR: come ho espresso in diverse occasioni tramite alcuni post su LinkedIn e sul VLOG, esiste un malinteso di base sulle capacita' di queste soluzioni, o meglio molti danno per scontato un livello di "autonomia" che queste soluzioni, by design, non hanno in quanto pensate per agevolare attivita' di analisi eseguite da un analista, una persona quindi. Non sono strumenti che fatto tutto da soli, vanno gestiti.

https://youtu.be/-cJX_cxYzyE

Puntata podcast con Andrea Dainese sul tema EDR.

Unisco quindi due esigenze di lavoro in un LAB dedicato: da un lato ho bisogno di migliorare e strutturare alcune tecniche di attacco in contesti dove e' presente un EDR, dall'altro lato voglio analizzare le potenzialita' di detection delle soluzioni di mercato o almeno quelle a cui posso accedere con le mie risorse. Elemento aggiuntivo del mio lab e' la verifica delle possibilita' di detection su device mobile: molti strumenti mettono a disposizione agenti per Android e iOS ma non ho mai avuto modo di lavorare attivamente su questi device.

## Struttura del LAB

Ho pensato di fare una cosa semplice:

- una guest Windows Server 2019
- una guest Linux (attacker)
- un vecchio smartphone Android
- soluzione EDR con console in cloud

<img src="{{ '/assets/images-posts/image-1.png' | relative_url }}" alt="image 1" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Come per quasi tutte le soluzione EDR che prevedono una Cloud Console e' indispensabile che gli endpoint comunichino verso l'esterno della rete.

## Primi test sulle funzioni di base

Come discusso nel podcast i moderni EDR introducono due funzioni principali sul piano della detection rispetto ai loro predecessori, gli anti-virus. Tali funzionalita' sono note come **analisi dinamica** e **analisi del comportamento**.

L'analisi dinamica osserva gli eventi del potenziale malware in esecuzione, solitamente utilizzando una sandbox: il file sospetto viene messo in condizioni di poter eseguire le sue attivita' ed il sistema EDR analizza gli eventi generati dal programma. Gli artefatti individuati vengono confrontati con gli IoC (indicatori di compromissione) noti per identificare attivita' malevole. Ad esempio se il processo ad un certo punto della sua esecuzione esegue una chiamata HTTPS verso un IP noto per appartenere ad una botnet, l'EDR interpreta questo evento come potenzialmente malevolo.

L'analisi del comportamento e' qualcosa di ancora piu' evoluto: l'allarme scatta quando una serie di eventi e' compatibile con una tecnica di attacco. Per esempio se il file malevolo cerca di eseguire una chiamata HTTPS verso un IP lecito, non presente tra gli IoC noti, il sistema EDR non ha elementi per capire se la chiama e' lecita o meno. L'analisi del comportamento prende in considerazione il fatto che l'evento, catalogabile come web-browsing nel caso in cui l'IP chiamato risponda a livello HTTPS, non e' stato generato da un processo che fa riferimento ad un browser ma da un processo eseguito per altre vie. Questo comportamento, di per se non malevolo, **risulta sospetto** in quanto simile al comportamento di un malware che cerca di contattare il proprio C2 o di inviare dati verso l'esterno. L'EDR generera' quindi un **alert per il comportamento sospetto**.

Questo in estrema sintesi il potenziale di detection aggiuntivo degli EDR; parlo volutamente di potenziale in quanto il tuning di queste funzionalita' e' tutt'altro che semplice troppo spesso trascurato.

Il mio obiettivo e' determinare il livello di sensibilita' degli EDR e valutare il livello di configurabilita' per far fronte a tentativi di compromissione tramite C2.

I miei test si concentreranno quindi sul far eseguire codice malevolo su un sistema target al fine di installare un C2 e governare da remoto il sistema vittima. Di alcuni EDR ho la certezza che alcuni comportamenti siano rilevabili gia' con il rule-set di base, ma questo non vale per tutte le soluzioni. Esiste gia' uno studio in merito che ha portato alla pubblicazione di una utility del MITRE che qui vi ricordo: [https://attackevals.mitre-engenuity.org/results/enterprise](https://attackevals.mitre-engenuity.org/results/enterprise?evaluation=turla&scenario=1).

In pratica si tratta di provare qualche tecnica di evasione in presenza di IoC e BIoC ben curati. Negli esempi di poco fa alcuni EDR si insospettiscono se la chiamata HTTPS viene eseguita verso servizi come pastebin.com mentre lo stesso comportamento verso una API di Dropbox risulta meno rumoroso. Test simili li abbiamo affrontati qualche mese fa (su [Patreon ci sono le LIVE](https://patreon.com/roccosicilia) della scorsa estate) dove mi ero limitato a trovare una tecnica utile ad alcune CyberOps che stavo preparando. Con questo nuovo lab vorrei provare altre opzioni ed aggiungere la componente di detection e hunting.
