from pymongo import MongoClient

def get_db():
    client = MongoClient("mongodb://localhost:27017/")
    return client["python_game"]

def formater_temps(secondes):
    if secondes < 60:
        return f"{secondes}s"
    elif secondes < 3600:
        minutes = secondes // 60
        sec = secondes % 60
        return f"{minutes}min {sec}s"
    else:
        heures = secondes // 3600
        minutes = (secondes % 3600) // 60
        sec = secondes % 60
        return f"{heures}h {minutes}min {sec}s"

def afficher_menu_principal():
    print("\n" + "="*50)
    print("COMBAT INFINI")
    print("="*50)
    print("1. Jouer")
    print("2. Classement")
    print("3. Statistiques")
    print("4. Quitter")
    print("="*50)

def afficher_personnages_disponibles():
    db = get_db()
    persos = list(db.personnages.find())

    print("\n" + "="*50)
    print("PERSONNAGES")
    print("="*50)
    for i, p in enumerate(persos, 1):
        print(f"{i}. {p['nom']} - ATK:{p['atk']} DEF:{p['defn']} PV:{p['pv']}")
    print("="*50)
    return persos

def afficher_equipe(equipe):
    print("\n" + "="*50)
    print("EQUIPE")
    print("="*50)
    for i, p in enumerate(equipe, 1):
        print(f"{i}. {p['nom']} - ATK:{p['atk']} DEF:{p['defn']} PV:{p['pv']}")
    print("="*50)

def afficher_statistiques(joueur):
    db = get_db()
    stats = db.statistiques.find_one({"joueur": joueur})

    print("\n" + "="*50)
    print("STATISTIQUES")
    print("="*50)
    print(f"Nom : {joueur}")

    if not stats:
        print(f"Aucune statistique pour {joueur}")
    else:
        print(f"Parties jouées : {stats['parties_jouees']}")
        print(f"Meilleur score : {stats['meilleur_score']} vagues")
        print(f"Total de vagues : {stats['total_vagues']}")
        print(f"Monstres battus : {stats['monstres_battus']}")
        print(f"Dégâts totaux : {stats['degats_total']}")
        temps_total = stats.get('temps_total', 0)
        print(f"Temps de jeu : {formater_temps(temps_total)}")

    print("="*50)


def initialiser_stats(joueur):
    db = get_db()
    stats = db.statistiques.find_one({"joueur": joueur})
    
    if not stats:
        db.statistiques.insert_one({
            "joueur": joueur,
            "parties_jouees": 0,
            "meilleur_score": 0,
            "total_vagues": 0,
            "monstres_battus": 0,
            "degats_total": 0,
            "temps_total": 0
        })


def mettre_a_jour_stats(joueur, vagues, monstres_battus, degats_total, temps_combat):
    db = get_db()
    initialiser_stats(joueur)

    stats = db.statistiques.find_one({"joueur": joueur})
    meilleur = max(stats['meilleur_score'], vagues)

    db.statistiques.update_one(
        {"joueur": joueur},
        {
            "$set": {"meilleur_score": meilleur},
            "$inc": {
                "parties_jouees": 1,
                "total_vagues": vagues,
                "monstres_battus": monstres_battus,
                "degats_total": degats_total,
                "temps_total": temps_combat
            }
        }
    )

def afficher_classement():
    db = get_db()
    scores = list(db.scores.find().sort("score", -1).limit(3))

    print("\n" + "="*50)
    print("CLASSEMENT")
    print("="*50)
    if not scores:
        print("Aucun score.")
    else:
        for i, s in enumerate(scores, 1):
            print(f"{i}. {s['joueur']} - {s['score']} vagues")
    print("="*50)

def sauvegarder_score(joueur, score):
    db = get_db()
    db.scores.insert_one({"joueur": joueur, "score": score})

def valider_entree_numerique(message, a, b):
    while True:
        try:
            x = int(input(message))
            if a <= x <= b:
                return x
            print(f"Entre {a} et {b}.")
        except:
            print("Nombre invalide.")

def valider_entree_texte(message, min_len=1):
    while True:
        t = input(message).strip()
        if len(t) >= min_len:
            return t
        print(f"Min {min_len} caractère(s).")
