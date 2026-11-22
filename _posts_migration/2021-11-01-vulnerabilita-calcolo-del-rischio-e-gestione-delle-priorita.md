---
layout:     post
title:      "Vulnerabilità, calcolo del rischio e gestione delle priorità"
date:       2021-11-01 00:27:19 +0100
categories: [cyber-security, hacking, ita]
image:
---
In più occasioni mi trovo a discutere della differenza nella sostanza tra lo score di una vulnerabilità, rappresentato dal parametro CVSS, ed il rischio ad essa correlata che deve tener conto di diversi elementi del contesto.

L'output standard dei tools di scansione delle vulnerabilità potrebbe facilmente portare a considerare lo score della vulnerabilità come il parametro che determina il rischio. Potrebbe sembrare logico: se la vulnerabilità ha uno score alto significa che è particolarmente grave quindi rischio di più. Come [accennavo in questo post](https://roccosicilia.com/2021/07/07/individuazione-delle-vulnerabilita-attacco-e-difesa-prima-parte/) è necessario considerare anche l'impatto sul business dell'asset o del servizio su cui è individuata una vulnerabilità: a parità di score una vulnerabilità che affligge un sistema di posta elettronica, per fare un esempio, è ben più impattante di una vulnerabilità che affligge una SmartTV.

Fette le dovute premesse al post passiamo all'operatività partendo dagli strumenti che tipicamente vengono adoperati per eseguire la verifica delle vulneralità, ovvero i tools di scansione. Ne esistono molti, con più o meno funzioni e per tutte le ***tasche***. La funzionalità base comune a tutti i software di scansione è relativa alla generazione di un report che riporti l'elenco degli asset interessati dalla scansione e le vulnerabilità rilevate. Il report porta all'attenzione diversi dati tra cui lo score delle vulnerabilità (CVSS) accompagnato da altri parametri a supporto della comprensione della stessa.

Ultimamente ho avuto modo di operare su due piattaforme molto diverse tra loro: Nessus e Qualys. **Al fine di automatizzare parte del processo di rilevamento delle vulnerabilità e calcolo del rischio** ho condotto qualche prova di estrazione dei dati per agevolare il processo di creazione del remediation plan secondo una logica "rischio centrica".

<img src="{{ '/assets/images-posts/image.png' | relative_url }}" alt="image" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Test API

Entrambi i software, come molti altri, consentono di utilizzare le API per accedere ai report delle scansioni permettendo così di creare semplici script di estrazione ed elaborazione dei dati. Dovendo potenzialmente calcolare il fattore di rischio per decine se non centinaia di vulnerabilità automatizzare almeno una parte del processo è cosa saggia.

La ricetta, come abbiamo visto, è relativamente semplice e si basa su un minimo di due dati oggettivi (CVSS dato dalla scansione e Business Impact dato dall'asset inventory) e un dato analitico che personalmente mi piace aggiungere per avvicinare l'analisi al *mondo vero* e che potremmo pragmaticamente chiamare appetibilità.

Alcuni tools, come Qualys, consentono di censire dati anche per l'asset oggetto di analisi. In questo caso parametri come il Business Impact possono far parte dei dati base del report e possono essere utilizzati per calcolare un fattore di rischio. Altri tools, come Nessus, riportano i dati relativi alle vulnerabilità che dovranno poi essere analizzati tenendo in considerazione i dati gestiti dal sistema di asset manager.

<img src="{{ '/assets/images-posts/image-1.png' | relative_url }}" alt="image 1" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

p-o-c

Ovviamente mettere in relazione i dati provenienti da una scansione con i dati di un tool di asset management non è banale in quanto entrambi i sistemi devono poter mettere a disposizione le informazioni tramite una API. Personalmente credo sia anche il metodo più strutturato per gestire un piano di rimedio in quanto transita per la creazione di un processo di gestione degli asset e relativi strumenti IT.

Dall'altro lato sfruttando opportunamente le funzionalità di tools più ricchi è possibile arrivare ad ottenere, già nel report, un parametro che aiuti a qualificare il rischio. In questo caso il parametro da utilizzare per comporre il remediation plan potrebbe essere presente già nel report ed una volta raccolti i dati si potrà ottenere un elenco per priorità semplicemente "riordinando la lista" partendo dalla coppia host/vulnerabilità che riporta il rischio più alto.

Un ultimo step potrebbe essere quello di generare una notifica per il team IT dove riportare solo le vulnerabilità che risultano avere un fattore di rischio meritevole di considerazione secondo la policy scelta dall'organizzazione per la gestione delle vulnerabilità.

Nella p-o-c ho riportato qualche esempio di accesso alle API di Qualys e Nessus relative ai dati dei report: <https://github.com/roccosicilia/sToolz/tree/master/GetVulnReport>
