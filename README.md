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

Debuffs négatifs (5% de chance) :
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