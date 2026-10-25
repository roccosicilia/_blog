---
layout:     post
title:      "Exchange 0-day, una settimana dopo."
date:       2021-03-10 09:00:00 +0100
categories: [cyber-security]
image:
---

Mi ero ripromesso di dedicare qualche minuto ad un approfondimento su quanto accaduto dopo la pubblicazione del post del [CSIRT](https://csirt.gov.it/contenuti/sfruttate-vulnerabilita-0-day-su-exchange-server-al01-210303-csirt-ita) ed aver atteso una settimana ha consentito di considerare diversi eventi e di approfondire alcune analisi così da elaborare qualche considerazioni su una situazione che, a parer mio, è tutt’altro che risolta.

I fatti sono noti a tutti: il 03 marzo viene annunciato da tutti i siti di settore che è stato individuato un attacco 0-day in grado di sfruttare una serie di vulnerabilità di Microsoft Exchange (2013, 2016, 2019) con l’obiettivo di compromettere il sistema e, potenzialmente, rubare informazioni sensibili come il contenuto della posta elettronica del server attaccato.

Come ho scritto in un [post](https://www.linkedin.com/posts/roccosicilia_cybersecurity-ethicalhacking-0day-activity-6773131640517525504-WbGN) poco dopo l’annuncio, si è trattato della “ricetta perfetta”: Exchange è largamente utilizzato da aziende medie e grandi, le vulnerabilità sono sfruttabili da remoto se il sistema espone funzionalità fruibili via https (cosa che ovviamente fanno tutti) e l’annuncio parlava di 0-day, non solo di vulnerabilità… quindi doveva essere chiaro che l’attacco era già cominciato.

Un post interessante lo trovate sul blog di [FireEye](https://www.fireeye.com/blog/threat-research/2021/03/detection-response-to-exploitation-of-microsoft-exchange-zero-day-vulnerabilities.html) dove vengono illustrati alcuni comportamenti osservati già da gennaio 2021 in relazione alle vulnerabilità CVE-2021–26855 e CVE-2021–26858. Le attività analizzate si riferivano allo sfruttamento delle vulnerabilità per il posizionamento di una web shell sul sistema target.

Quello che di fatto abbiamo osservato è che la fase “1” dell’attacco, relativa all’exploiting atto al posizionamento della web shell, era già in corso e sono certo che **molti di quelli che si sono apprestati ad installare le patch suggerite da Microsoft hanno potuto verificare la presenza della web shell** nel path c:\inetpub\wwwroot\apsnet_client\ del sistema Exchange sotto forma di file *.aspx; nel seguente [repo di GitHub](https://gist.github.com/JohnHammond/0b4a45cad4f4ed3324939d72dc599883) è stato riportato un elenco di possibili nomi dei file che vengono caricati attribuiti ad una famosa web shell nota con il nome di **China Chopper**.

> Note: questo potrebbe dar sostanza ai sospetti di Microsoft stessa sul gruppo responsabile di questa campagna di attacchi che si ritiene essere [HAFNIUM](https://blogs.microsoft.com/on-the-issues/2021/03/02/new-nation-state-cyberattacks/).

La prima doverosa nota tecnica si riferisce al comportamento dei firewall che tipicamente vengono configurati con un NAT per esporre i servizi di Exchange: molti firewall sono in grado di rilevare specifiche minacce grazie alle funzionalità di inspection, ma nel caso specifico l’azione avviene all’interno di una sessione HTTPS e quindi, a meno che il Firewall o il WAF non sia configurato per eseguire attività di SSL decryption, resta assolutamente invisibile al sistema di presidio del perimetro esterno.

Una volta portata a termine la prima fase dell’attacco, avendo a disposizione una web shell ricca di funzionalità, l’attacker è in grado di tentare ulteriori azioni anche contando sulla presenza delle altre vulnerabilità rese note nello stesso contesto (CVE-2021–26857 utilizzata per eseguire codice arbitrario sul sistema con utente SYSTEM e CVE-2021–27065 utilizzata per la scrittura arbitraria di file sul file system del server Exchange).

Nel caso specifico ciò che avviene è un tentativo di garantirsi un accesso persistente al sistema (il mio Red Team ha intercettato l’installazione di DLL e la registrazione di servizi al fine di garantire il dialogo persistente verso il server di Command and Control) e successive azioni che puntano al furto delle informazioni contenute nel sistema con particolare riferimento ai dati in memoria gestiti dal processo LSASS (quindi anche le credenziali) ed i dati presenti sul file system (le mailbox).

Le evoluzioni di questi comportamenti sono presentate anche [in un post di Microsoft](https://www.microsoft.com/security/blog/2021/03/02/hafnium-targeting-exchange-servers/) che è stato via via aggiornato e che da qualche spunto interessante.

Sulle azioni successive al primo exploit ci sono ulteriori elementi di analisi che possono essere utili ad una detection e mitigation dell’attacco. In particolare le attività che portano ad un dialogo verso il C2 server possono essere intercettate dai firewall che mettono a disposizione specifiche funzionalità di verifica del traffico e delle destinazioni. Una certa reattività potremmo aspettarcela anche dai sistemi di anti-exploiting di cui, spero, tutti facciate uso anche se, devo essere onesto, i rilevamenti fatti mi hanno lasciato perplesso su quest’ultimo fronte.

Per chiudere qualche suggerimento (banale ma doveroso):

- Non avere ancora installato i fix? Mi complimento per il coraggio… fateli ma mettete anche in conto una bonifica del sistema.
- Avete versioni precedenti di Exchange? Avete un problema ben peggiore perché state utilizzando un sistema end of support per gestire un asset fondamentale per la vostra organizzazione.
- Avete applicato i fix subito dopo gli annunci? Bene, assicuratevi che il primo exploit non sia stato lanciato e verificate il traffico del vostro Exchange server sul firewall.
- Precauzionalmente eseguite un cambio password del Domain Admin (due volte) e, già che ci siete, forzate un cambio password all’utenza.

Come sempre mi piacerebbe confrontarmi con chi si trova a gestire il problema all’interno delle organizzazioni. Ogni vostro contributo è prezioso alla community.