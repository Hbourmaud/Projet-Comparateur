# Mise en place du serveur web

## Installation des composants à partir des référentiels Ubuntu

```bash
$ sudo apt update
$ sudo apt -y upgrade
$ sudo apt install openssh-server
```

## Configuration d'un pare-feu de base

```bash
$ sudo ufw enbale
$ sudo ufw allow OpenSSH
$ sudo ufw app list
```

<ins> Output : </ins>

```
Available applications:
  OpenSSH
```

## Installation de Flask et du code web

```bash
$ pip install flask
$ sudo python3 -m pip install mysql-connector-python
$ git clone https://gitlab.com/Hbourmaud/projetcomparateur
```
Cela permet d'obtenir le code utilisé pour les pages web ainsi que le backend du site. ( Veillez à changer les clés API disponible sur rapidapi.com ainsi que les identifiants pour se connecter à la base de donnée)

```bash
$ sudo ufw allow 5000
$ python3 app.py
```
Output :
```
* Serving Flask app 'app' (lazy loading)
* Environment: production
WARNING: This is a development server. Do not use it in a production deployment.
Use a production WSGI server instead.
* Debug mode: off
* Running on http://[YOUR IP]:5000/ (Press CTRL+C to quit)
```

## Installation de gunicorn

```bash
$ sudo apt install gunicorn
```

La commande nous permettant de spécifier l'interface et le port auxquels se connecter afin que l'application soit démarrée sur une interface accessible aux publics.

```bash
gunicorn --bind 164.132.230.224:5000 wsgi:app
```

Output :
```
[2022-01-18 12:26:50 +0100] [1447] [INFO] Starting gunicorn 20.1.0
[2022-01-18 12:26:50 +0100] [1447] [INFO] Listening at: http://10.5.1.4:5000 (1447)
[2022-01-18 12:26:50 +0100] [1447] [INFO] Using worker: sync
[2022-01-18 12:26:50 +0100] [1449] [INFO] Booting worker with pid: 1449
```

> A partir de cette commande, on peut visiter le site avec son adresse ip du serveur suivi de :5000

On peut en faire un service pour que ce soit plus simple à activer et à utiliser par la suite.

```bash
sudo nano /etc/systemd/system/myproject.service
```

myproject.service
```
[Unit]
Description=Gunicorn instance to serve myproject
After=network.targ

[Service]
User=brante
Group=www-data
WorkingDirectory=/home/brante
Environment="PATH=/home/brante/bin"
ExecStart=/home/brante/bin/gunicorn --workers 3 --bind unix:myproject.sock -m 007 wsgi:app

[Install]
WantedBy=multi-user.target
```
