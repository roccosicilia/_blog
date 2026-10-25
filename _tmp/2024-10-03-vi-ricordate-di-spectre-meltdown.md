---
layout:     post
title:      "Vi ricordate di Spectre/MeltDown?"
date:       2024-10-03 14:00:00 +0200
categories: [cyber-security, ita]
image:      /assets/images-posts/spectre.png
---
Un argomento a dir poco glorioso per chi si ricorda di quei giorni nel 2018 (è passata una vita). Fa un po' sorridere parlarne a ottobre 2024, ma evidentemente la ferita è ancora aperta.

Perché ne parlo? Ciclicamente questa vulnerabilità mi si presenta d'avanti e la domanda che gli interessati mi fanno è sempre la stessa: **avendo aggiornato gli hypervisor** (ormai è raro trovare server con O.S. Microsoft installato BareMetal) **devo preoccuparmi di eseguire il fix anche sulle Virtual Machine?** Risposta breve: **sì**. Due cenni sul perché e come.

## Perché?

Per chi è del settore invito alla lettura dei relativi paper che potete trovare qui: <https://meltdownattack.com/>. In questa occasione mi permetterete di iper-semplificare il tema per renderlo digeribile anche a chi non ha nozioni di architettura dei moderni processori. Il punto a cui prestare attenzione è che la vulnerabilità, oltre ad avere diverse varianti, si applica a diversi scenari, tra i quali esiste lo scenario che vede come target una Virtual Machine non fixed.

Microsoft ci regala questo documento in cui sono riassunti gli scenari relativi alla variante 4 (CVE-2018-3639): <https://msrc.microsoft.com/blog/2018/05/analysis-and-mitigation-of-speculative-store-bypass-cve-2018-3639/>. Per quanti mi riguarda è stato il documento che più mi ha aiutato a capire se, nei diversi contesti in cui ho lavorato, era opportuno procedere con l'applicazione delle fix/mitigation o meno.

## Come?

Qui viene il bello perché la mitigation é applicabile semplicemente creando due chiavi di registro il cui valore varia a seconda di diversi parametri tra cui l'architettura CPU e la variante su cui vogliamo operare. Come accennavo la variante che probabilmente molti si trovano a dover - ancora - gestire è la v4 la cui mitigation è spiegata nell'ultimo link.

Per i super pigri lascio il link ad uno script che vi consente di eseguire la mitigation se le chiavi non sono ancora presenti sul sistema target. Da considerare che è necessario il reboot della macchina una volta applicata la fix: <https://github.com/roccosicilia/VulnerabilityReview/blob/main/CVE-2018-3639/review.md>

<img src="{{ '/assets/images-posts/cve-2018-3639-screenshot-01.png' | relative_url }}" alt="cve 2018 3639 screenshot 01" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

__________

Se ti interessano i miei articoli ad i miei video di approfondimento puoi sostenere il progetto tramite la community [patreon](https://patreon.com/roccosicilia). Per ricevere gli update puoi registrarti al blog:

__________

## Minacce correlate

Una nota importante che dovrebbe contribuire a far comprendere la pericolosità di questa vulnerabilità: sono documentati diversi PoC della vulnerabilità discussa, non ci sono ragioni valide per non eseguire il fix.
