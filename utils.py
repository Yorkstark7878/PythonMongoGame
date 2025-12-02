from pymongo import MongoClient

def get_db():
    client = MongoClient("mongodb://localhost:27017/")
    return client["jeu_video"]

def afficher_menu_principal():
    print("\n" + "="*50)
    print("COMBAT INFINI")
    print("="*50)
    print("1. Démarrer le jeu")
    print("2. Classement")
    print("3. Quitter")
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
