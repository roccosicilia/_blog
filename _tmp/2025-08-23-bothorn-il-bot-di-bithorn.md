---
layout:     post
title:      "BotHorn, il bot di BitHorn"
date:       2025-08-23 09:00:00 +0200
categories: [hacking, ita, update]
image:      /assets/images-posts/screenshot-2025-08-23-at-09.08.00.png
---
Visto che ho dedicato uno spazio del mio venerdì sera, compreso il secondo pezzo della live, al bot che ho introdotto e che vorrei espandere, ho pensato di scrivere due note sul funzionamento e sui possibili sviluppi.

#### Obiettivi base

Come [spiego nella live](https://youtube.com/live/0V73TF9yScg) l'idea nasce dall'esigenza di mantenere un certo livello di integrazione tra subreddit e gruppo Telegram e la prima proposta che è stata avanzata è stata quella di inviare un messaggio su Telegram che notifichi nuove discussioni. Ho fatto una variazione sul tema ed ho preparato uno script che va ad estrarre le discussioni presenti nel subreddit individuando quelle aperte nella giornata in corso, di queste viene fatto un summary ed inviato al gruppo.

<img src="{{ '/assets/images-posts/image-12.png' | relative_url }}" alt="image 12" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Summary del 22 agosto

A questa funzione se ne possono aggiungere altre ed alcune le ho ipotizzate nel readme file del progetto, che ovviamente è rilasciato open source qui: <https://github.com/b1th0rn/BotHorn>.

#### Struttura dello script

La cosa divertente di questi micro-progetti è che in poco si impara sempre qualcosa di nuovo. Ad esempio in questa occasione ho appreso che Reddit consente agli utenti di accedere ad alcune API senza particolari automazioni. Ad esempio che sul browser eseguite la richiesta <https://www.reddit.com/r/BitHorn/new.json?limit=10> otterrete l'export in JSON degli ultimi 10 topic del subreddit.

Sono partito da questo livello di accesso per fare il prototipo che però ha smesso di funzionare quando ho spostato lo script sul server dove avrebbe poi dovuto girare. Analizzando meglio prima il codice di errore (reddit non rispondeva più e mi restituiva un sonoro 403) e poi la documentazione, ho appreso che l'accesso alle informazioni è negato senza autenticazione se la richiesta arriva da una rete provider che evidentemente reddit censisce.

Questo è il motivo per il quale ho, infine, utilizzato Oauth:

```
def get_reddit_token():
    auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    data = {
        'grant_type': 'client_credentials'
    }
    headers = {'User-Agent': 'BitHornBot/0.2'}
    response = requests.post('https://www.reddit.com/api/v1/access_token', auth=auth, data=data, headers=headers)
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        print(f"Error Reddit OAuth: {response.status_code}")
        print(response.text)
        return None
```

Mentre scrivo mi sono accorto che ho lasciato nel codice le mie bruttissime *print* per avere l'output di cosa stava succedendo, poi le tolgo :-/  
Ad ogni modo a noi interessa il fatto che, una volta passati a reddit CLIENT_ID e CLIENT_SECRET il sistema ci ritorni il token di autenticazione. Con quello possiamo tornare a chiedere le informazioni che ci servono.

#### Hosting

Mentre cercavo info sul funzionamento della API di Telegram ho notato che molti utilizzato la piattaforma PythonAnywhere per i propri script. Ho quindi deciso di provarla per l'occasione.

Effettivamente il servizio è molto comodo e consente di istanziare script ed applicazioni in Python. Ho quindi configurato un semplice task (che non credo usi crontab) che esegue lo script tutte le sere alle 23:55. Il risultato è che tutte le sere sul gruppo Telegram arriva il messaggio con la lista dei nuovi post, ovviamente se ne esistono.

#### Note di chiusura

Come dicevo il bot è stato creato su una esigenza specifica ma ho intenzione di aggiungere alcune funzionalità e può facilmente essere riadattato. Il codice resta disponibile e se qualcuno vuole prendere spunto o proporre variazioni è liberissimo di farlo.
