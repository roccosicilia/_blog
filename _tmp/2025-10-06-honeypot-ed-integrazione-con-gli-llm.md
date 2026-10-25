---
layout:     post
title:      "Honeypot ed integrazione con gli LLM"
date:       2025-10-06 12:00:00 +0200
categories: [cyber-security, hacking, ita]
image:      /assets/images-posts/screenshot-2025-10-06-at-16.36.13.png
---
### Premessa

Prima di affrontare il tema devo fare una premessa. Non penso che gli LLM siano strumenti miracolosi che cambieranno la storia dell'umanità, penso siano strumenti che possono dare una mano se usati in modo strutturato da persone ben consapevoli del loro funzionamento (probabilmente non moltissime). Detto questo posso procedere con il post.

### Come funzionerebbe

All'interno del progetto [**eg0n**](https://github.com/b1th0rn/eg0n) abbiamo integrato una componente honeypot utile per *rastrellare* informazioni da analizzare e trasformare in IoC qualificati. Il funzionamento che avevo pensato per gli honeypot è abbastanza semplice: simulo un servizio e gestisco una serie di richieste al fine di dare l'impressione al bot o al threat actor che il servizio sia effettivamente attivo così da invogliarlo ad interagire. Ciò che viene fatto dal software è ovviamente registrare tutte le interazioni in un LOG che da qualche settimana è analizzabile dall'interfaccia di eg0n.

https://www.youtube.com/watch?v=LqWY_xvJypw

Integrazione della componente honeypot

Discutendone con più persone è emersa l'idea, già utilizzata in modo strutturato da progetti come [Beelzebub](https://beelzebub.ai/), di utilizzare un LLM per generare risposte per il threat actor. La meccanica potrebbe essere qualcosa tipo:

- il finto servizio (es: telnet) riceve una richiesta di login
- la trappola elabora la richiesta di login rispondendo (sulla base di alcune condizioni) alla richiesta con una shell
- il threat actor, vedendo una shell utilizzabile, prova ad eseguire dei comandi
- i comandi vengono inseriti in un prompt per un LLM che genera una risposta verosimile al comando dato, il servizio inviare la risposta alla sessione del threat actor
- il threat actor riceve una risposta coerente e continua con la sua "post exploitation"

Tutti i passaggi verrebbero registrati sul database di eg0n, compresi gli eventuali payload che il threat actor tenterà di utilizzare. A noi interessano proprio questi elementi.

L'utilizzo del LLM è limitato alla generazione di finte risposte da inviare al threat actor sfruttando la capacità statistica di riprodurre qualcosa di coerente con la "domanda". Eventuali errori, normali per un sistema che riproduce testo sulla base di una coerenza statistica e non sulla base di una comprensione del contesto, non compromettono il funzionamento del sistema in se, alla peggio il threat actor potrebbe insospettirsi dall'incoerenza della risposta e smettere di interagire con il sistema.

### Prossimo step

Ieri sera, durante una live di puro coding che [trovate su YouTube](https://www.youtube.com/watch?v=bcskYxcFG6o), ho implementato la componente di servizio telnet che è quasi funzionante (ci sono ancora un paio di errori che vorrei sistemare).

Il prossimo step è quindi quello di creare una funzione per gestire il dialogo con il LLM, fare qualche test funzionale e poi inserire la funzione nel comportamento del servizio che al momento si limita a non dare risposta ad eventuali comandi (nel video della live si vede abbastanza bene il comportamento di base).

Ho pensato di iniziare con telnet per sperimentare e misurare la funzionalità, se da risultati interessanti si può ragionare anche su altri servizi.
