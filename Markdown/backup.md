# Backup
Pour la sauvegarde des données de la base de données nous avons décider de sauvegarder tous les jours les fichiers sql via une backup automatisée par un service et un timer:
Création du script du service
```bash=
$ sudo nano /srv/backupdb.sh
#!/bin/bash
#Make backup of database

# Script vars
save_file='/srv/backup/'
log_file='/var/log/backup/backup_db.log'


usage() {
echo "Usage : backupdb.sh
Make a backup of database more specifically of comparator in tar.gz

        -h      Prints this message"
}

while getopts ":h" option; do
    case "${option}" in
        h)
            usage
            exit 0
            ;;
    esac
done

name=comparator_db_$(date +"%y%m%d_%H%M%S").tar.gz
mysqldump -h [your_database_ip] -p -u [user_database] [name_database] > ${save_file}tempdb.sql
tar -czvf ${name} ${save_file}tempdb.sql &> /dev/null
rm ${save_file}tempdb.sql
mv ${name} ${save_file}

#log

log_prefix=$(date +"[%y/%m/%d %H:%M:%S]")
log_line="${log_prefix} Backup ${save_file}${name} created successfully."
echo "${log_line}" >> "${log_file}"
echo "Backup ${save_file}${name} created successfully."
```

Création du service
```bash=
$ sudo nano /etc/systemd/system/backup_db.service
[Unit]
Description=Backup database for comparator

[Service]
ExecStart=/srv/backupdb.sh
Type=oneshot

[Install]
WantedBy=multi-user.target
```
Création du timer
```bash=
$ sudo nano /etc/systemd/system/backup_db.timer
[Unit]
Description= Timer for launch backup of comparator
Requires=backup_db.service

[Timer]
Unit=backup_db.service
OnCalendar=*-*-* 1:00:00

[Install]
WantedBy=timers.target
```

Pour la backup d'autres fichiers nous avons décider de sauvegarder en plus, ponctuellement les fichiers suivants:
- Code du site web (dispo sur git, app.py, templates/, static/)
- Les différents services, confs ( myprojet.service, backup_db.service, backup_db.timer)
