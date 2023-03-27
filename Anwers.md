#Prise en main

##Q1
C'est une architecture client-serveur avec deux clients connectés au même serveur.

##Q2
Les logs affichent les actions effectuées par le serveur et les clients, y compris les messages échangés. On peut ainsi suivre le déroulement de la communication entre les différents acteurs.

##Q3
Le fait que les messages ne soient pas chiffrés pose un problème de sécurité car ils peuvent être lus et modifiés par une personne non autorisée, ce qui viole le principe 
de Kerckhoffs.

##Q4
On peut utiliser un algorithme de chiffrement symétrique tel que l'AES pour chiffrer le message. Ensuite, on chiffre la clé de chiffrement symétrique avec la clé publique du destinataire et on envoie les deux éléments chiffrés. Le destinataire peut alors utiliser sa clé privée pour déchiffrer la clé de chiffrement symétrique et ainsi déchiffrer le message.


#Chiffrement

##Q1
urandom est une fonction qui produit des nombres aléatoires dans Python, mais elle n'est pas suffisamment sécurisée pour une utilisation en cryptographie car elle peut être prédictible.

##Q2
En utilisant des primitives cryptographiques, il est important de bien comprendre leur fonctionnement pour pouvoir détecter et corriger toutes les vulnérabilités potentielles. Si nous n'avons pas une telle compréhension, il y'a un risque que notre implémentation ne soit pas totalement sécurisée.

##Q3
Même si nous chiffrons les données, un serveur malveillant peut toujours perturber le fonctionnement du système en envoyant de fausses données ou en surchargeant le serveur. Le chiffrement ne garantit pas la sécurité totale du système.

##Q4
Il manque une étape d'authentification en utilisant le HMAC.

#Authenticated Symetric Encryption

##Q1
Fernet est moins risqué que les primitives cryptographiques car il est basé sur une implémentation éprouvée et gère automatiquement les problèmes de padding. La clé secrète est également générée automatiquement, ce qui diminue les risques liés au choix d'une clé faible ou prévisible.

##Q2
L'attaque s'appelle la "replay attack", elle consiste à renvoyer des messages précédemment interceptés pour tromper le destinataire.

#Q3

Pour se protéger contre les attaques de replay, on peut ajouter un identifiant unique à chaque message, appelé nonce ou un timestamp unique à chaque message. Cela permet de s'assurer que le message reçu est bien nouveau et n'a pas été intercepté et renvoyé ultérieurement.

#TTL

#Q1
A première vu nous ne voyons pas forcément de différence avec le chapitre précedent

#Q2
Le destinataire ne pourra pas déchiffrer le message  car le timestamp ne correspondra plus au temps actuel et le message sera considéré comme ayant dépassé sa durée de vie.

#Q3
Cette méthode peut aider à se protéger contre les attaques de replay si le temps d'expiration est suffisamment court pour empêcher la réutilisation des messages précédents.


#Q4
Les limites de cette solution peuvent inclure des problèmes de synchronisation des horloges entre les systèmes, la possibilité d'attaques par rejeu avec des messages précédemment émis mais toujours valides, et la nécessité de maintenir un historique des numéros de séquence ou des horodatages pour chaque message. 


#Regard critique

La librairie Fernet utilisée pour chiffrer les messages présente des vulnérabilités : elle ne peut pas chiffrer les messages trop volumineux, elle utilise une fonction pseudo-aléatoire pour générer les iv, ce qui peut rendre ces derniers prédictibles.

Bien que les messages soient chiffrés et non lisibles par le serveur, les noms des destinataires restent en clair, ce qui permet de voir qui envoie des messages à qui.

Ces vulnérabilités peuvent être exploitées pour intercepter ou tronquer des messages.


