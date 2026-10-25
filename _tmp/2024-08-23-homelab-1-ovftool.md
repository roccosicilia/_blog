---
layout:     post
title:      "HomeLab #1: ovftool"
date:       2024-08-23 15:00:00 +0200
categories: [hacking, ita, study-with-me]
image:      /assets/images-posts/homelab.png
---
Dedico una serie di post al mio HomeLab ed alle varie evoluzioni/modifiche che eseguo nel tempo. In questa serie non ci saranno riferimenti a specifiche attività in ambito cyber sec. ma mi limito a descrivere le scelte fatte a livello di lavoratorio e, ovviamente, a spiegarne le motivazioni.

Di base posso contate sul mio MacBook dove ho installato un paio di VM di servizio (una Linux e una Windows) e su cui installo buona parte dei tools che mi servono. L'ovvio limite dei moderni MacBook è il processore: in caso di esigenze x86 devo utilizzare altre piattaforme. Per questo mi sono dotato di un MiniPC (al momento molto limitato) per ambienti guest x86. Per varie ragioni al momento il MiniPC è una WinBox (mi serviva un Windows bare metal) con installato VirtualBox. Una piccola utility di cui dotarsi è, proprio per le esigenze di gestione delle guest, ovftool grazie alla quale è possibile creare archivi *ova* (open virtual appliance).

Oggi ho rimesso le mani su alcune macchine di VulnHub e buona parte di queste macchine sono rilasciate nel formato VMware, quindi con un *vmx* file che descrive la VM ed il disco nel formato *vmdk*. Convertendo la macchina in un archivio *ova* possiamo facilmente importarla in ambienti VMware e VirtualBox senza mettersi a copiare file su Datastore remoti o fare altri "accricchi"

> [Nota] Dispongo anche di un attrezzatissimo LAB messo a disposizione dalla mia company (vedi mio [profilo LinkedIn](https://www.linkedin.com/in/roccosicilia/)) con VMware vSphere e altri strumenti, utilissimo per le attività di testing e studio. Disporre di attrezzature di laboratorio adeguate è un supporto indispensabile alla crescita delle proprie abilità tecniche.

Il tool da utilizzare per questo piccolo task è ovftool che nella sua semplicità ci consente di creare il nostro *ovf/ova* file partendo appunto dal *vmx* e dal *vmdk*.

Nel contesto specifico - macchine create per far pratica di Penetration Testing - considerate che chi crea queste Virtual Machine non sempre si preoccupa di eseguire un'esportazione della macchina con condifurazioni di vHardware generiche, potrebbe capitare che la VM, una volta importata, presenti vDevice che non avete sul vostro host e questo potrebbe impedire il boot del sistema. In questo caso è sufficiente modificare la configurazione della VM a livello di vDevice.

---

In questi giorni sto pubblicando un po' di video con delle "study session" che ho fatto in live, le rendo disponibili pubblicamente su [Patreon](https://patreon.com/roccosicilia), **basta il free access**.
