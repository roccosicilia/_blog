---
layout:     post
title:      "[eg0n] Il processo di \"raccolta\" degli IoC con un esempio"
date:       2025-08-11 08:00:00 +0200
categories: [cyber-security, hacking, ita]
image:      /assets/images-posts/parlo-di-ioc-e-threat-intelligence-fai-una-cosa-semplice-1.png
---
Questo post è una serie di riflessioni a *voce alta* legata al progetto [eg0n](https://github.com/b1th0rn/eg0n).

Uno degli obiettivi di base a cui non vogliamo/voglio rinunciare è arrivare a generare delle liste di IoC immediatamente consumabili dai sistemi di detection/protection come Firewall, IDS, EDR e tutte le soluzioni a cui affidate la sicurezza della vostra rete. Questo risultato richiede dei passaggi sui cui stiamo ragionando assieme e che probabilmente rivedremo nel corso del progetto.

Abbiamo affiancato ad **eg0n** una istanza **MISP** - <https://misp.bithorn.org> - per mettere a disposizione della community uno strumento che è oggi considerato uno standard per quanto riguarda la raccolta e l'analisi degli IoC. MISP è un software molto utile ma con tante limitazioni (ne ho parlato recentemente in un video che vi riporto qui sotto) e non poteva essere lo strumento definitivo per il progetto.

https://www.youtube.com/watch?v=VGnmxReucsI

Il video fatto in collaborazione con @esadecimale

La raccolta può avvenire in diversi modi, quelli di cui possiamo disporre a T0 sono i dati forniti dagli analisti che partecipano al progetto ed i dati forniti tramite gli honeypot. Con questo set di base di informazioni è possibile portare sull'istanza MISP l'analisi di eventi legati ad azioni di Threat Actor con i relativi artefatti individuati. In questo processo la cura per il dettaglio deve essere maniacale: più sono le informazioni che vengono portate sulla piattaforma e più è probabile arricchire e correlare dati con altri eventi tracciati e registrati dalla community.

Vorrei inoltre evitare gli "errori" che ho visto commettere in altre MISP community: è vero che di base si tratta di un "grosso DB" molto articolato ma la cosa peggiore che possiamo fare è usarlo come un elencone di artefatti. Provo a spiegarmi meglio: ovviamente all'interno di un evento devono essere inseriti gli artefatti utili all'analisi ma devono essere ripotati anche gli elementi di contesto. **MISP documenta l'evento con tutti i suoi elementi**, gli artefatti sono alcuni degli elementi.

Probabilmente la cosa migliore è fare un esempio e quasi certamente farò dei video dedicati all'argomento. Supponiamo di voler documentare un evento specifico come una campagna di phishing: per prima cosa va considerato se ha senso creare un evento nuovo o se di tratta di informazioni che possono arricchire eventi esistenti.

<img src="{{ '/assets/images-posts/image-2.png' | relative_url }}" alt="image 2" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Una selezione di SPAM / Phishing

Se buttate un occhio nella posta elettronica che automaticamente il vostro provider vi propone come SPAM potreste trovare qualche esempio con cui esercitarvi. Ho preso alcuni eventi recenti di un mio account e sembrerebbe che nel mese di luglio (non ho evidenza del passato in quanto faccio pulizia) si è mosso qualcosa per il brand visibile come mittente nello screenshot. Analizzando il contenuto possiamo andare a caccia di elementi per capire se si tratta di banale SPAM o se è qualcosa di più vicino alla truffa o al phishing.

## Elementi legati alla comunicazione

Sto argomentando un esempio e vorrei cercare di non tralasciare dettagli. Le e-mail sono, come si sa, uno strumento di comunicazione per mandare un messaggio ad "A" a "B". Affinché io possa scrivere una e-mail a qualcuno è necessaria una certa infrastruttura di base e dei servizi tra cui la connessione ad Internet (ovvio) ed i servizi di posta elettronica (ovvio). Questi servizi funzionano grazie al fatto che esistono altri servizi come il DNS. Per farla breve, quando inviamo una email succedono un sacco di cose che l'utente non vede ma di cui abbiamo delle tracce all'interno del messaggio di posta elettronica, o meglio, nel suo header.

In questo caso specifico dall'integrazione possiamo sicuramente recuperare l'**indirizzo email del mittente**, il **domain name** associato ed il **server** che è stato utilizzato per inviare il messaggio di posta elettronica:

```
[...]
From: <info_fty@webin-764.non.nsp.mk.ua>
[...]
header.from=webin-764.non.nsp.mk.ua
[...]
Received: from static.114.69.180.157.clients.your-server.de
[...]
```

Questi dati sono al momento semplici elementi tecnici e, mentre l'indirizzo email è facilmente manipolabile dal mittente, domain name e IP del server da cui è partito il messaggio sono più difficili da manipolare e in questi casi forse è anche poco utile.

## Elementi legati al contenuto

Nel corpo del messaggio ovviamente ci sono elementi che possiamo prendere in considerazione per capire meglio il contesto. In particolare quando si tratta di phishing potremmo provare elementi come tracker, link a siti esterni e allegati. Ogni elemento ha una funzione specifica.

I tracker consentono al Threat Actor di capire se l'e-mail è stata visualizzata e consente di ottenere alcune informazioni di base come l'IP pubblico della rete della vittima. Solitamente sono inserito come link all'interno dell'email o come contenuto esterno (es: una immagine) che il client può caricare.

<img src="{{ '/assets/images-posts/image-3.png' | relative_url }}" alt="image 3" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Estratto degli "href"

Essendo solitamente dei link li su può individuare andando a caccia dei tag href all'interno del corpo dell'email. Ne esistono due in questo caso e come si vede dalla URL si tratta di un link che puntano ad una risorsa Google ed in particolare ad un GCP Bucket con nome "lijhy".

Se si va ad analizzare la risposta alla GET vediamo meglio cosa succede, vi risparmio i vari "jump" e vi riporto lo screenshot relativo al caricamento del contenuto del bucket (ammesso stia interpretando correttamente):

<img src="{{ '/assets/images-posts/image-4.png' | relative_url }}" alt="image 4" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Analisi della risposta (BurpSuite)

Sulla destra si vede chiaramente il contenuto del bucket con la chiamata JS responsabile della redirect:

```
document.location.href = 'http://static.148.85.180.157.clients.your-server.de/' + fragment;
```

La variabile *fragment* è valorizzata poco sopra ed equivale a tutto ciò che viene passato in URL dopo il carattere *#*. In pratica la URL viene riscritta modificando il solo dominio di destinazione. I due link si comportano allo stesso modo, è evidente che lo scopo del threat actor è portare l'utente ad accedere al sito target.

---

La mia attività di ricerca ed i progetti che porto avanti sono auto-sostenuti. Se ti interessano gli argomenti che porto puoi supportarmi tramite il [**mio canale Patreon**](https://patreon.com/roccosicilia). Per restare aggiornato su articoli, video e live puoi iscriverti al blog:

---

Sugli elementi trovati va fatta una considerazione: come accennato in un recente [post su LinkedIn](https://www.linkedin.com/posts/roccosicilia_cybersecurity-trick-activity-7359601768768397314-gx6i?utm_source=share&utm_medium=member_desktop&rcm=ACoAAATK5U0By2qlNbOT_QThQp0s692DGhr_JfU), la URL storage.cloud.google.com è stata classificata come sospetta in alcuni feeds e da alcuni vendor. La community VirusTotal segnala diversi abusi di questo servizi a scopo phishing. Ovviamente nessuno si sognerebbe di bloccare questo dominio sui propri sistemi e questo ci ricorsa quanto sia fondamentale integrare/gestire le informazioni che arrivano dai feeds prima di utilizzarle.

Quindi, più che un **domain name - lato GCP - mi porterei a casa il bucket name come IoC**, mentre per quanto riguarda l'host a cui veniamo reindirizzati ha senso segnarselo e procedere con l'analisi.

## L'infrastruttura usata dal threat actor (una parte)

La pagina su cui si viene reindirizzati potrebbe sembrare un tracker:

```
https://www.loiete[.]com/2W1Q1KK/2Q8T7P4X/?sub1=7896681841dc4b7888ef48002fae53f1&source_id=20365&sub5=102054
```

I sistema di DNS sec. (OpenDNS di Cisco) che utilizzo lo blocca in quanto il dominio loiete.com è considerato malevolo. VirusTotal la pensa allo stesso modo: <https://www.virustotal.com/gui/domain/loiete.com>.

Non si tratta ancora della pagina di atterraggio e il threat actor sembra voler giocare con l'analista. Questo il contenuto della index del dominio in questione:

<img src="{{ '/assets/images-posts/image-5.png' | relative_url }}" alt="image 5" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Depistaggio?

È molto probabile che il dominio sia utilizzato dal threat actor per attività di phishing e scam. Dai dati prelevati da whois emerge un numero di telefono associato a diversi domini già analizzati per attività di scam, phishing e ransomware: +354.4212434). Anche in questo caso abbiamo un nuovo redirect verso un altro dominio:

```
https://dinusreal[.]store/?sub5=27822&source_id=20365&encoded_value=223GDT1&sub1=7896681841dc4b7888ef48002fae53f1&sub2=&sub3=&sub4=&sub5=27822&source_id=20365&domain=www.loiete[.]com&ip=XX.YY.129.188
```

Siamo arrivati alla "landing page" in cui viene proposto un finto sondaggio a cui partecipare per vincere il premio. Interessante notare che alla pagina vengono inviati i dati del dominio di provenienza e l'IP che del client che è stato reindirizzato.

<img src="{{ '/assets/images-posts/image-6.png' | relative_url }}" alt="image 6" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Landing Page

Anche questo nuovo dominio sarebbe da analizzare con calma e sulla nostra istanza MISP aggiungerò dei commenti. Tra le varie curiosità ho notato che uno degli script JS presenta **commenti al codice in italiano**, cosa spesso indicativa per definire la paternità dello script che sembra essere custom. Il dominio è categorizzato, in diversi feeds, come legato ad attività di shopping-phishing, elemento coerente con quanto analizzato sino ad ora.

Se si completa il sondaggio si viene reindirizzati alla pagina dove è possibile completare il pagamento di pochi euro per tramite carta di credito per ricevere l'omaggio. Questa pagina non è sempre la setta: oggi il dominio a cui si viene reindirizzati è malwaresafeapp[.]world per il quale ci sono poche informazioni online, ma ci sono elementi che potremmo considerare anomali come l'assenza di una home, una configurazione DNS "curiosa" e la quasi totale assenza di indicizzazione.

## Note sul processo

Considerando che i dati sono quelli relativi ad una singola email su sei ricevute nel mese di luglio, non sono pochi gli IoC da candidare ed analizzare. Diversi domain name che puntano a diversi host per i quali è opportuno fare verifiche puntuali a livello di paternità ed informazioni disponibili. L'attività di ricerca richiede un elenco di fonti da interrogare. C'è parecchia OSInt ed è richiesta una certa capacità di correlazione tra le informazioni che si raccolgono e ciò che si riesce ad intuire sul comportamento del truffatore di turno. È anche necessario avere un'idea delle tecniche che in questi contesti vengono utilizzate e saper analizzare gli host target in modo relativamente profondo ma restando in superficie... non è un penetration testing.

## Collecting

Ora che abbiamo un po' di dati bisogna portarli sulla piattaforma MISP in modo che abbiano senso. Come accennavo in un precedente post è necessario definire uno standard per inserire dati all'interno della piattaforma. Al momento prediligo l'utilizzo di "attributi" composti da diversi oggetti, ma in alcuni casi è necessario documentare il singolo oggetto.

<img src="{{ '/assets/images-posts/image-7.png' | relative_url }}" alt="image 7" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Event Graph (MISP)

Un elemento importante sono le relazioni tra gli attributi e gli oggetti documentati: se ci si limita ad inserire una serie di oggetti senza note e senza relazioni si perde completamente il "senso" di documentare un **evento**. Avere una lista di URL sospette è il risultato di un processo di analisi, all'interno della piattaforma MISP **è utile documentare il path su cui viene messa la vittima e gli artefatti** con cui entra in contatto.

Una singola email di phishing si porta dietro una bella scia di elementi che richiedono poi approfondimenti tecnici. È un lavoro lungo e complesso e possiamo farci affiancare da altri sistemi per velocizzare l'arricchimento delle informazioni, ma va necessariamente fatto se vogliamo disporre di informazioni utili alla comprensione della minaccia. La cura del dettaglio non è opzionale.
