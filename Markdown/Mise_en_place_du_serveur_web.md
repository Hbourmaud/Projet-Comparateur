# Mise en place du serveur web

## Installation des composants à partir des référentiels Ubuntu

```bash
$ sudo apt update
$ sudo apt -y upgrade
$ sudo apt install openssh-server
$ sudo apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools
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

## Intallation de Nginx

```bash
$ sudo apt update
$ sudo apt install nginx
```

## Ajustement du pare-feu

```bash
$ sudo ufw allow 'Nginx HTTP'
$ sudo ufw app list
```

<ins> Output : </ins>

```
Available applications:
  Nginx Full
  Nginx HTTP
  Nginx HTTPS
  OpenSSH
```

`$ sudo ufw status`

<ins> Output : </ins>

```
Status: active

To                         Action      From
--                         ------      ----
OpenSSH                    ALLOW       Anywhere                  
Nginx HTTP                 ALLOW       Anywhere                  
OpenSSH (v6)               ALLOW       Anywhere (v6)             
Nginx HTTP (v6)            ALLOW       Anywhere (v6)
```

## Installation de Mariadb

```
$ sudo apt install mariadb-server
$ sudo systemctl enable mariadb
$ sudo ss -alpnet
```

/!\ Pour la manipulation suivante, vous ne devez pas utiliser vos adresses publiques pour relier la database avec le serveur web /!\

```
$ sudo ufw allow from 164.132.230.224 to any port 3306
$ sudo ufw allow 3306/tcp
```



