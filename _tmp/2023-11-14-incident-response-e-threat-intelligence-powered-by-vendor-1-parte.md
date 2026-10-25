---
layout:     post
title:      "\"Incident Response\" e \"Threat Intelligence\" powered by $vendor [1^ parte]"
date:       2023-11-14 00:15:00 +0100
categories: [cyber-security, ita]
image:
---
## Intro e premesse

In piu' occasioni ho avuto modo di discutere una tipologia di servizi che da qualche anno fa parte del portafoglio prodotti di diversi vendor di soluzioni e tecnologia. Ricordo di aver notato da subito i vendor di soluzioni EDR proporre servizi di Incident Response e Threat Hunting, ma in poco tempo molti altri vendor, che per diverse ragioni disponevano di competenze e dati sul complesso mondo delle minacce cyber, hanno messo a frutto l'immenso capitale di informazioni e dati che erano in grado di elaborare e ne sono nati dei servizi oggi a disposizione dei provider (che ne fanno giustamente uso per migliorare la propria efficacia) e dei clienti finali che hanno sicuramente l'esigenza di organizzarsi a livello di prevenzione e governo degli incidenti cyber.

Mi permetto un parere personale sulla situazione attuale, parere che sono ben felice di discutere e rielaborare: mentre per i provider di servizi cyber mi sembra relativamente ovvio dover scegliere tra il costruire un servizio di IR completamente interno o valutare una collaborazione con team esterni, per un cliente finale la situazione e' un po' diversa.

Provo a spiegarmi. Un'organizzazione strutturata ha sicuramente bisogno di definire un piano di IR ed ha molto probabilmente bisogno di un supporto a livello di Threat Intelligence (TI) per prevenire alcune situazioni spiacevoli. Come ho scritto anche in alcuni post su [LinkedIn](https://www.linkedin.com/in/roccosicilia/), le organizzazioni mature e strutturate sono sul pezzo e solitamente evitano di costruire internamente questo tipo di servizio, e' molto piu' frequente rivolgersi ad un provider che eroga il servizio specifico, talvolta lo stesso provider che gia' opera a livello di detection (vedi SOC ed evoluzioni verso EDR/XDR). Come detto, da qualche anno le organizzazioni hanno la possibilita' di rivolgersi direttamente ad un vendor (che di fatto funge da provider) per alcuni di questi servizi, separando cosi' a livello di interlocutore la funzione di "Detection and Response" - nel caso di un servizio EDR - dalla funzione di "Incident Response". C'e' anche da dire che sono gli stessi provider di servizi ad appoggiarsi, per competenza, ai servizi ed alle tecnologie che i vendor hanno portato sul mercato.

<img src="{{ '/assets/images-posts/image.png' | relative_url }}" alt="image" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Rappresentazione confusa della confusione.

Questa premessa per dire che io non ho la soluzione in tasca, ho quindi pensato di esplorare le proposte di tre big player lato vendor per cercare di comprendere meglio come si stanno ponendo sul mercato ed in questa serie di tre post vi riporto i dati che ho raccolto e le mie note. I vendor che ho selezionato sono [Cisco](https://www.cisco.com), [Palo Alto](https://www.paloaltonetworks.com/) e [Mandiant](https://www.mandiant.com/); avendo interesse a comprende il funzionamento di questa tipologia di servizi la mia ricerca prendera' in esame solo i dati tecnici e di contesto. Non e' una comparazione.

## Talos (Cisco)

Per il primo post ho scelto il vendor che conosco da piu' anni e di cui avevo seguito la "nascita" tra il 2013 ed il 2014 a seguito dell'acquisizione di Sourcefire da parte di Cisco. Come molti addetti ai lavori all'epoca seguivo con un certo interesse le soluzioni IDS come Snort il cui creatore, Martin Roesch, era anche il founder di Sourcefire. [Talos](https://www.talosintelligence.com/) nasceva quindi come l'unione di diversi team: Sourcefire Vulnerability Research Team (Sourcefire VRT), Cisco Threat Research, Analysis, and Communications (TRAC) team e Security Applications (SecApps).

Dalla documentazione pubblica a disposizione si percepisce che alla base esiste una struttura in grado di raccogliere ed elaborare una enorme quantita' di informazioni che vengono principalmente da quattro fonti: attivita' di ricerca del team, telemetrie prodotte dall'enorme installato dei prodotti Cisco in ambito cyber sec. (basti pensare al gia' citato Snort che per anni e' stato parte della soluzione Firewall e Umbrella che raccoglie telemetrie a livello DNS), attivita' OSInt e partnership con attori terzi.

> Anticipazione: questa base sembra essere comune a molti vendor.

Elemento interessante il fatto che Talos e' attiva nella ricerca delle vulnerabilita' software e [rilascia diversi report](https://www.talosintelligence.com/vulnerability_reports). Il servizio CORE con cui si propone non e' pero' la parte di Threat Intelligence: la struttura dei servizi ruota attorno al concetto di Incident Response nella forma della disponibilita', a richiesta, di gestire e rispondere ad un incidente di sicurezza. All'interno di questa struttura di servizi vi e' anche la possibilita' di accede ai dati di Intelligence su richiesta.

Per erogare in modo efficace il servizio vengono messi a disposizione ulteriori servizi di cui cito quelli che ritengo particolarmente sensati laddove l'esigenza e' la response:

- IR plan: la defizinione di un piano di Incident Responce
- IR playbook: la possibilita' di definire e predisporre in anticipo dei playbook per velocizzare le attivita' di risposta all'incidente
- Threat Hunting: la possibilita' di verificare se esistono minacce attive all'interno della propria infrastruttura.

E' da considerare che un'organizzazione matura probabilmente ha gia' un piano di IR strutturato, quindi le attivita' preparatorie in questo ambito potrebbero essere di puro "on boarding" a livello di servizio e di coordinamento con il nuovo team.

Sul fronte dei playbook mi riservo di riprendere in mano il tema in un capitolo a parte. La mia sensazione e' che oggi le aziende sottovalutino i vantaggi di un po' di automazione si tutti i fronti. Anche molti task in ambito cyber sec. possono essere resi piu' efficienti introducendo elementi di automazione: i playbook in un contesto di IR sono un ottimo esempio. Come detto, questo tema lo riprendiamo.

Le skills in ambito Threat Hunting non sono banali e non basta conoscere le tecnologie che si hanno in casa. Su questo tema un supporto esterno credo sia molto utile praticamente a tutte le realta'. Da tenere in considerazione.

A livello di struttura il servizio prevede quindi di accede a delle "funzionalita'" su richiesta (vedi la parte di Intelligence o la parte di IR), a dei report periodici sull'andamento del servizio ed a delle comunicazioni di emergenza in relazione ad evidenze di intelligence particolarmente gravi come eventuali attivita' da parte di TA che possono essere interessanti per l'organizzazione.

A scanso di equivoci: questa categoria di servizi non e' da assimilare al mondo detection.

Un po' di link per approfondire:

1. <https://www.youtube.com/@CiscoTalosIntelligenceGroup>
2. <https://blog.talosintelligence.com/category/threat-source-newsletter/>
3. <https://talosintelligence.com/resources/580>
4. <https://www.cisco.com/c/dam/global/en_sg/solutions/industries/talos_white_paper.pdf>

Nota sul terzo link: da notare che il blueprint in relazione all'ecosistema sicuro parte da "analisi della superficie di attacco e asset management".

## Prossimo post?

La settimana prossima mi organizzo per raccogliere i dati sui servizi Palo Alto. Per feedback, domande, osservazioni lasciate i vostri commenti.
