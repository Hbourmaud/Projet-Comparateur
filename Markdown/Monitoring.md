# Monitoring

Pour le monitoring des différents serveurs, nous avons choisi d'utiliser netdata pour des raisons pratiques et de simplicitées.

Pour installer netdata sur chacun des serveurs que l'on veut monitorer:
```bash
sudo curl https://my-netdata.io/kickstart.sh > /tmp/netdata-kickstart.sh && sh /tmp/netdata-kickstart.sh --claim-token ['votre token disponible en créant un compte netdata'] --claim-rooms ['votre room id'] --claim-url https://app.netdata.cloud
```

Ensuite soit vous pouvez vous rendre sur https://app.netdata.cloud/ ou directement http://localhost:19999/

Cette solution permet de lister beaucoup de ressources mais notamment:
- Etat du serveur
- RAM utilisé
- CPU utilisé
- Bande passante entrante/sortante
- Utilisation des disques

En plus de cela, netdata permet d'être averti  lors de la détection d'un problème via de multiples notifications configurables. (ex: mail, discord ...)