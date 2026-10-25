---
layout:     post
title:      "CyberSec di base: pubblicazione dei servizi"
date:       2026-08-11 09:00:00 +0200
categories: [cyber-security, hacking, study-with-me]
image:      /assets/images-posts/monitor-cybersec.png
---
### Intro

Praticamente tutte le reti, salvo alcune eccezioni, devono esporre qualche servizio verso internet. Se riprendiamo il nostro schema “brutto” possiamo riportare visivamente un esempio molto semplice e che - ve lo anticipo - presenta degli errori di design dal punto di vista della sicurezza, ma per ora ci va bene così.

<img src="https://substackcdn.com/image/fetch/$s_!9Jwg!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F014598e3-acb6-4cc1-aaab-6c2d8f290106_1240x622.png" alt="immagine" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Supponiamo di avere un servizio WEB che dobbiamo rendere accessibile anche da internet. Il server avrebbe un proprio IP privato (10.10.10.5 nel nostro schema) ed il web server Apache sarebbe attivo sulla porta 80. Quindi gli utenti della rete LAN posso tranquillamente accedere al servizio digitando sul proprio browser http://10.10.10.11.

Ovviamente un utente esterno alla rete (es: noi da casa o un fornitore) non potrà accedere direttamente al server in quanto c’è “in mezzo” internet e quando la richiesta del browser arriverà al router domestico questo semplicemente gli dirà che non sa dove inoltrare una richiesta per 10.10.10.11. In questo caso ciò che dobbiamo fare è assegnare un IP pubblico gestito dal firewall di confine al servizio che vogliamo pubblicare, ad esempio se il nostro firewall gestisce la rete pubblica 1.2.3.0/24 possiamo utilizzare uno degli IP, il .4 nell’esempio, per pubblicare il servizio HTTP sulla porta 8080.

Questo ci consentirà di rendere disponibile il nostro servizio WEB anche all’esterno della rete e lo renderà accessibile potenzialmente a chiunque. Nell’articolo di oggi prendiamo in esame questa semplicissima configurazione e le implicazioni di sicurezza che ne derivano.

### Preparazione di un web-server

Per praticità userò una distro Ubuntu Server ma voi usate quello che volete. Quello che ci serve è posizionare un sistema nella rete che abbiamo dedicato ai server per poi usarlo come base per il nostro servizio. Faremo deliberatamente un errore di design: useremo un server posizionato in un punto della rete “interno” e pubblicheremo un suo servizio alla rete internet. I dettagli di questo errore li discuteremo assieme.

Per prima cosa va installata una virtual machine con il sistema operativo che si desidera utilizzare, nel mio caso sarà la citata Ubuntu:

<img src="https://substackcdn.com/image/fetch/$s_!szzZ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0013c7d0-3cf0-403d-84f5-29a4db6ab2f5_1624x998.png" alt="immagine" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

La macchina farà parte del LAB e sarà il sistema che utilizzeremo per pubblicare servizi di vario tipo. Nel mio caso avrà un IP compatibile con la mia rete server: 10.10.10.11/24.

```
# This is the network config written by 'subiquity'
network:
  ethernets:
    enp0s3:
      dhcp4: false
      dhcp6: false
      match:
        macaddress: 08:00:27:e5:68:4c
      set-name: enp0s3
      addresses:
        - 10.10.10.11/24
      routes:
        - to: default
          via: 10.10.10.254
      nameservers:
        addresses: [8.8.8.8]
  version: 2
```

Come servizio di pubblicazione utilizziamo il comodo Apache Web Server che possiamo installare facilmente:

```
sudo apt update
sudo apt install apache2
```

In questa occasione non ci serve fare molte personalizzazioni: il web server utilizza un set di files di configurazione di default posizionati in /etc/apache2, in particolare il file */etc/apache2/sites-enabled/000-default.conf* contiene la configurazione di default per un sito di default attivo via HTTP su porta tcp\80.

```
<VirtualHost *:80>

	#ServerName www.example.com

	ServerAdmin webmaster@localhost
	DocumentRoot /var/www/html

	ErrorLog ${APACHE_LOG_DIR}/error.log
	CustomLog ${APACHE_LOG_DIR}/access.log combined

</VirtualHost>
```

Della conf. ci interessa solo la posizione della DocumentRoot, ovvero la directory in cui posizionare i file del sito web di test. In questa posizione andremo a posizionare, per ora, un semplice file statico HTML.

```
<div>
  <h1>Server UP</h1>
</div>
```

Il risultato finale sarà la pubblicazione di un contenuto HTML:

<img src="https://substackcdn.com/image/fetch/$s_!BFKT!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4af533d7-551c-4ca0-9256-0760dc876d84_1175x538.png" alt="immagine" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

### Dalla rete LAN alla rete “esterna”

Torniamo per un attimo allo schema di rete riportato ad inizio post. In questa condizione tutte le VM presenti nel LAB sono in grado di contattare il web server ma mentre le le VM nella rete “LAN” dedicata ai server questo dialogo avviene a livello 2 nello stesso dominio di broadcast, per i sistemi che sono nella rete CLIENT la comunicazione avviene attraverso il Firewall.

In assenza di regole di comunicazione il Firewall, se configurato bene, non deve consentire traffico in modo incontrollato. Dobbiamo quindi, per consentirci qualche test, consentire alla rete client di accedere al web-server. In questa occasione facciamo una regole che consenta a tutta la rete ci raggiungere l’IP 10.10.10.11 per qualsiasi porta/protocollo.

Per il nostro pfSense il procedimento è abbastanza semplice, dobbiamo ovviamente accedere al sistema e posizionarci nella voce del menu ***Filrewall / Rules***:

<img src="https://substackcdn.com/image/fetch/$s_!Q5Ee!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffcafd573-ee4a-4f20-a78c-c6a121261c22_1041x385.png" alt="immagine" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Nel nostro caso la regola che vogliamo creare è relativa alla rete ***CLIENT***, accediamo quindi al relativo tab:

<img src="https://substackcdn.com/image/fetch/$s_!qASE!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3673f8d7-22b3-4091-8df5-7618f2c321c7_1041x303.png" alt="immagine" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Nel mio lab la regola è già presente ma disabilitata, infatti se accedo alla VM client Win10 e provo ad eseguire un ping del server 10.10.10.11 i pacchetti non giungono a destinazione:

<img src="https://substackcdn.com/image/fetch/$s_!Q3Xf!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd3ec77cb-e54c-4131-9dc6-11290b47b172_2312x1228.png" alt="immagine" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Per consentire il traffico dobbiamo quindi creare la specifica regola che ci serve, in questo caso autorizziamo tutta la rete CLIENT (10.10.11.0/24) a raggiungere 10.10.10.11:

<img src="https://substackcdn.com/image/fetch/$s_!_07v!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa0cb5e1b-7707-4496-8f78-eb9b4d597bf7_929x758.png" alt="immagine" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Una volta abilitata la regola non solo potremo eseguire un ping verso la destinazione ma vedremo anche la pagina web che abbiamo creato:

<img src="https://substackcdn.com/image/fetch/$s_!P4tT!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faeca20c5-c8ba-4382-84d7-a7bc75f48037_2708x1216.png" alt="immagine" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Ora che abbiamo avuto un assaggio del tema della visibilità (su cui torneremo) possiamo pubblicare il servizio “all’esterno”.

### NAT e pubblicazione del servizio

Abbiamo detto che il nostro scopo è fare in modo che il servizio sia raggiungibile dall’esterno della nostra rete ma gli IP privati del nostro LAB non possono essere raggiunti dai sistemi via internet. Questa esigenza viene gestita tramite NAT (network address traslation), una configurazione che sostanzialmente permette di associare un IP che il firewall gestisce sulla sua interfaccia esterna ad un sistema della rete interna.

Sul nostro pfSense la configurazione va definita in *Firewall / NAT / Port Forwarding* ed in questo caso ci limiteremo a prendere il traffico in arrivo sull’IP WAN porta TCP\8080 e ad re-indirizzarlo sull’IP 10.10.10.11 porta TCP\80:

<img src="https://substackcdn.com/image/fetch/$s_!0kb5!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F39dc541a-d694-4915-8559-cfbe83edac10_916x873.png" alt="immagine" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Attenzione: serve anche una regola di visibilità. Il NAT si occupa solo di associare la coppia IP:PORTA esterna alla coppia IP:PORTA interna. Il firewall pfSense crea automaticamente una regola dedicata quando si crea un NAT e possiamo andarla a vedere in *Firewall / Rules*:

<img src="https://substackcdn.com/image/fetch/$s_!BkMO!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F38449756-926c-40fd-9a20-9deea10e38d7_929x364.png" alt="immagine" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Se tutto ha funzionato a dovere sull’IP esterno del pfSense è ora disponibile il servizo che abbiamo pubblicato. Nel mio LAB il perimetro esterno è in realtà un’altra rete privata, la 192.168.1.0/24, ma il principio non cambia.

<img src="https://substackcdn.com/image/fetch/$s_!KlmX!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0cde583a-3932-4ca7-8bc0-ec9eb03d9080_1144x554.png" alt="immagine" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Per avere un quadro completo possiamo andare a verificare i log del Firewall filtrando per il nostro IP sorgente e vedere il tracciato del traffico relativo al nostro test:

<img src="https://substackcdn.com/image/fetch/$s_!s6w0!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7ebefabe-f3bc-481a-a4ad-542309679571_915x143.png" alt="immagine" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Dove compare l’IP “esterno” del cliente e l’IP “interno” del server. Non è visibile nel log, in questo caso, l’IP da cui siamo transitati a livello NAT, ovvero quello dell’interfaccia esterna del Firewall che nel mio lab è 192.168.1.250.

### Conclusioni

Ora che abbiamo un sistema che pubblica un servizio attraverso un firewall possiamo fare un po’ di ragionamenti su come analizzare il traffico di rete e cosa possiamo vedere grazie a strumenti come Wireshark.
