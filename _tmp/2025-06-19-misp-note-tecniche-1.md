---
layout:     post
title:      "MISP: note tecniche (1)"
date:       2025-06-19 09:00:00 +0200
categories: [cyber-security, hacking, ita]
image:      /assets/images-posts/image-17.png
---
Probabilmente farò qualche post sulla parte di gestione tecnica/operativa di una installazione MISP che di base è un'applicazione web abbastanza stratificata e con diversi difetti di architettura che è bene conoscere. In questo primo post parlo di un tema di base: l'esigenza di tenere in partizioni separate l'istallazione di MISP che si compone della parte applicativa e del Database. Nota: non è un tutorial passo-passo su come si installa MISP, ne trovate una montagna online.

---

Se i miei articoli ti interessano e vuoi supportarmi nel mio progetto di divulgazione [**puoi sostenermi tramite il Patreon**](https://patreon.com/roccosicilia) e restare aggiornato iscrivendoti a questo blog.

[<img src="{{ '/assets/images-posts/image-14.png' | relative_url }}" alt="image 14" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />](https://patreon.com/roccosicilia)

---

L'assunto di base è semplice: MISP è uno strumento che serve a raccogliere dati ed è probabile che la quantità di informazioni in esso contenuta aumenti molto. È comunque opportuno ricordare che il processo di Threat Intelligence deve essere efficiente, vanno quindi selezionati i dati da raccogliere in quanto devono essere in grado di generare informazioni utili/cercabili sui nostri sistemi. Avere tera-byte di dati che poi non consumiamo è abbastanza inutile.

Per l'occasione ho fatto qualche test funzionale utilizzando una macchina del mio LAB: una Rocky Linux 8. L'istallazione di MISP è ben [documentata in questa repo](https://misp.github.io/MISP/INSTALL.rhel8.html) e per questa versione di Linux non dovreste incontrare grandi problemi. Ovviamente lo script da utilizzare per l'installazione [è questo](https://raw.githubusercontent.com/MISP/MISP/2.4/INSTALL/INSTALL.sh) che, come da documentazione, dovrebbe andare bene per "RHEL8/Rocky8.4/Rocky8.5/Fedora34/Fedora35". Noterete che ho utilizzato il condizionale... nonostante Rocky Linux sia citato in documentazione c'è un controllo che non consente l'installazione nell'install script:

Nell'attuale processo di installazione viene riportata una variabile "SUPPORT_MAP" con l'elenco delle architetture e distribuzioni supportate.

<img src="{{ '/assets/images-posts/screenshot-2025-06-16-at-15.24.06.png' | relative_url }}" alt="screenshot 2025 06 16 at 15.24.06" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

$SUPPORT_MAP della versione 2.4

Rocky Linux non c'è. Avendo un successivo controllo sulla versione del sistema operativo prima di far partire il processo di installazione, tutto si blocca. Il controllo si riferisce all'output di alcuni comandi per identificare architettura, distribuzione e versione:

<img src="{{ '/assets/images-posts/screenshot-2025-06-16-at-15.27.58.png' | relative_url }}" alt="screenshot 2025 06 16 at 15.27.58" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Controllo della versione

Il mio assunto di base, all'atto della preparazione del sistema, era che tra una RHEL 8 e una Centos 8 (entrambe supportate e citate nel file) e una Rocky Linux 8 le differenze a livello di pacchetti del sistema e delle repo siano relativamente trascurabili. Mi era quindi venuta voglia di "fixare" lo script di installazione ma mettendoci le mani ho visto che ci sono diversi riferimenti da sistemare. Non abbandono l'idea ma non lo faccio in questa occasione, per il test sono quindi tornato ad una RHEL 8 per utilizzare l'install script ufficiale che prevede l'installazione di MISP 2.4.

Nota: uno dei temi da considerare nell'uso di MISP è la gestione delle compatibilità con le diverse distribuzioni ed i pacchetti disponibili nelle repo di riferimento, non sottovalutate la cosa anche in ottica di futuri aggiornamenti.

<img src="{{ '/assets/images-posts/image-11.png' | relative_url }}" alt="image 11" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Experimental?

Nota: l'installer per RHEL 8 è tutt'ora experimental, preparatevi a qualche sistemata durante l'installazione.

## Qualche nota per l'installazione

La componente applicativa viene, di default, posizionata in /var/www/MISP e contiene sostanzialmente tutta l'applicazione. Il processo di installazione esegue il download tramite *git*, è quindi necessario assicurarsi di avere spazio a sufficienza considerando che una installazione da zero richiede circa 1,6 GB. Inoltre, i dati relativi agli eventi vengono ovviamente archiviati nel DB *MySQL/MariaDB* mentre *Redis* viene utilizzato per alcuni dati di backend (sto ancora studiando quali di preciso, ho iniziato a lavorare sul codice da poco) e per le funzioni di cache.

Non ci voglio girare attorno, MISP è un'assemblato di componenti e l'installazione si porta dietro una montagna di pacchetti software da gestire: la parte di gestione del sistema non è da sottovalutare. Una buona idea, giusto per mettersi comodi, è dedicare una partizione all'installazione, almeno per quanto riguarda la parte di applicativa ed il Database che, tra le altre cose, è destinato a crescere. Un metodo semplice ma efficace potrebbe essere quello di creare dei symbolic link per i default path */var/www/MISP* e */var/lib/mysql/misp*.

Come accennavo lo script di installazione non è esente da bug, ve ne racconto un paio incontrati da me su cui sto lavorando per proporre le modifiche allo script in questione. Nota importante: i **bug si riferiscono ai test fatti su RHEL 8, l'installazione su Ubuntu è andata liscia senza intoppi**.

**Database**  
L'installazione di MariaDB, in alcuni test, ha dato problemi in fase di installazione. L'installer tira dritto con una sfilza di errori quando deve poi creare lo schema. Per aggirare temporaneamente il problema è possibile installare i pacchetti prima di lanciare l'installer.

**Pacchetti**  
Per qualche ragione l'installazione del pacchetto git e redis ogni tanto non va a buon fine e ovviamente senza queste componenti l'installazione non procede. Anche in questo caso si può ovviare installato separatamente i pacchetti.  
Qualche problema lo danno anche alcune librerie installate via pip ma su questo fronte devo ancora approfondire i singoli errori.

**Apache**  
L'installer modifica la configurazione di apache al fine di configurare il virtualhost per l'applicazione. In questo processo viene anche modificata la porta su cui apache deve essere in ascolto con il comando:

```
sed -i '/Listen 443/!s/Listen 80/a Listen 443/' /etc/httpd/conf/httpd.conf
```

L'0'obiettivo è sostituire a "Listen 80" la stringa "Listen 443", evidentemente per lavorare in https. Il comando contiene un errore in quanto l'autore voleva probabilmente mettere in ***append*** la stringa "Listen 443" con il comando ***a***, cosa che non può essere fatta se si sta eseguendo una sostituzione. Il carattere ***a*** viene quindi interpretato come stringa e nel file httpd.conf troveremo "a Listen 443". Ovviamente in questo caso il file di configurazione contiene un errore di sintassi ed apache non potrà avviarsi.

## Next step

Non so se ha senso proporre un fix per quella che di fatto non è l'ultima versione di MISP per un sistema operativo con qualche annetto. Proverò quindi ad eseguire un test di installazione della versione 2.5 su versioni più recenti di RedHat e Rocky Linux e in caso di problemi vedremo come fixare l'installer.
