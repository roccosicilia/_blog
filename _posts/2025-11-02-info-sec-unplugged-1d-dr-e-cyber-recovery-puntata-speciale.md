---
layout:     post
title:      "Info Sec Unplugged [1d] – DR e Cyber recovery (puntata speciale)"
date:       2025-11-02 09:00:00 +0100
categories: [update]
image:      /assets/images-posts/copertina_2026_2kpx.jpg
---

Ultima puntata di questa mini serie in cui abbiamo approfittato della saggezza di [Mattia Parise](https://www.linkedin.com/in/mattiaparise/) che si è unito a me ed [Andrea](https://www.linkedin.com/in/adainese/) per discutere in dettaglio di Cyber recovery. Non voglio fare spoiler visto che la puntata è in uscita - la troverete disponibile dal 03.11.2025 - quindi vi lascio qui il link al [sito del podcast](https://www.infosecunplugged.it) e mi limito ad una breve riflessione.

L'approfondimento su cui vorrei porre l'accendo, toccato anche durante la chiacchierata, è relativo al tema dei test. Se per l'ambito Disaster Revocery è spesso complesso organizzare un test realistico, ovvero che consenta di verificare veramente se quanto previsto dalla procedure funzionerà anche in caso di vero disastro, per il concetto di Cyber recovery - concetto che Mattia ci illustra molto bene nel podcast - probabilmente dobbiamo considerare ulteriori difficoltà.

Uno dei requisiti che spesso si fatica a rispettare è l'isolamento dell'ambiente di recovery. In un contesto di Disaster Recovery tradizionale prevedere dei livelli di ridondanza è spesso molto utile e sensato e talvolta questi livelli di ridondanza sono possibili grazie ad una forte integrazione tra i sistemi. Un tipico esempio è l'estensione dei servizi Active Directory in modo da avere una parte di infrastruttura di base già attiva in caso di fault dell'infrastruttura primaria.

Questo vantaggio in un contesto di Disaster Revocery diventa un pericolo in un contesto di Cyber Recovery in quanto l'AD potrebbe essere uno dei sistemi compromessi dal threat actor, cosa che inevitabilmente renderebbe anche il sito di recovery compromesso, invalidando lo sforzo. È un tema si cui ha sicuramente senso riflettere. Con questo non voglio dire che non abbia senso valutare strategie di DR che integrino concetti di Cyber Recovery, bisogna sempre fare i contri con il budget a disposizione, ma va considerato molto bene il concetto di isolamento che questo modello richiede per funzionare.