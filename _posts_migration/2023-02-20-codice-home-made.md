---
layout:     post
title:      "Codice \"home made\""
date:       2023-02-20 13:30:00 +0100
categories: [cyber-security, hacking, ita]
image:
---
Molte figure con un background tecnico-informatico si dedicano alla scrittura di software per moltissimi motivi: dal puro piacere personale di costruirsi qualcosa di utile, anche solo per esigenze personali, fino ad arrivare ad esigenze operative o aziendali gestibili con un software custom. Personalmente ho scritto "molto" codice per automatizzare o velocizzare alcuni processi operativi ed analitici, anche in ambito Red Team è molto utile avere il proprio "arsenale" di tools custom. E' qualcosa di abbastanza diffuso nel mondo IT: ci sono aziende che si sono scritte il proprio gestionale, che automatizzano processi tramite script fatti dagli addetti ai lavori, team che creano software per consentire a clienti e fornitori di interfacciarsi con processi aziendali. Tutto questo in molti casi (non tutti ma molti) viene fatto senza un metodo di sviluppo adeguato e senza una particolare attenzione alla sicurezza del codice. Il problema parte dalle fondamenta: chi scrive molto di questo codice non ha nozioni di sviluppo di codice sicuro.

<img src="{{ '/assets/images-posts/codice.png' | relative_url }}" alt="codice" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

un mio blocco di codice a caso

Non ho le competenze specifiche per parlarvi di codice sicuro, faccio un altro *mestiere*, posso però raccontarvi cosa succede quando introducete codice "home made" in un contesto aziendale. I software sono asset della vostra infrastruttura a prescindere da chi li ha prodotti, che si tratti del nuovo CRM o dello script che vi notifica l'esito dei backup giornalieri il contesto è quello di un software attivo all'interno della rete, accessibile almeno ad una parte dell'utenza, che genera interazioni con altri sistemi.

Esattamente come tutti gli altri asset anche il software prodotto internamente va gestito nel tempo, nel suo ciclo di vita. Potrebbe essere necessario correggere dei bug funzionali, aggiornare delle componenti di terze parti (vedi il concetto di Software Bill of Materials che Paolo Perego accennava [qui](https://www.youtube.com/watch?v=SEFrcnUHAH8)), aggiornare le componenti core del software stesso. Quando adottiamo un prodotto software solitamente non ci preoccupiamo della qualità del software in modo diretto, ci si affida alla qualità del brand/partner che abbiamo selezionato. Uno dei parametri che probabilmente valuteremo è la frequenza con cui vengono rilasciate delle patch e la reattività del team di sviluppo in caso sia necessario correggere una vulnerabilità.

Abbiamo tutti imparato a limitare/eliminare l'utilizzo di software che presenta delle vulnerabilità, sappiamo che esistono vulnerabilità che consentono di manomettere il funzionamento dell'applicazione, possono consentire l'accesso a dati riservati e, in casi estremi, possono consentire l'accesso al sistema su cui è attivo il software vulnerabile. Questi rischi esistono nel software "enterprise" tanto quanto esistono nel software "home made", con la differenza che di solito il software disponibile sul mercato (o prodotto dalla community) transita da processi di controllo, è sottoposto a più tipologie di test sulla sicurezza ed esiste un team che ne corregge, in modo strutturato, i bug.

Ora il concetto è abbastanza semplice: nonostante i team di sviluppo composti da professionisti, i controlli integrati nel processo di sviluppo ed i test di sicurezza capita di rilasciare software che presenti delle vulnerabilità. Cosa ci fa pensare che noi, all'interno del nostro team IT/DEV, non commetteremo errori?

## Il punto di vista dell'attacker

In una sessione di attacco simulato, trovare qualcosa di "home made" potrebbe essere un ottimo punto di partenza per ottenere il controllo di un host sfruttando vulnerabilità abbastanza classiche. Ovviamente non è possibile generalizzare ma ci sono degli elementi facili da indagare che potrebbero restituire all'attacker l'appiglio per compromettere la macchina che ospita l'applicazione vulnerabile.

Considerando solo la mia esperienza diretta (e chissà quante ne potreste raccontare voi) mi potrei aspettare di trovare qualche vulnerabilità a livello di gestione dell'upload di contenuti (https://owasp.org/www-community/vulnerabilities/Unrestricted_File_Upload) con la conseguenza di poter portare sul sistema target un file malevolo sa eseguire successivamente tramite una chiamata http/https.

Altro grande classico, soprattutto in contesti dove sono presenti piccole integrazioni a livello di sistema, la possibilità di eseguire comandi sulla macchina remota tramite injection (https://owasp.org/www-community/attacks/Command_Injection). Spesso alcuni script di integrazione utilizzano chiamate al sistema operativo locale a cui passano delle stringe di comandi da eseguire direttamente in "shell". Altra grande opportunità per prendere possesso della macchina che ospita applicazioni di questo tipo.

In questi casi diventa relativamente semplice per un attacker sfruttare vulnerabilità anche molto gravi ma spesso non sottoposte a nessuna verifica di merito: essendo il software autoprodotto difficilmente ci sarà un processo di update della piattaforma o una verifica periodica delle nuove vulnerabilità. Eppure sarebbe abbastanza ovvio: come siamo abituati a chiedere il vulnerability assessment dei sistemi potremmo farso anche per il software prodotto internamente.

## Qualche risorsa

In relazione allo sviluppo di codice sicuro forse una delle risorse più note è la documentazione OWASP (<https://owasp.org/>), utilissima soprattutto per comprendere anche le varie tipologie di vulnerabilità di cui il nostro codice potrebbe essere afflitto.

Un bell'articolo introduttivo al tema che mi ero segnato è questo: <https://martinfowler.com/articles/web-security-basics.html>. Ottimo per chi vuole iniziare a capirci qualcosa.

Ci sono poi una tonnellata di libri specifici per i differenti linguaggi, non li ho letti quindi non mi permetto di dare consigli. Per segnalare qualche risorsa a noi geograficamente vicina, oltre a già citato canale e blog di Paolo, a settembre, in occasione dell'edizione 2023 di RomHack, ci saranno dei corsi tematici tra cui una sessione interamente dedicata alla sicurezza del codice: <https://romhack.io/training/code-review/>.
