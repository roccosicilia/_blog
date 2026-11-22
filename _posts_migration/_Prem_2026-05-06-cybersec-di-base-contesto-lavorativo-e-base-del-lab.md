---
layout:     post
title:      "CyberSec di base: contesto lavorativo e base del lab"
date:       2026-05-06 09:00:00 +0200
categories: [cyber-security, ita]
image:      /assets/images-posts/monitor-cybersec.png
---
### Il contesto

È giusto partire dal contesto. La sicurezza informatica nel 2026 è una materia che abbraccia moltissimi ambiti, coinvolge più settori, è interessata da normative e leggi e ci sono moltissime tecnologie usate in questo contesto. Non è possibile, oggi, occuparsi di tutto e l’ambito che vorrei coprire in queste sessioni è - ovviamente - quello tecnico, ovvero cerchiamo di capire come funzionano i sistemi e le rete, a che minacce sono esposti, come possiamo verificarle, cosa possiamo fare per migliorarne la robustezza e come possiamo difendere questi sistemi.

https://youtu.be/0dEjsKlQa2c

Per restare collegati al contesto faremo sicuramente dei “link” con l’ambito governance e normativo, ma saranno elementi aggiuntivi per avere anche il quadro generale. Chi si occupa di cybersecurity ad alto livello - anche i super tecnici che spaccano il bit - deve avere un’idea del contesto normativo e dei settori in cui si opera. Ci sarebbe anche da discutere degli aspetti legati alla geografia: il luogo spesso influenza enormemente il contesto.

Al di là dei temi normativi dobbiamo renderci conto che gli strumenti digitali hanno un livello di pervasività totale: l’intera infrastruttura del “mondo moderno” è fortemente legata al funzionamento dei sistemi informatici e della rete e l’aumento della complessità ci ha rapidamente portato ad avere, in proporzione, pochissime persone competenti nel merito, mentre continuiamo a sfornare “mediocri” operatori di settore.

Uno dei problemi che noto più frequentemente è una scarsa comprensione dell’infrastruttura: sia in ambito *Defense* che in ambito *Offensive*, ed in generale nel mondo info-sec, si incontrato molte figure che sanno eseguire un’attività di analisi o un penetration testing sulla base del funzionamento degli strumenti che hanno imparato ad usare ma non hanno la piena comprensione di quello che stanno facendo con la conseguenza diretta di non saper interpretare correttamente gli output di questi strumenti. Saper usare gli strumenti è importante, ma sapere cosa si sta facendo è fondamentale. È molto improbabile che riusciremo a risolvere problemi veri se non conosciamo bene il funzionamento di quello che vorremmo migliorare.

### Di che infrastruttura stiamo parlando?

Nella pratica, chi lavora in ambito cybersecurity, su che infrastrutture mette le mani? Molto dipende dal path di specializzazione che si decide di intraprendere. Chi vuole lavorare nel grande mondo della consulenza, che sia Blue o Red o un System Engineer (per usare le qualifiche che si usano nelle big tech) metterà le mani sull’infrastruttura di altri: grandi reti e detacenter se si tratta di lavorare per grandi gruppi, piccole installazioni e sale dati se si lavora con la piccola e media imprese.

Il mercato italiano, da questo punto di vista, presenta enormi squilibri: ci sono aziende che non hanno budget ed è difficile restituire qualità quando questa non viene pagata, ci sono anche aziende che - pur non buttando via i soldi - hanno modo di investire in progetti legati alla sicurezza informatica ed in questi casi c’è la possibilità più concreta di fare qualcosa di significativo.

Ovviamente sto facendo la “media del pollo”, conosco piccole aziende di consulenza che anche con budget bassi cercano di fare il meglio è ottengono risultati, cosa sicuramente ammirevole ma che presenta effetti collaterali non facili da gestire. Banalmente questo tipo di aziende raramente potranno permettersi trattamenti economici “generosi” per il proprio team (cosa che ovviamente auguro di cuore) che, se composto da persone valide, potrebbe essere attirato da aziende più strutturate e con posizioni più interessanti sia come inquadramento che come aspettativa di crescita professionale ed economica. Il mercato della consulenza è molto complesso ma in questo momento, per chi ha buone capacità, è un’ottimo punto di ingresso: ci sono molte richieste ed aziende di ogni tipo che hanno bisogno di persone qualificate sia in Italia che in Europa.

Tra le alternative al mondo delle consulenza è giusto citare (imho) il mondo Enterprise ed il Vendor (IT/Tech). Sono due ambiente estremamente diversi: con Enterprise mi riferisco a tutte quelle aziende strutturate che utilizzano molto la tecnologia ed hanno bisogno di figure specialistiche interne, mentre per i Vendor mi riferisco alle aziende che producono soluzioni e software dedicati al mondo IT.

Ogni ambito ha le sue peculiarità ed ognuno di noi ha esigenze diverse, ha quindi senso valutare le diverse opzioni. Il nostro ruolo all’interno di diverse strutture può essere applicato in modi molto diversi (ne ho un po’ parlato in una recente [puntata del podcast](https://www.infosecunplugged.it/episodes/episode-41.html)) ma il tipo di tecnologie e le basi tecniche che da cui partiremo sono tendenzialmente sempre le stesse: lavoreremo con dei sistemi operativi ed applicazioni (client e server), lavoreremo con reti più o meno complesse, lavoreremo con programmi ed automazioni.

### La pratica ed il lab

Ci dobbiamo costruire il nostro laboratorio da zero e nel farlo possiamo imparare una montagna di cose. Ci tengo a ricordare il “taglio” che ci accompagnerà: l’approfondimento e l’esigenza di partire dalle basi. Alcune cose le approfondiremo subito, altre strada facendo.

#### Partiamo dai devices

Inevitabilmente ci servono dei sistemi su cui andremo ad installare quello che ci serve ed è molto probabile che non tutti abbiano devices da dedicare al lab. Ora, se vi è possibile suggerisco di valutare qualcosa di fisico che non sia il vostro laptop o la vostra workstation per evitare di “spippolare” eccessivamente sul vostro O.S. di studio/lavoro. Ma se non avete alternative il piano B è installare un software di virtualizzazione sul vostro sistema desktop.

Il tema della virtualizzazione dei sistemi operativi lo prenderemo di petto più avanti ma in questa occasione è giusto dare degli elementi concreti. Ormai da diversi anni si utilizzato dei software che permettono di condividere l’hardware delle vostre macchine con più sistemi operativi attivi contemporaneamente. Tra i più noti nel mondo desktop (poi affronteremo anche il mondo server) c’è sicuramente VMware Workstation (o Fusion per OSX) e Oracle VirtualBox.

Sono software che potete installare sulla vostra macchina ed il loro compito è “simulare” l’hardware su cui installerete un nuovo sistema operativo che potrà girare “dentro” il vostro sistema desktop. Vederlo rende sicuramente tutto più semplice e nel video che accompagna questo post troverete diversi esempi.

La cosa importante che dobbiamo considerare, in questa prima sessione, è che il software di virtualizzazione è in grado di tenere “isolati” i sistemi virtualizzati tra loro (a livello di processi e risorse) e che possiamo quindi considerare una macchina virtuale come se fosse un server completo, con le sue risorse disco, la sua memoria RAM, il suo processore e la scheda di rete.

Nel lab anche il nostro laptop/desktop avrà un ruolo: sarà la base per le operazioni di gestione dei sistemi e useremo alcuni client software per collegarci alle macchine virtuali che useremo.

Per utenti Windows se aprite un terminale powershell trovere il client ssh.exe che useremo per collegarci ai sistemi unix-like.

<img src="https://substackcdn.com/image/fetch/$s_!YiAC!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9d9cac5e-372d-46ed-8c78-7d292e29c7a0_820x520.png" alt="immagine" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Per collegarci ai sistemi Windows useremo un altro tool: Remote Desktop Connection. Per ora è sufficiente accertarsi di averli a disposizione ed utilizzabili.

Se siete utenti Linux probabilmente avete più familiarità con la shell e sapete di avere a disposizione il cliente ssh, mentre per quanto riguarda il cliente per collegarsi ai sistemi Microsoft vi suggerisco Remmina.

Infine per gli utenti OSX abbiamo a disposizione lo stesso client ssh ed diverse utility per collegarsi in desktop remoto ai sistemi Microsoft, io uso Microsoft Remote Desktop.

Ricapitolando, per iniziare a mettere le mani sul lab dobbiamo avere sulla scrivania il nostro laptop/desktop, un laptop o un miniPC di laboratorio ed una USB pendrive da 4/8 GB.

#### La rete di base

Sul tema network ho intenzione di fare diversi approfondimenti, in questa prima sessione ci serve qualcosa di estremamente basilare per quanto riguarda i device fisici. La cosa più semplice è connettere tutto via Wireless usando la vostra rete Wi-Fi domestica o improvvisandone una con l’hotspot del vostro cellulare. L’importante è disporre di una rete che comprenda un accesso ad internet, il resto lo approfondiremo strada facendo.

Quando si lavora su una rete, anche di laboratorio, è sempre bene definire un piano di indirizzamento, ovvero una mappatura degli indirizzi IP utilizzati ed il relativi servizi che ci faremo girare sopra. Vi espongo il mio che siete liberi di replicare o modificare secondo le vostre esigenze.

Nota importante: solitamente è opportuno tenere separata la rete domestica dalla rete di laboratorio e faremo la stessa cosa in questa occasione. Gli host di base (laptop e macchina di lab) avranno un indirizzo nella rete domestica che sarà necessario per le operazioni di gestione, ma le macchine virtuali che andremo a creare dialogheranno su una rete separata e differente. È una buona abitudine tenere separato il mondo della “produzione” dal mondo dei lab e dei test anche per tematiche di sicurezza: molto spesso nei laboratori ci permettiamo configurazioni deboli che non metteremmo mai in produzione, ma se la rete è condivisa tecnicamente stiamo mescolando i due mondi.

La mia rete di gestione è un classico indirizzamento privato 192.168.1.0 con netmask 255.255.255.0 (ovvero a variare è solo l’ultimo ottetto ad ottenere il range 192.168.1.0-255. Su questa rete uso un DHCP server ma l’host di test ha un suo IP statico: il .66 in rete Wireless.

Per la rete di lavoratorio dobbiamo fare le cose con un po’ più ordine per non perderci pezzi e già da ora cominciamo a prenotare alcuni indirizzi che useremo più avanti. Come detto io vi riporto i miei ma voi potete scegliere liberamente quelli che vi piacciono.

<img src="https://substackcdn.com/image/fetch/$s_!hxp6!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F242ccd5e-59f3-4a7a-b428-d2f080f18933_820x392.png" alt="immagine" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Nel mio lab questa rete è interamente cablata in quanto uso un collegamento diretto tra il mio laptop ed il miniPC. Si tratta di una mia scelta di comodo che vi illustro nel video. Tutte le macchine che ho elencato, dal DC1 al Firewall, sono alcuni degli ambienti virtuali che creeremo in questa serie e con cui giocheremo.

#### Setup del primo host

Per iniziare la prima cosa da fare è installare un software di virtualizzazione sull’host che avete eletto a macchina “server”. Nel mio caso si tratta di un miniPC con OS Microsoft Windows 11, ma potete scegliere liberamente di utilizzare anche una performante distro Linux (i motivi che mi hanno portato a scegliere win li ho raccontati nel video).

Come software vi suggerisco di partire da Oracle VirtualBox, scaricatelo ed installatelo sul vostro ambiente. La UI è abbastanza standard e dovremmo non avere particolari problemi anche se usate altri OS rispetto a quelli che mostrerò nel lab.

Qualche nota tecnica sulla virtualizzazione che da ora in avanti useremo parecchio.

I moderni sistemi operativi lavorano per lo più su processori a 64bit che per essere usati in un contesto di virtualizzazione hanno bisogno di un host (la macchina fisica che userete) che supporti la Tecnologie di Virtualizzazione (VT-x per Intel, AMD-v per AMD). Solitamente è una funnzionalità abilitata di default sul BIOS ma è bene che ve ne accertiate per evitare noie più avanti.

Altro tema importante sono le risorse: la virtualizzazione “assegna” parte delle risorse dell’host fisico alle macchine virtuali ed ovviamente ci sono dei limiti dati dalla quantità di risorse hardware di cui disponete. Se il vostro host dispone di 16 GB di RAM, come nel mio caso, potrete tenere accese macchine virtuali per qual quantitativo di RAM.

<img src="https://substackcdn.com/image/fetch/$s_!lY9d!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F376efbde-a741-4126-b31c-199efb2a98dc_2032x1162.png" alt="immagine" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Nell’esempio vi mostro la RAM del mio host con quattro macchine virtuali accese di cui una (Detect1) da sola richiede 6 GB di RAM a causa dei servizi che deve far partire. Per buana parte di questo corso il problema non si pone, ma è giusto valutare sin da ora i limiti hardware che si potrebbero dover affrontare.

### Conclusione della sessione di introduzione

In questa sessione ho voluto proporre una panoramica del contesto e parlarvi dell’approccio che vorrei tenere in questa serie che credo durerà parecchio (ho un sacco di cose da raccontare).

Dalla prossima sessione partiamo dalla rete del lab introducendo la prima vera macchina virtuale su cui lavoreremo: il firewall.
