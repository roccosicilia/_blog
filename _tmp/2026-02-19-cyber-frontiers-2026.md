---
layout:     post
title:      "Cyber Frontiers 2026"
date:       2026-02-19 15:00:00 +0100
categories: [cyber-security, ita, update, vlog-podcast]
image:      /assets/images-posts/cyberfrontiers-convention.jpeg
---
Prima qualche dato tecnico: "*CyberFrontiers nasce dall’idea di professionisti appassionati di sicurezza informatica e tecnologia, con l’obiettivo di creare un  
ponte tra il mondo tecnico e quello aziendale. Unisce esperti, community e imprese in un unico ecosistema, favorendo networking, condivisione e crescita.*" Così recita l'[about della pagina LinkedIn](https://www.linkedin.com/company/cyberfrontiers-convention/about/) che ho voluto riportare integralmente.

**Partecipare ad eventi e conferenze, non so quante volte l'ho detto, è sempre stato uno stimolo positivo**: da spettatore trovi contenuti interessanti e persone con cui confrontarsi, da speaker si aggiunge l'onere della preparazione di un contenuto che dovrebbe portare qualcosa di utile (non necessariamente nuovo o originale, ma utile si).

Bisogna dire che salire sullo stesso palco di figure come [Andrea Menin](https://www.linkedin.com/posts/cyberfrontiers-convention_cyberfrontiers2026-cybersecurity-infosec-activity-7422923249157763072-GRjr) e [Omar Morando](https://www.linkedin.com/posts/cyberfrontiers-convention_cyberfrontiers2026-cybersecurity-otsecurity-activity-7424046614480252928-vLxO) è di per se già un onore. Cito loro tra i vari speaker solo perché ho avuto modo di conoscerli un qualche occasione, seguo da tempo il loro lavoro e considero entrambi figure molto preparate e capaci di trasmettere informazioni di valore... e non è poco! Sono certo che anche gli altri interventi saranno di valore.

Link al sito dell'evento: <https://www.cyberfrontiers.it/>

#### Di cosa parlerò

Nelle occasioni in cui ho modo di scegliere l'argomento, come in questo caso, cerco di restare sul tecnico e gli organizzatori mi hanno dato il loro "go". Vorrei parlare, seppur brevemente considerando che gli interventi devono giustamente avere un limite di tempo, di Detection GAP sul piano operativo.

Nelle mie attività di security test i GAP nella capacità di detection di strumenti e team sono qualcosa da ricercare, indagare e sfruttare per far emergere effettivi "punti ciechi" da gestire nel processo di Detection and Respond. Per chi difende si tratta di aree grigie che emergono solitamente assieme ad un problema.

La mia personale esperienza mi ha portato a concludere che il miglior modo per affrontare il tema è cooperare in modo strutturato tra team: il Red Team devono implementare test che abbiano come obiettivo la "misurazione" della sensibilità degli strumenti e dei processi di Detection ed i Blue Team devo poter replicare i test per analizzare l'effettivo comportamento dei sistemi e verificare eventuali lacune a livello di struttura o di processi.

Obiettivi nobili che bisogna anche scaricare a terra mettendo assieme le giuste teste e le giuste motivazioni. Per lavorare al miglioramento della Detection assieme ed in modo virtuoso è necessario lasciarsi alle spalle pregiudizi, ego, prese di posizione, ecc. È un processo di miglioramento e tutte le parti in causa devono allinearsi all'obiettivo. Il Red Team deve portare dati oggettivi ed il Blue Team deve portare evidenze oggettive. Su queste basi di ragiona assieme sugli eventuali punti di miglioramento, budget permettendo.

Visto che non voglio fare una sessione accademica ho deciso di portare esempi reali di test relativi ad effettive lacune che sono poi state discusse e migliorare grazie alla collaborazione tra team. La sessione prenderà in esame gli aspetti tecnici delle evidenze discusse ed i ragionamento fatti.

#### Materiale tecnico

Per ovvie ragioni non potrò mostrare le reali evidenze, sono stato autorizzato ad utilizzare gli esempi ma non i dati reali. Ho quindi deciso di riprodurre alcuni elementi in laboratorio al fine di mostrare qualcosa di tangibile e riproducibile. Pur considerando che ogni infrastruttura è un mondo a se e che i ragionamenti fatti in un certo contesto raramente hanno validità generale, ho pensato che ragionare con d'avanti il threat e la telemetria possa essere più interessante rispetto ad interpretare metriche e statistiche.

Ho cominciato in questi giorni (sere in realtà) a preparare il materiale ed essendo interamente basato sul mio [HomeLab](https://youtu.be/eyPFMt5YwrE) aspettatevi anche qualche approfondimento tecnico su queste pagine.
