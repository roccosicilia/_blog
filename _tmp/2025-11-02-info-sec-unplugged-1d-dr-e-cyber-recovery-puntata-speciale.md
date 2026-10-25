---
layout:     post
title:      "Info Sec Unplugged [1d] – DR e Cyber recovery (puntata speciale)"
date:       2025-11-02 12:00:00 +0100
categories: [cyber-security, ita, update, vlog-podcast]
image:
---
Ultima puntata di questa mini serie in cui abbiamo approfittato della saggezza di [Mattia Parise](https://www.linkedin.com/in/mattiaparise/) che si è unito a me ed [Andrea](https://www.linkedin.com/in/adainese/) per discutere in dettaglio di Cyber recovery. Non voglio fare spoiler visto che la puntata è in uscita - la troverete disponibile dal 03.11.2025 - quindi vi lascio qui il link al sito del podcast e mi limito ad una breve riflessione:

[<img src="{{ '/assets/images-posts/screenshot-2025-11-02-at-12.24.05.png' | relative_url }}" alt="screenshot 2025 11 02 at 12.24.05" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />](https://www.infosecunplugged.it)

Homepage del progetto podcast.

L'approfondimento su cui vorrei porre l'accendo, toccato anche durante la chiacchierata, è relativo al tema dei test. Se per l'ambito Disaster Revocery è spesso complesso organizzare un test realistico, ovvero che consenta di verificare veramente se quanto previsto dalla procedure funzionerà anche in caso di vero disastro, per il concetto di Cyber recovery - concetto che Mattia ci illustra molto bene nel podcast - probabilmente dobbiamo considerare ulteriori difficoltà.

Uno dei requisiti che spesso si fatica a rispettare è l'isolamento dell'ambiente di recovery. In un contesto di Disaster Recovery tradizionale prevedere dei livelli di ridondanza è spesso molto utile e sensato e talvolta questi livelli di ridondanza sono possibili grazie ad una forte integrazione tra i sistemi. Un tipico esempio è l'estensione dei servizi Active Directory in modo da avere una parte di infrastruttura di base già attiva in caso di fault dell'infrastruttura primaria.

Questo vantaggio in un contesto di Disaster Revocery diventa un pericolo in un contesto di Cyber Recovery in quanto l'AD potrebbe essere uno dei sistemi compromessi dal threat actor, cosa che inevitabilmente renderebbe anche il sito di recovery compromesso, invalidando lo sforzo. È un tema si cui ha sicuramente senso riflettere. Con questo non voglio dire che non abbia senso valutare strategie di DR che integrino concetti di Cyber Recovery, bisogna sempre fare i contri con il budget a disposizione, ma va considerato molto bene il concetto di isolamento che questo modello richiede per funzionare.
