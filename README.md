Combat Infini – README JeuPythonMongo

Description : 
Combat Infini est un jeu en ligne de commande où vous formez une équipe de trois personnages et affrontez des vagues de monstres. 
Les combats sont au tour par tour et la partie s’arrête lorsque toute l’équipe meurt.
L'objectif est de tenir le plus de vague possible.

Installation :
- Installer pymongo : pip install pymongo
- Initialiser la base : python db_init.py

Lancer le jeu : python main.py
MongoDB doit être actif en local.

Comment jouer :
- Entrez un nom.
- Choisissez 3 personnages différents.
- Combattez des monstres générés aléatoirement.
- Votre équipe attaque en premier, le monstre ensuite.
- Le score correspond au nombre de vagues gagnées.
- Les données sont enregistrées

Système de Buffs/Debuffs Aléatoires : 

Buffs positifs (10% de chance) :
- Coup critique** : Dégâts x2 pour ce tour
- Régénération** : +20 PV pour toute l'équipe
- Défense renforcée** : Réduit les dégâts reçus de 5

Ajout de la boutique d'items qui propose au joueur un catalogue d'attaque et défense afin de tenter de survivre un maximum de vague possible avec les choix qui sont les suivants : 
- Potion de soin : Cette potion restaure la santé du joueur à 50 PV.
- Grande potion : la grande potion restaure la santé entiere du joueur.
- Boost d'attaque : Le boost d'attaque ajoute +5 ATK au joueur par vague.
- Bouclier : Le bouclier ajoute au joueur une défense permanente de +3.

Paramètre monstres_battus en double
Dans l'appel à mettre_a_jour_stats() à la ligne 211 de game.py :
La fonction attend 5 paramètres dans cet ordre :

- joueur → Nom du joueur
- vagues → Nombre de vagues survécues
- monstres_battus → Nombre de monstres battus
- degats_total → Dégâts totaux
- temps_combat → Durée du combat

Dans ce jeu : 1 vague = 1 monstre
Donc vagues et monstres_battus ont toujours la même valeur. On passe donc monstres_battus deux fois pour remplir les deux paramètres avec la même donnée.
Cette architecture permet une évolution future du jeu (exemple : plusieurs monstres par vague) sans refactoriser la structure de la base de données.

Système Debuffs négatifs (5% de chance) :
- Fatigue : -30% ATK pour ce tour
- Coup manqué** : 0 dégât ce tour
Ces effets ajoutent de l'imprévisibilité et de la stratégie aux combats !

Le jeu sauvegarde automatiquement :
- votre meilleur score
- vos parties jouées
- vos vagues complétées
- vos dégâts totaux
- vos monstres vaincus

Fichiers principaux : 
- main.py : lancement
- game.py : logique des combats
- models.py : Personnages et Monstres
- utils.py : MongoDB et utilitaires
- db_init.py : initialisation de la bdd

Problèmes courants :
- Pas de connexion : vérifier que MongoDB est lancé.
- Pas de personnages et de monstres : relancer db_init.py.
- Import error : installer pymongo.