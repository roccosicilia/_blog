---
layout:     post
title:      "Attack and Defense: post-live del 21 settembre"
date:       2022-09-22 21:00:00 +0200
categories: [cyber-security, hacking, ita]
image:
---
Non l'ho fatto per la prima live in coppia con [Andrea](https://www.adainese.it/), ho pensato di farlo per la seconda sessione di ieri sera sul canale di [Security Cert](https://www.twitch.tv/securitycert). Come ho raccontato un paio di settimana fa abbiamo in testa questa idea da qualche tempo ormai: condividere delle sessioni di analisi di un target per definire una strategia di attacco (lato mio) e una strategia di difesa (lato Andrea). Nella prima puntata abbiamo visto il contesto e la base di partenza del lab, una tipica VPS che espone una web app con qualche vulnerabilità. Ieri, in occasione della seconda puntata, abbiamo iniziato ad analizzare il target ed il questo post faccio un po' la sintesi di quello che ci siamo detti, ovviamente dal mio punto di vista.

<img src="{{ '/assets/images-posts/live_21092022.png' | relative_url }}" alt="live_21092022" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Qualche info di servizio prima di iniziare a discutere le azioni intraprese:

- il video della live è archiviato sul canale YouTube di SecurityCert e lo trovate [qui](https://www.youtube.com/watch?v=lPC_cunHrzU)
- sul mio canale porterò avanti le fasi di preparazione alla live, trovate la programmazione [qui](https://www.twitch.tv/roccosicilia)
- la prossima live è programmata per il 06/10/2022
- se volete partecipare attivamente alla sessione assieme ad Andrea (nelle azioni difensive) o assieme a me (nelle azioni offensiva) i dati di accesso all'ambiente vengono condivisi con i partecipanti alla sessione

## Cosa abbiamo di fronte

Tra le prime azioni intraprese abbiamo ovviamente eseguito una scansione del sistema target. Essendo una macchina di recente installazione che è solitamente off-line (il lab viene disattivato quando non siamo live) non vi è possibilità di utilizzare tecniche passive come l'analisi di precedenti versioni dell'applicazione (Wayback Machine) o i rilevamenti di scansioni terze (Shodan).

Con il più classico degli nmap abbiamo ottenuto l'elenco dei servizi:

- porta tcp\22 (ssh)
- porta tcp\80 (apache2)
- porta tcp\3306v (mysql)

L'accesso al DB è stato subito dall'esterno è stato quasi subito inibito da Andrea, in effetti non aveva senso e come prima azione ci era venuto in mente di tentare un brute force attack.

L'applicazione web espone un sito in Wordpress che abbiamo subito preso in esame. Come discusso il live la prima cosa che verrebbe in mente a chiunque è di utilizzare *dirb* per dare un occhio ai path esposti e *wpscan* per verificare lo stato dell'applicazione, cosa assolutamente sensata e lo faremo anche noi. Prima ho voluto lasciare spazio a qualche tools/servizio terze parti per vedere che tipo di info avrebbero portato all'attenzione. Ve ne cito alcuni tra quelli provati, dateci un occhio anche voi:

- https://www.getastra.com/website-scanner
- https://sitecheck.sucuri.net/
- https://www.ssllabs.com/ssltest/
- https://hostedscan.com/ (report via e-mail)
- https://quttera.com/
- https://www.siteguarding.com/
- https://observatory.mozilla.org/
- https://pentest-tools.com/website-vulnerability-scanning/website-scanner

Qualche elemento interessante da queste scansioni è emerso ma nulla di particolare, qualche risultato lo abbiamo commentato assieme in live. La scansione tramite wpscan da invece dei risultati molto chiari:

- vengono enumerati due utenti (admin e events)
- vengono rilevate tre plugin segnalate come out of date

Da una ricerca su wpscan.com emergono le potenziali vulnerabilità per:

- wp-advanced-search v3.3.3
- social-warfare <= 3.5.2
- wp-file-upload

Nel rilevare le informazioni base che ci consentiranno di definire un modello di attacco abbiamo discusso delle evidenze che le nostre azioni hanno generato, in particolare i log che Andrea riusciva chiaramente a ricondurre alle nostre azioni.

## ToDo per la prossima sessione

E' evidente che siamo stati troppo rumorosi e il parte questo era lo scopo della sessione. In un contesto di Penetration Testing potrebbe anche non essere un problema ma in ambito Red Team lo è. Quindi per la prossima sessione sicuramente dobbiamo dotarci di uno strumento per generare traffico realistico sul sistema.

Una volta che abbiamo la possibilità di confonderci nella mischia inizieremo a verificare la possibilità di utilizzare le vulnerabilità plausibili per costruire una tattica di attacco.

Continua.
