---
layout:     post
title:      "Info Sec Unplugged [19] – Threat Int. (3a parte)"
date:       2025-09-08 08:00:00 +0200
categories: [cyber-security, ita, update, vlog-podcast]
image:      /assets/images-posts/podcast.png
---
Questa è una puntata un po' particolare: da questo episodio la versione audio su [**spreaker**](https://www.spreaker.com/podcast/info-sec-unplugged--6025156) sarà quella completa e disponibile online sulle piattaforme podcast mentre sul mio canale [YouTube](https://youtube.com/@roccosicilia) e sul blog pubblicherà un video/post di accompagnamento gli highlight e qualche approfondimento.

https://youtu.be/3LJb2OtQf28

Info Sec Unplugged [19]

La puntata è la terza parte di un argomento complesso: la Threat Intelligence. Ci siamo dati l'obiettivo di provare a spiegare come questo processo si "incastra" in una struttura operativa, a cosa serve e come si può utilizzare per migliorare la propria postura di sicurezza. Per chiudere questa serie di tre episodi abbiamo utilizzato un esempio pratico: l'analisi di una semplice scampagna di phishing per ripercorrere i passi che un analista può fare per raccogliere informazioni da un elemento semplice come una email.

## Approfondimenti

#### L'analisi di una email

Durante la puntata facciamo riferimento all'analisi dell'intestazione e del corpo di una email indicando che in questa parti del contenuto ci sono diverse informazioni utili che possiamo raccogliere.

Per fare un esempio che quasi tutti posso replicare facilmente potete selezionare una email dal vostro account Gmail e scegliere l'opzione *Show Original*. Dovrebbe aprirsi una nuova pagina sul vostro browser con la versione "estesa" del messaggio di posta elettronica dove, nella parte iniziale, troverete una serie di stringhe che probabilmente faticherete a decifrare.

<img src="{{ '/assets/images-posts/image-1.png' | relative_url }}" alt="image 1" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Header di un messaggio di spam nella mia mailbox Gmail

In questa parte del messaggio di posta ci sono informazioni preziose sull'origine dell'email che, anche se in parte contraffatte, possono essere annotate e documentate in quanto potrebbero costituire un elemento utile all'analisi.

Ad esempio, per il Threat Actor è sicuramente facile falsificare un indirizzo email mittente - *edu@cma7c.h8i.fouri.web.za* in questo caso - un po' più complesso falsificare il dominio o il sistema che ha fisicamente inviato l'email, rispettivamente *cma7c.h8i.fouri.web.za* e *157.180.69.114*. Questi dati possono essere un buon punto di partenza per avviare un'indagine.

#### Analisi dei link

Nel corpo del massaggio spesso ci sono link che portano a pagine web che, come nel caso dell'esempio fatto durante il podcast, servono a portare l'utente ad inserire i propri dati che vengono poi raccolti dagli autori della campagna di phishing/scam.

In questa campagna viene utilizzato un trucco per "pulire" il link presente nell'email inserendo un riferimento che punta ad una risorsa cloud storage di Google:

<img src="{{ '/assets/images-posts/image-2.png' | relative_url }}" alt="image 2" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Link ad una risorsa hosted da Google

Difficilmente i sistemi anti-spam ed in generale i sistemi di detection bloccano questo tipo di link. Nel caso specifico si può osservare come questo tipo di link sia ampiamente documentato su VirusTotal come infrastruttura abitualmente utilizzata per scam/phishing:

<img src="{{ '/assets/images-posts/image-3.png' | relative_url }}" alt="image 3" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

316 community report a cui vado ad aggiungere il mio

Più interessante, come in un altro caso analizzato, il contenuto della pagina a cui si punta:

```
<meta http-equiv="refresh" content="3; url=http://static.239.113.98.91.clients.your-server.de">

<script>
var fragment = window.location.href.split('#')[1] || ''; // fallback to empty string if no fragment
document.location.href = 'http://static.239.113.98.91.clients.your-server.de/' + fragment;
</script>
```

Un semplice redirect verso un'altra pagina che poi rimanda ad un altro sito (loiete[.]com) che infine ci porta sul sito di phishing (dinusreal[.]store).

#### Unire i puntini

Raccogliere i singoli elementi e documentarli nel dettagli porta ad ottenere una collezione di artefatti (ip, url, frammenti di JS, testi di email, sender, ecc) che presi singolarmente non hanno particolare significato, ma se organizzati in un unico evento che descrive una campagna di phishing acquistano molto significato.

Sono dati a cui un analista può accedere tramite ricerche mirate e che possono essere correlati con altri dati. Sono informazioni che possiamo far consumare ai sistemi di detection o che possiamo utilizzare per attivare policies più stringenti in base alle esigenze della nostra infrastruttura e degli utenti che la utilizzano.

Ovvio, prima devo avere uno strumento che mi consenta tutto questo (come MISP) ed un team o un partner che mi aiuti ad integrare questo tesoretto di informazioni nei miei sistemi di detection.

## Conclusioni

La Threat Int. è un tema molto complesso, il fatto di aver dedicato tre puntate sol per introdurlo penso sia un elemento che lo testimonia. È anche una disciplina estremamente utile che, a vali livelli, tutte le organizzazioni devono iniziare a considerare. È un tema che sicuramente riprenderemo nel podcast.

Vi ricorso, importantissimo, il link al **[podcast su Spreaker](https://www.spreaker.com/podcast/info-sec-unplugged--6025156)** e, come sempre, se gli argomenti che porto vi interessano e volere restare aggiornati su tutto quello che pubblico oltre al Podcast potete iscrivervi a questo Blog lasciando la vostra email o seguirmi sui miei canale diretti:

- YouTube: <https://youtube.com/@roccosicilia>
- Patreon: <https://patreon.com/roccosicilia>
- Reddit: <https://www.reddit.com/r/SheliakNotes/>
