---
layout:     post
title:      "eg0n: primi commit"
date:       2024-12-07 09:00:00 +0100
categories: [cyber-security]
image:      /assets/images-posts/coding.png
---

Nell'ultima live ho introdotto il progetto eg0n (precedentemente chiamato BitIoC) di cui si era già discusso qualche mese fa. L'idea di base è avere uno strumento semplice da integrare che consenta di raccogliere e qualificare IoC con il contributo della community.

Non è mia intenzione replicare MISP che funziona egregiamente, l'idea parte da una esigenza personale di integrazione degli IoC e documentazione di artefatti ed appunti operativi che ho pensato di trasformare in un progetto contributivo.

In questa prima fase stiamo semplicemente costruendo lo scheletro dall'app d'appoggio per il progetto per la quale ho, infine, deciso di usare django: semplice, flessibile, supportato. Per restare sul pragmatico siamo partiti da uno specifico oggetto "tipo": gli IP address. Durante la live abbiamo discusso i "campi" iniziali per questo tipo di dato e fatto un po' di ragionamenti sui profili degli utenti che potranno contribuire.

<img src="{{ '/assets/images-posts/eg0n-v1.webp' | relative_url }}" alt="demo" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Prossimo step: consolidare la struttura dell'app IP_ADD e lavorare sui profili utente.

Il progetto eg0n è:

- sviluppato dalla community
- supervisionato dal sottoscritto
- autofinanziato con il mio progetto di divulgazione

Se sei interessato puoi sostenerlo:

- collaborando attivamente alla discussione su [Discord](https://discord.gg/Ys5AAbsyyH)
- collaborando attivamente allo [sviluppo](https://github.com/roccosicilia/eg0n)

> Se trovi interessanti i miei contenuti e vuoi supportare il mio progetto di divulgazione iscriviti alla mia [newsletter](https://roccosicilia.substack.com) sostienimi con una donazione.