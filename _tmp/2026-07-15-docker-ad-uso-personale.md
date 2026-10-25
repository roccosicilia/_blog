---
layout:     post
title:      "Docker ad uso personale"
date:       2026-07-15 10:00:54 +0200
categories: [hacking, ita, study-with-me]
image:      /assets/images-posts/image-3.png
---
In molti ambiti dell'IT capita di costruirsi piccoli tools per automatizzare alcuni task o rendere più comodo alcune operazioni e solitamente questi tools vengono utilizzati localmente sulle proprie workstation/laptop. Più di recente mi è capitato di dover automatizzare operazioni con strumenti che avrei poi dovuto spostare su altri host e mi è venuto in mente che avrei potuto creare dei pacchetti facili da portare in giro. È stata l'occasione buona per rimettere mano a Docker e in questo post riporto qualche appunto molto operativo per chi è interessato a valutare l'utilizzo di container per propri piccoli progetti personali.

Ci sono anche dei risvolti sul fronte della sicurezza nell'utilizzo dei container ma ne parlo in un prossimo post.

Per prima cosa due note su come ho deciso di lavorare a livello di ambiente di sviluppo. Questo tema credo sia molto soggettivo e legato al proprio ambiente di lavoro: nel mio caso per le mie attività di lavoro / ricerca / studio uso il mio MacBook di servizio ed ho trovato comodo utilizzare Docker Desktop per la gestione ordinaria dei container. I restanti strumenti sono i soliti: con VS Code, Github ed il terminal si fa tutto.

#### Preparazione del progetto

Provo a fare uno step-by-step di come ho avviato la base del progetto che sto portando avanti in questo periodo, la versione *containered* del mio C2 di laboratorio, così ve la potete scaricare ed implementare comodamente dove vi pare.

Ovviamente come primo step ho creato il progetto sul mio Github, codename: [portable_c2](https://github.com/roccosicilia/portable_c2/). Nella root dir di progetto ho preparato il Dockerfile con le istruzioni che mi serviranno per la creazione del container (ci ho messo un po' per trovare la conf. più pulita che sono riuscito a definire):

```
# immagine comoda per un progetto basato su python
FROM python:3.11-bookworm

# Apache e strumenti necessari per compilare mod_wsgi
RUN apt-get update && apt-get install -y \
    apache2 \
    apache2-dev \
    gcc \
    build-essential \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# installa mod_wsgi nello stesso Python dove verrà installato Flask
RUN pip install --no-cache-dir mod_wsgi

# abilita il modulo Apache mod_wsgi
RUN mod_wsgi-express install-module \
    && mod_wsgi-express module-config > /etc/apache2/mods-available/wsgi.load \
    && ln -s /etc/apache2/mods-available/wsgi.load /etc/apache2/mods-enabled/wsgi.load

WORKDIR /app

# installa dipendenze Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copia applicazione
COPY . .

# config Apache
COPY apache-config.conf /etc/apache2/sites-available/000-default.conf

# fix il warning AH00558
RUN echo "ServerName localhost" >> /etc/apache2/apache2.conf

EXPOSE 80

CMD ["apache2ctl", "-D", "FOREGROUND"]
```

Come si intuisce dal Dockerfile il container ospiterà un'applicazione molto semplice basata su python e la pubblicazione di alcuni elementi è affidata ad Apache. Va quindi predisposta la configurazione del web-server:

```
<VirtualHost *:80>
    WSGIDaemonProcess c2 python-path=/app/app
    WSGIProcessGroup c2
    WSGIScriptAlias / /app/app/app.wsgi

    <Directory /app/app>
        Require all granted
    </Directory>

    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```

Molto semplicemente il container esporrà l'applicazione "c2" il cui codice sarà posizionato nella directory */app* di cui, giusto per avviare il servizio, scriviamo del codice di test utile ad avere un output per fare qualche test.

In questo caso ci basta un file di base che verrà eseguito alla chiamata dell'app (*app.py*):

```
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "HOME :: Test"
```

Per come funzionano le python app pubblicate via Apache è necessario avere a disposizione un file "ponte" che verrà chiamato direttamente da Apache e che vediamo anche nella conf. del web server con la direttiva *WSGIScriptAlias* per "app.wsgi":

```
from app import app as application
```

Come si intuisce il file in questione non fa altro che importare il codice di *app.py*. Ultima componente per quanto riguarda python è il requisito iniziale di *flask* e *requests* che andiamo a dichiarare nel file *requirements.txt* e che abbiamo già deciso di utilizzare nel nostro Dockerfile:

```
Flask==3.1.3
requests==2.32.3
```

Per la configurazione del container possiamo definire dei parametri a livello di file di configurazione, nel mio caso il *docker-compose.yml* è così strutturato:

```
services:
  web:
    build: .
    volumes:
      - .:/app
    ports:
      - "8080:80"
```

Per comodità ho deciso di usare un bind mount della directory */app*. Non so se è la scelta migliora ma per ora procederò in questo modo. Per quanto riguarda la porta tcp da utilizzare per accedere all'app ho definito una tipica tcp\8080 mappata alla porta 80 di Apache web server all'interno del container. Questo significa che l'applicazione sarà disponibile sull'IP della macchina host via browser con una richiesta a *http://a.b.c.d:8080*.

#### Ingnore file

Ho sempre mal tollerato le *repo* incasinate quindi, se il progetto è strutturato, preferisco definire subito cosa mettere in *ignore*:

File *.dockerignore*:

```
.git
__pycache__
*.pyc
.venv
```

File .gitignore:

```
__pycache__/
*.pyc
.venv/
.env
```

#### VS code e container

Ora è tutto apparecchiato e possiamo procedere con la build del container che conterrà un'app di test.

<img src="{{ '/assets/images-posts/image-1.png' | relative_url }}" alt="image 1" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Come si vede dallo screenshot il comando per eseguire la build è:

```
docker compose up -d --build
```

Ovviamente il comando ha senso se viene eseguito dalla directory in cui si trovano anche i file di configurazione che abbiamo preparato. Se tutto è stato configurato correttamente dovremmo poter accedere alla nostra applicazione di test con il browser.

<img src="{{ '/assets/images-posts/image-2.png' | relative_url }}" alt="image 2" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

C'è un trick, una funzionalità in realtà, molto interessante che mi permette di lavorare comodamente da VS Code per aggiornare la mia applicazione python: la chiamata *volume* nel file *docker-compose.yml*. Stiamo sostanzialmente chiadendo a Docker di tenere sincronizzato il contenuto della directory /app, ovverò l'area del file system locale che useremo per posizionare tutti i file dell'applicazione.

In questo modo a seguito di una modifica sarà sufficiente riavviare il servizio web senza eseguire una nuova build del container. Ovviamente se i change sono più profondi e riguardano la struttura stessa del container faremo semplicemente una nuova build.

<img src="{{ '/assets/images-posts/image-3.png' | relative_url }}" alt="image 3" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Giusto per vedere cosa succede, nello screenshot ho eseguito una semplice modifica della print di test.

<img src="{{ '/assets/images-posts/image-4.png' | relative_url }}" alt="image 4" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Eseguo il restart del servizio web con il comando:

```
docker compose restart web
```

Se non ci sono errori troveremo le modifiche applicate controllando l'output dell'applicazione:

<img src="{{ '/assets/images-posts/Screenshot-2026-07-15-at-08.06.19.png' | relative_url }}" alt="Screenshot 2026 07 15 at 08.06.19" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

#### Note di chiusura

Come ho accennato ci sono anche risvolti sul piano della sicurezza dei sistemi nell'uso dei container. Ho voluto condividervi i miei appunti anche per introdurre chi non conosce la tecnologia al contesto operativo per fare poi qualche ragionamento di legato all'ambito sec.

È un argomento molto DevOps che, pur non volendo metterlo tra i requisiti minimi per chi si occupa di sicurezza informativa, è sicuramente un tema importante su cui è molto utile avere qualche base.
