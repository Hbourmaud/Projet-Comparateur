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

## Installation de Flask

```bash
$ pip install flask
$ pip install gunicorn
$ nano myproject.py
```

myproject.py
```py
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"

if __name__ == "__main__":
    app.run(host='164.132.230.224')
```

```bash
$ sudo ufw allow 5000
$ python3 myproject.py
```

Output :
```
* Serving Flask app 'myproject' (lazy loading)
* Environment: production
WARNING: This is a development server. Do not use it in a production deployment.
Use a production WSGI server instead.
* Debug mode: off
* Running on http://10.5.1.4:5000/ (Press CTRL+C to quit)
```

```bash
$ nano wsgi.py
```

wsgi.py
```py
from myproject import app

if __name__ == "__main__":
    app.run()
```
