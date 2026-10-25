---
layout:     post
title:      "Info Sec Unplugged [1a] – DR e Cyber recovery (parte 1)"
date:       2025-09-22 07:15:00 +0200
categories: [cyber-security, ita, vlog-podcast]
image:      /assets/images-posts/podcast.png
---
Iniziamo a discutere un tema che sul piano pratico è estremamente importante. Monte aziende hanno implementato un piano di Disaster Recovery - più o meno bene - e in quasi la totalità dei casi che ho analizzato lo stesso piano è stato adeguata per gestire l'evento "attacco cyber". Nella realtà dei fatti gli adeguamenti che ho visto sono spesso insufficienti se non errati.

https://youtu.be/1gieddeZxWw

In caso di attacco ci sono diverse domande a cui dovremmo rispondere prima di utilizzare il piano di DR:

- sono in grado di comprendere se la compromissione ha interessato anche il sito secondario?
- sono in grado di stabilire se i recovery point di cui dispongo sono "puliti"?
- sono in grado di stabilire se le operazioni da parte del threat actor sono state effettivamente bloccate?

Rispetto al "vecchio" piano di DR ci sono nuovi elementi che dobbiamo necessariamente considerare e quindi nuove predisposizioni da implementare.

In questa puntata del podcast discutiamo quelle che sono i principali errori osservati nell'utilizzo del piano di DR come strumento di recovery per lo scenario degli attacchi cyber e lo facciamo tenendo a mente uno schema logico di base, quello probabilmente più utilizzato, in cui abbiamo due siti Datacenter interconnessi a livello rete ed a livello storage.

La puntata del podcast è disponibile integralmente qui: <https://www.spreaker.com/episode/0x1a-dr-e-cyber-recovery-parte-1--67835796>

Allego uno schema tecnico di base utile alla discussione:

<img src="{{ '/assets/images-posts/screenshot-2025-09-22-at-09.23.11.png' | relative_url }}" alt="screenshot 2025 09 22 at 09.23.11" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

---

Se i contenuti che propongo tramite questo [blog](https://roccosicilia.com), il [podcast](https://infosecunplugged.github.io/), il mio canale [YouTube](https://youtube.com/@roccosicilia) e la piattaforma [Patreon](https://patreon.com/roccosicilia) ti sono utili si suggerisco di iscriverti (gratuitamente) ai miei canali per rimanere sempre aggiornato.

Il mio progetto di divulgazione è completamente auto-finanziato e puoi aiutarmi a migliorarlo sostenendomi tramite Patreon. Ai sostenitori, dedico del tempo extra con contenuti speciali e canali diretti.

[<img src="{{ '/assets/images-posts/image-14.png' | relative_url }}" alt="image 14" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />](https://patreon.com/roccosicilia)
