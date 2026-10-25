---
layout:     post
title:      "Password policies e resistenza agli attacchi"
date:       2022-04-17 17:53:56 +0200
categories: [hacking, ita]
image:
---
Un post di riflessione in merito ai corretti (a mio parere) spunti che Paolo Perego propone in [questo sui articolo](https://codiceinsicuro.it/2022/04/16/non-mettete-regole-troppo-complesse-alle-vostre-password/). Non ripeto quello che ha scritto Paolo, leggetelo e valutate voi stessi, il suo post merita. Parto direttamente dalle sue conclusioni: dove sta la debolezza di una ***passphrase*** rispetto ad una password complessa?

Provo ad affrontare il tema dal punto di vista dell'attacker che ha ovviamente l'obiettivo di eseguire il cracking di un accesso ad un sistema o ad una applicazione. Nel post di Paolo si fa riferimento al contesto dei portali e siti web ma il tema della verifica della robustezza prescinde il contesto. Per procedere quindi con le specifiche prove utilizzo un piccolo lab composto dalla solita kali (per comodità) che farà sia da base offensiva che da target con un utente "test" per il quale ho configurato un semplice accesso SSH. Come password utilizzeremo quella proposta da Paolo: "Il colore della mia stanza è blu".

## Wordlist

Partiamo dalle basi dell'*attacco ad una credenziale*: il brute forcing utilizzando un elenco di parole predefinite. In questo caso i tipici dizionari presenti nei diversi tools (kali compresa) riportano tipicamente un elenco di parole, non di frasi. Una wordlist classica sarebbe quindi poco efficace verso una passphrase salvo la creazione di diverse combinazioni di *words* obiettivamente molto onerosa da costruire in termini di tempi di generazione e volumi di dati. Escluderei quindi questa tecnica tra quelle efficaci.

## Generazione di credenziali

E' probabilmente più funzionale tentare di generare una credenziale partendo da un dato che non ci è però dato sapere in anticipo, ovvero il fatto di essere di fronte ad una passphrase e non una password.

Se l'attacker partisse da questo assunto (cosa di per se non particolarmente realistica senza dati a supporto della tesi) potrebbe valutare l'utilizzo di varie combinazioni di parole comuni a formare una frase semplice da ricordare. Non mi stupirebbe scoprire che molti utenti, in questo scenario, potrebbero voler utilizzare delle citazioni famose o frasi che possano essere in qualche modo riferibili al sistema a cui si sta accedendo.

In tal senso un potenziale approccio potrebbe essere l'utilizzo di tools come ***cewl*** per creare una lista si parole partendo dal sito del target o da altri contenuti (es: racconti o testi comuni) per provare a costruire poi delle frasi.

<img src="{{ '/assets/images-posts/image-4.png' | relative_url }}" alt="image 4" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Plausibile ma sicuramente non comodo e credo, anche in questo caso, poco efficace.

Un altro approccio, visto che le passphrase di base sono stringhe relativamente lunghe, è il brute force più tradizionale con calcolo delle varie combinazioni. Mettiamoci in un caso relativamente comodo dove la frase è tipicamente composta da caratteri alfabetici con degli spazi come separatori. Assumiamo anche di conoscere la lunghezza della passphrase del target, un metodo realistico in alcuni scenari di attacco è contare ad orecchio le digitazioni dell'utente. Nell'esempio di Paolo ci troviamo comunque davanti ad un frase di 32 caratteri.

Cosa succedere se proviamo a generare frasi di 32 caratteri alfabetici con ***crunch***?

<img src="{{ '/assets/images-posts/image-5.png' | relative_url }}" alt="image 5" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Non impossibile ma decisamente improbabile.

## Crack degli hash

Qualche giorno fa ho parlato di credential stuffing. Supponiamo quindi che a causa di un Data Breach gli hash delle passphrase siano disponibili all'attacker. Ai nostalgici verrà subito in mente di utilizzare tools come John the Ripper ma di base le difficoltà saranno le stesse descritte nei precedenti due casi in quanto le tipiche modalità di utilizzo di questi tools prevedono l'impiego di wordlist o utilizzano funzioni di generazione di stringhe.

## Le mie conclusioni

Ho voluto scrivere questo post per non rischiare di generare una "battaglia di opinioni". [Paolo](https://codiceinsicuro.it/) ha proposto una riflessione corretta che ho voluto mettere alla prova con qualche esempio reale e ritengo che non vi siano motivazioni che rendano una passphrase meno sicura di una "strong password"... anzi in un certo senso la lunghezza gioca un ruolo a favore non banale.
