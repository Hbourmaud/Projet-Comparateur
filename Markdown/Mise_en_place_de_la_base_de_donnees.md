# Mise en place du serveur de base de donnée

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

### Création de la base de données

> connexion à MySQL : `mysql -h localhost -u root`

La première connexion doit se faire par root vu que vous n'avez pas encore créé d'utilisateur.

Création d'un nouveau compte utilisateur dans MySQL : `CREATE USER 'nouveau_utilisateur'@'localhost' IDENTIFIED BY 'mot_de_passe';`

Vous devez ensuite lui donner tous les privilèges à cet utilisateur : `GRANT ALL PRIVILEGES ON * . * TO 'nouveau_utilisateur'@'localhost';`

Maintenant, vous pouvez utiliser votre nouveau "super-utilisateur" pour créer votre database.

`sudo mysql -u utilisateur -p`

Vous êtes maintenant entré dans MySQL avec votre comtpe utilisateur.
Vous pouvez créer votre base de données constituée de tables, de champs... et configuré le tout.

```
MariaDB [(none)]> CREATE database comparator;

MariaDB [(none)]> use comparator;

MariaDB [comparator]> CREATE TABLE accounts(id int PRIMARY KEY NOT NULL, users VARCHAR(100) NOT NULL, password VARCHAR(100) NOT NULL);

MariaDB [comparator]> CREATE TABLE gaming(id int NOT NULL, games VARCHAR(100) NOT NULL, sources VARCHAR(100) NOT NULL, price FLOAT NOT NULL, plateforms VARCHAR(15) NOT NULL);
```

Si pour X raison, vous n'avez pas défini le NOT NULL dans une des commandes permettant de définir si le champs doit être obligatoirement rempli ou non.
Vous pouvez utiliser cette commande : `ALTER TABLE nom_table MODIFY nom_colonne type NOT NULL/NULL;`

Utilisez la commande `ALTER TABLE nom_table ADD UNIQUE (nom_colonne);` pour que votre colonne ne possède seulement des valeurs uniques.





