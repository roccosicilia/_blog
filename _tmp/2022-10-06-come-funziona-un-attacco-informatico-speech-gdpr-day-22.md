---
layout:     post
title:      "Come funziona un attacco informatico (speech GDPR day '22)"
date:       2022-10-06 08:00:00 +0200
categories: [cyber-security, ita, update]
image:
---
Il 5 ottobre ho presenziato al [GDPR day](https://www.gdprday.it/) organizzato dal super [Federico Lagni](https://www.linkedin.com/in/federicolagni/) a Bologna. Quest'anno il [mio team](https://www.linkedin.com/company/versivo-security/) ha partecipato con una sponsorizzazione all'evento che ha l'obiettivo, che condivido pienamente, di **formare** oltre che informare.

Per 25 minuti abbiamo raccontato uno spaccato di realtà di come operano i threat actor (anche io uso un po' di parole fighe ogni tanto) illustrando le fasi di un tipico attacco, tratto da esperienze sul campo, per analizzarlo assieme e comprenderne i meccanismi. L'obiettivo è, come spesso racconto, conoscere meglio il nostro "nemico" e, di conseguenza, comprendere come difenderci in modo efficace.

In questo post, che probabilmente sarà un po' lungo, voglio raccontarvi quello di cui abbiamo parlato. Ovviamente leggerlo su queste pagine non è uguale ad ascoltarlo durante la sessione con la possibilità di interagire e discuterne assieme, ma confido in future occasioni alle prossime edizioni di questo o altri eventi.

## Fasi di un attacco

Spesso si ha l'idea che un attacco sia una singola e deflagrante azione, un singolo colpo. Ciò che avviene è in realtà molto diverso sia per la quantità di attività che precedono l'azione di attacco vero e proprio che per i tempi che queste attività richiedono. Gli addetti ai lavori parlano infatti di "fasi" di un attacco informatico. Esistono diversi modelli che sintetizzano le fasi di un attacco di cui nell'immagine che segue ne riporto uno relativamente recente in riferimento ad una specifica tipologia di attacco: i ransomware.

<img src="{{ '/assets/images-posts/ransom_lifecycle.png' | relative_url }}" alt="ransom_lifecycle" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Più in generale l'attacker inizia la sua attività da una fase ricognitiva in cui raccoglie informazioni sul target. Ognuno di noi, sia come individui che come membri di una organizzazione, semina diverse tracce ed informazioni in rete sul proprio conto: contatti, abitudini, preferenze, qualifiche. Questo patrimonio di dati viene raccolto ed analizzato al fine di costruire un modello del target da studiare; ovviamente vi è una proporzionalità tra l'accuratezza della *profilazione* e la quantità di informazioni disponibili.

Alcune informazioni possono essere reperite grazie ad azioni più invasive come una campagna di phishing mirata e studiata appositamente per entrare in possesso di una credenziale valida. Altre potrebbero non richiedere azioni dirette verso il target: in alcuni casi l'attacker potrebbe accedere o acquistare informazioni o dati relativi a precedenti azioni offensive verso l'organizzazione o ai datti di uno dei dipendenti.

Facciamo un paio di esempi pratici per comprendere meglio che dati possono essere utilizzati contro di noi ed in che modo vengono reperiti.

## Banking scam

Un'azienda si rende conto di aver subito una truffa bancaria: un cliente afferma di aver provveduto ad un pagamento a seguito di una email da parte di uno dei commerciali dell'azienda ma tale pagamento non è mai giunto a destinazione.

Dal DFIR report (Digital Forensics and Incident Response) emergono alcune evidenze:

- l'email inviata al cliente risulta essere autentica
- viene identificato un accesso non autorizzato all'account email del commerciale
- la password dell'email personale del commerciale è disponibile su "have I been pwned"
- l'account del commerciale non dispone di MFA

Con queste informazioni certe in mano possiamo cominciare ad ipotizzare cosa sia successo.

Partiamo dalla cattiva abitudine di riutilizzare password in diversi account. Ne parlo spesso: se la credenziale è la stessa o simile per tutti gli account ovviamente siamo nella condizione in cui anche un solo breach possa avere impatto verso tutti i nostri account. Nel caso specifico la credenziale individuata dall'attacker era quella dell'account di posta elettronica personale del dipendente. E' già un caso abbastanza eclatante, molto più frequentemente vengono sfruttati data breach di servizi anche molto banali e forse considerati di bassissimo impatto per l'utente che ne fruisce. Potrebbe essere il portale della biblioteca comunale o il sito di un piccolo esercizio dove siamo clienti occasionali. Non importa, se utilizziamo la stessa password che utilizziamo per la posta elettronica aziendale stiamo semplicemente aumentando la superficie attaccabile.

L'assenza di MFA riduce la complessità di una azione offensiva: sarebbe stato molto più complesso e probabilmente non fattibile per l'attacker accedere all'account di posta elettronica se l'organizzazione avesse implementato questo tipo di tecnologia. Da sottolineare che anche in questo caso vi sono metodi di bypass che fanno conto sull'ingenuità e sulla pigrizia degli utenti (parleremo in un altra occasione degli attacchi alla MFA).

Per chi è del mestiere la situazione è già abbastanza chiara. L'attacker ha trovato una credenziale valida e si è assicurato un accesso al servizio di posta da cui ha potuto comodamente consultare i contenuti, gli scambi, i contatti della vittima. Una volta contestualizzato il tutto è stato scelto un cliente con cui la vittima abitualmente dialogava per inviare una email di cambio coordinate bancaria.

Nella sua semplicità l'attacco è estremamente efficace e ci si rende conto di ciò che è avvenuto a cose ormai fatte. Ragionare sui modelli utilizzati dagli attacker per eseguire azioni offensive ci consente di individuare dove l'organizzazione deve migliorare:

- c'è sicuramente un tema di awareness da considerare visto l'utilizzo un po' ingenuo delle credenziali da parte della vittima
- probabilmente qualche presidio di sicurezza in più per i servizi IT non sarebbe male, abbiamo parlato di MFA ma anche un controllo sulle tipologie di accesso aiuterebbe
- è evidente che non ci sono o non vengono rispettare procedure di verifica delle comunicazioni laddove vi è uno scambio di informazioni sensibili o che toccano processi CORE come la fatturazione e la gestione del credito

Il ragionamento può essere esteso alle metodologie di assessment utili ad eseguire una qualifica dei punti deboli di un'organizzazione al fine di costruire un piano di rimedio coerente con le effettive esposizioni che il target presenta agli occhi di un attacker. L'idea è quindi di spostare il focus, il più velocemente possibile, sulle azioni da compiere per ridurre la superficie attaccabile laddove l'esposizione corrisponde ad una opportunità reale di attacco con relativo impatto sul business.

Ancora una volta prima degli strumenti viene la **cultura** e la **consapevolezza**.

Condivido le slide presentate anche se, come sempre, hanno più senso se commentate. Se l'argomento è di interesse (attendo feedback) valuto la registrazione di una presentazione del contenuto per intero. Qui allego le slide:

[versivo-gdpr-day](https://roccosicilia.com/wp-content/uploads/2022/10/versivo-gdpr-day.pdf)[Download](https://roccosicilia.com/wp-content/uploads/2022/10/versivo-gdpr-day.pdf)
