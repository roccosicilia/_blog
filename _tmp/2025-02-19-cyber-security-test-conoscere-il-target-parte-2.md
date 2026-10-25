---
layout:     post
title:      "Cyber Security Test: conoscere il target (parte 2)"
date:       2025-02-19 21:00:00 +0100
categories: [cyber-security, hacking, ita]
image:      /assets/images-posts/cybersecurity-test-serie.png
---
Nel precedente post abbiamo discusso le basi della fase di ricognizione e raccolta informazioni, in questa seconda parte ho pensato di discutere ed approfondire le attività operative e l'analisi dei dati raccolti.

Ci siamo dati degli obiettivi specifici: raccogliere un elenco di IP/url riconducibili al target ed analizzare le tecnologie rilevate, individuare nominativi e relative informazioni, files e documenti che ci consentano di farci un'idea della struttura organizzativa. Andiamo con ordine.

---

Se gli argomenti che pubblico sul blog e sui miei canali ti interessano e vuoi sostenere il progetto puoi diventare un supporter tramite la mia [pagina Patreon](https://patreon.com/roccosicilia) dove troverai anche molti approfondimenti come i video dedicati a questa serie di post.

---

# Individuare gli endpoint

Per la funzione che svolge abbiamo già citato il servizio DNS che, se correttamente interrogato, può dare molte informazioni.

<img src="{{ '/assets/images-posts/image-7.png' | relative_url }}" alt="image 7" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

DNSdumpster

I record che possiamo quasi in tutti gli scenari chiedere ed analizzare sono gli A record che associano uno nome dominio ad un IP, gli MX record usati dai servizi di posta e i TXT record che possono contenere diverse informazioni tra cui il Sender Policy Framework (SPF), anche questo riferito al servizio di posta elettronica. Nel precedente post ([e video](https://www.patreon.com/posts/cyber-security-1-118474393)) ho dedicato uno spazio con qualche riflessione tecnica sulla configurazioni dei record MX, in questa occasione ci interessa solo raccogliere ed analizzare gli eventuali IP individuati.

<img src="{{ '/assets/images-posts/image-8.png' | relative_url }}" alt="image 8" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Continuiamo a farci aiutare da Maltego per annotare i dati: tutte le richieste DNS citate possiamo eseguirle tramite una *trasformazione*. Nell'esempio preso in esame nella prima parte, ed in particolare nella dimostrazione video, avevamo utilizzato la *trasformazione* "To IP Address" per ottenere gli indirizzi IP associati agli host.

L'indirizzo IP potrebbe far parte di un subnet che fa riferimento esplicitamente al nostro target: i provider dovrebbero assegnare e documentare le subnet sul databese di riferimento per la region. Disporre degli indirizzi IP dei vari servizi ci consente di ricostruire il perimetro del nostro target.

---

### Focus su "come funziona internet"

Scopo di questi post è soprattutto **addentrarci un po' nel funzionamento dei sistemi e delle reti** e sul motivo che ci porta ad eseguire certe operazioni. Provo quindi ad approfondire un aspetto tecnico legato al funzionamento delle reti pubbliche, elemento di base per **comprendere** i prossimi ragionamenti. Quindi, come funziona Internet?

<img src="{{ '/assets/images-posts/image-11.png' | relative_url }}" alt="image 11" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

ISP: Schema di super sintesi

Premetto che nella video spiegazione sarò più chiaro ed in questa occasione mi concederete delle super semplificazioni. Di base internet è formato da una serie di reti interconnesse tra loro. Le reti dei provider sono interconnesse grazie ai rispettivi Border Gateway e possono dialogare direttamente o tramite delle apposite infrastrutture (dei Datacenter) definiti Internet Exchange. L'unione e la comunicazione di queste reti rappresenta l'infrastruttura logica (la parte fisica la saltiamo in questa occasione) di internet.

I provider erogano servizi specifici: ci sono provider e strutture Datacenter che erogano servizi di connettività per le aziende, altri che erogano servizi agli utenti domestici, altri che si occupano esclusivamente dell'ospitalità di infrastrutture IT, server e sistemi di altre aziende.

Così **il mio blog** è gestito da un'azienda che ha i suoi server presso il Datacenter di un **Cloud Provider** la cui connettività è erogata da un **Internet Service Provider** che utilizza una ipotetica rete A.0.0.0/8 di cui una sottorete viene assegnata al **Cloud Provider**. Così l'host su cui gira il mio blog avrà un IP della citata rete che fa parte delle reti in gestione all'**Internet Service Provider**.

Per poter gestire **il mio blog** devo accedere ad internet e lo faccio tramite un altro **Internet Service Provider** che mi eroga un servizio di connettività non diverso dal servizio offerto ad un'azienda o ad un cloud provider ma è molto diverso per quanto riguarda i parametri di servizio ed alcuni elementi tecnici. Anche il mio **Internet Service Provider** mi assegna una sottorete pubblica che solitamente varia ad ogni nuova connessione del router domestico (si semplifica questo concetto con l'espressione *IP dinamico*).

Il mio **Internet Service Provider** dialoga con molti altri provider, tra i quali c'è, direttamente o indirettamente, anche il **Cloud Provider** del **mio blog**. Quindi, quando sul mio browser digito la URL del mio blog la richiesta HTTP passa dal mio router locale, transita per la rete del mio **ISP**, raggiunge la rete del ****Cloud Provider A**** per poi arrivare nella rete del Cloud Provider ed infine al **server del mio blog**.

Qui la video spiegazione di quanto scritto:

https://www.youtube.com/watch?v=v0ekk3wumAQ&t=406s

Come funziona (più o meno) internet?

---

Solitamente i servizi di connettività per le aziende vengono rilasciati assieme ad una o più subnet su cui il cliente pubblica i servizi che desidera siano raggiungibili dall'esterno. Ad esempio se l'azienda utilizza un sistema proprio per la gestione della posta elettronica, a questo verrà assegnato un indirizzo IP pubblico (semplifico) al quale verrà associato un MX record per consentire la ricezione della posta elettronica.

Ne consegue che individuare alcuni host tramite le già citate DNS query potrebbe consentire di individuare l'intera subnet utilizzata dal target e questa subnet potrebbe essere (rif. allo schema ISP) una sede o un sito Datacenter. Stiamo di fatto mappando il perimetro del target e per individuare gli host attivi senza passare ad azioni dirette possiamo usare due utilissimi tools come [Shodan](https://www.shodan.io/dashboard) e [Censys](https://search.censys.io/).

<img src="{{ '/assets/images-posts/image-1.png' | relative_url }}" alt="image 1" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Shodan

Per individuare l'esatta subnet è possibile verificare sul database dell'ente che regolamenta l'assegnazione delle classi nella region, per l'europa è il [RIPE](https://ripe.net).

<img src="{{ '/assets/images-posts/image-2.png' | relative_url }}" alt="image 2" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Esempio di record

Per ovvie ragioni ho coperto i riferimenti, ma fare la prova vi richiederà pochi secondi: è sufficiente cercare un IP pubblico per ottenere la subnet di appartenenza, il riferimento dell'ISP e se le cose sono state fatte bene anche il riferimento del cliente finale, ovvero dell'utilizzatore. Non è raro che i provider, soprattutto i piccoli ISP, non mantengano aggiornate le assegnazioni delle classi, questo dato va quindi preso un po' con le pinze.

Una volta che abbiamo individuato le subnet del target i citati Shodan e Censys ci aiuteranno a fare un po' di enumeration degli host del target. Già in queste fasi non è raro individuare, grazie alla profondità di scansione dei citati tools, sistemi operativi con tanto di dettagli sulle applicazioni in uso, versioni ed informazioni su eventuali vulnerabilità - tutte da accertare - esposte in rete.

### Analisi della zona DNS

Ne avevo parlato nella prima parte ma vale la pena tornarci per citare due utili tools (non sono gli unici) che possono portare ulteriori spunti alla ricerca: dnsrecon e dnsenum. Lo scopo del post non è proporre un tutoria sull'uso dei tools (ampiamente documentati in rete), si cito a titolo di esempio in quanto presentano funzioni interessanti coma la possibilità di eseguire una ricerca di record CNAME tramite brute forcing.

<img src="{{ '/assets/images-posts/image-3.png' | relative_url }}" alt="image 3" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Esempio di output di DNSENUM

Va considerato che l'analisi della zona DNS potrebbe farci incappare in endpoint fuori dallo scope del target: non è raro che un record DNS punti ad un servizio terze parti. Una buona pratica, in caso di dubbi, è sottoporre al committente quanto rilevato dalle indagini prima di procedere con azioni di test effettivo.

# Nominativi e documenti

Di base internet ci mette a disposizione una quantità enorme di informazioni ed i limiti sono solo quelli dalla nostra fantasia ed esperienza.

Praticamente tutte le aziende con un minimo di struttura interna hanno una pagina social (es: LinkedIn) che può essere utilizzata per raccogliere dati su dipendenti, ruoli, competenze. In molti casi si riesce a ricostruire buona parte dell'organigramma grazie alle informazioni che si possono trovare sui siti istituzionali del target, sulle pagine social dell'azienda e tramite la ricerca di articoli e pubblicazioni (anche non digitali) sul target.

Anche la ricerca di documenti specifici può venire in aiuto: premesso che trovare ed analizzare documenti DOC, PDF, ecc è a prescindere utile per espandere il nostro livello di conoscenza del target, questi file presentano informazioni utili anche a livello dei metadati. Ad esempio nei metadati dei file PDF sono spesso specificate informazioni come il programma usato per la creazione del documento ed il nominativo dell'autore.

Ovviamente il contenuto può essere altrettanto utile in quanto non è raro trovare riferimenti a fatti che possono in qualche modo essere sfruttati in un contesto di social engineering, si trovano spesso riferimenti ad altre figure aziendali, fornitori, partner clienti. La quantità di informazioni è enorme e tutto è potenzialmente rilevante.

# Conclusione

I più accorti si saranno resi conto di quanto questa fase assomiglio ad una operazione di intelligence e non è un caso. Una profonda conoscenza del target consente di define i modelli di attacco più efficaci ed è esattamente di queste informazioni che le aziende hanno bisogno per predisporre le adeguate contromisure.
