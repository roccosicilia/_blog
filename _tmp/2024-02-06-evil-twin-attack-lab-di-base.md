---
layout:     post
title:      "Evil Twin Attack: lab di base"
date:       2024-02-06 18:00:00 +0100
categories: [cyber-security, hacking, ita]
image:
---
Ne ho parlato ogni tanto durante qualche live: l'attacco noto con il nome Evil Twin rappresenta ancora oggi uno strumento efficace per guadagnare un accesso ad una rete target. Nei contesti della sicurezza offensiva come i Penetration Test sulle infrastruttura WiFi o le attivita' di Red Teaming e' spesso un valido strumento per ricavare informazioni di base come una coppia di credenziali valide.

Ho pensato di costruire un lab permanente per alcuni scenari di base e con questo post condivido la configurazione del primo scenario. Il contesto piu' semplice prevede la possibilita' di trasmettere un segnale che sia confondibile dagli utenti come la rete WiFi dell'organizzazione, portare l'utente a connettersi alla rete "gemella" e tentare di carpire una credenziale.

[<img src="{{ '/assets/images-posts/image-7.png' | relative_url }}" alt="image 7" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />](https://www.patreon.com/posts/evil-twin-attack-97977741)

Video recap del lab di base

## Struttura del lab

Partiamo da qualcosa semplice da replicare. Con una linux-box installata su un laptop che abbia un adattatore Wireless teoricamente siamo gia' nelle condizioni di operare, ma ho notato che molti usano la propria linux-box (spesso una kali) tramite una guest. Per il mio lab usero' una delle mie "macchine da battaglia", un laptop con kali a cui aggiungo un adapter Wireless esterno, ma il principio di funzionamento e' applicabile anche per altri contesti.

<img src="{{ '/assets/images-posts/image-1.png' | relative_url }}" alt="image 1" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Questo laptop ha otto anni e ancora macina cicli.

Requisito tecnico dell'adapter Wireless: deve supportare la Monitor Mode e la Packet Injection per consentirci di "forzare" alcuni comportamenti. Come dicevo ritengo piu' comodo usare una macchina fisica anche per non diventare matto che le integrazioni ed i driver: la mia kali-box virtuale non sempre digerisce gli adarper esterni collegati via vUSB. Inoltre nel contesto fisico posso disporre di due interfacce WiFi ed una ethernet, che non guasta in alcuni scenari.

Per fare qualche test e' bene dotarsi anche di un device che faccia da "vittima", nel mio caso e' in vecchio smartphone Android.

## Scenari di attacco

In questa revisione del lab vorrei affrontare due scenari base da utilizzare in contesti operativi per guadagnare una credenziale di accesso alla rete target o raccogliere informazioni dai client.

In entrambi i casi implementeremo un access point "non legittimo" che dovra' apparire come uno degli access point del target per portare l'utente vittima ad utilizzare la nostra rete, l'effetto sull'utente sara' pero' diverso nei due casi.

Nel primo caso simuleremo un captive portal associato alla rete target: gli utenti che si collegheranno al nostro AP verranno indirizzati ad una pagina web che chiede le credenziali per l'accesso alla rete WiFi. Se l'utente non si rende conto di essersi collegato ad una rete "ostile" potrebbe essere portato ad inserire la propria credenziale che verrebbe poi salvata in chiaro dal finto servizio di rete.

Il secondo caso e' leggermente piu' subdolo e consiste nel mettere a disposizione un AP che fornira' poi una connessione ad internet, simulando quella che potrebbe essere una rete guest aperta. In questo caso non vengono presentati captive portal ma semplicemente il device vittima accedera' alla rete internet. L'attacker si limitera' a "sniffare" in traffico con tools come Wireshark.

## Captive portal scenario

Nota introduttiva: sto avendo qualche problema con la creazione della pagina web custom del captive portal, quindi su questo punto aspettiamoci degli update. Passo allo step-by-step.

### *Setup iniziale*

Come accennavo il mio laptop ha due wireless adapter, quindi nel mio caso uno verra' configurato in monitor mode mentre l'altro restera' connesso alla rete locale. La monitor mode e' una modalita' di lavoro delle NIC che consente di ricevere il traffico a livello di segnale (non viene catturato tutto il traffico) dei dispositivi wireless a portata della nostra "stazione" senza la necessita' di un collegamento diretto tra dispositivi (<https://en.wikipedia.org/wiki/Monitor_mode>). E' una modalita' di lavoro completamente passiva che ci e' utile per analizzare le reti wireless disponibili attorno a noi, per questo motivo una volta che l'adapter e' posto in monitor mode non puo' essere usato anche come *station* per la connessione WiFi.

<img src="{{ '/assets/images-posts/image-2.png' | relative_url }}" alt="image 2" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

configurazione dei due wireless adapter

Nell'immagine ho segnato in arancione la configurazione della NIC wlan0, felicemente connessa alla rete WLAN del mio lab, e la NIC wlan1 che poco sotto riporta la specifica ***link/ieee802.11/radiotap*** che ci consente di catturare anche i RadioTap Header, una serie di informazioni aggiuntive sul sistema di radio-frequenza che stiamo osservando.

<img src="{{ '/assets/images-posts/image-4.png' | relative_url }}" alt="image 4" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

cattura con wireshark della NIC wlan1 con aurodump-ng attivo

Da questa configurazione possiamo iniziare a lavorare con airgeddon, disponibile come pacchetto in molte distro o reperibile qui: <https://github.com/v1s1t0r1sh3r3/airgeddon.git>.

### *"airgeddon"*

Questa utility integra diverse funzionalita' utili all'analisi delle reti wireless e ad alcuni scenari di attacco. Questo post non e' una guida all'utilizzo del tool di cui si trova ampia documentazione in rete (google is you friend), mi concentro quindi sulla metodologia e sui passi per implementarla.

Tra le funzionalita' interessanti c'e' la possibilita' di avviare un servizio captive portal con relativa rete "aperta" (facendo spoofing dell'AP legittimo) e portale di accesso (personalizzabile) in cui viene chiesta una password per autenticarsi alla rete.

<img src="{{ '/assets/images-posts/image-6.png' | relative_url }}" alt="image 6" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

ipotesi di scenario

Tra le opzioni e' possibile lanciare un deauthentication attack che ci consente di forzare la disconnessione di uno specifico client dalla rete target. In questo modo otterremmo che l'utente, vedendosi disconnesso, tentera' di eseguire nuovamente l'accesso alla rete, auspicabilmente selezionando il nostro rogue AP che si presentera' con lo stesso SSID della rete legittima. In questo caso, essendo la rete aperta, non verra' chiesta una credenziale e l'utente si trovera' connesso alla rete dell'attacker per essere poi reindirizzato alla pagina del captive portal.

Qui c'e' un tema di consapevolezza: in condizioni normali all'utente non viene presentato nessun captive portal e ci si aspetta che la vittima, insospettiva, chiuda la pagina e vada a verificare a cose si e' connesso. Se l'utente e' particolarmente impreparato (imho) potrebbe decidere di inserire le proprie credenziali nella login form del captive portale, credenziali che l'attacker intercettera'.

[Nota tecnica] Aigeddon di default saltva le credenziali raccolte in /root/{nome_file}.txt ma in alcune versione potrebbe presentarsi un bug per cui la credenziale non viene salvata. In questo caso e' possibile aggirare il problema utilizzando wireshark e sniffando il traffico della NIC utilizzata per il rogue AP: la password e' osservabile in chiaro nel traffico HTTP tra l'utente e il captive portal.

## Nel prossimo post ...

... una piccola evoluzione dello scenario descritto in cui non usiamo il captive portal ma **proviamo ad inserire qualche altro elemento per raccogliere informazioni** dal target.

## Disclaimer

Per quanto sia ovvio meglio ricordarlo: le informazioni riportate in questo post hanno scopo divulgativo e sono indirizzate a figure tecniche del mondo dell'info sec. o figure IT che hanno l'esigenza di comprendere le metodologie di attacco e valutare le contromisure opportune.
