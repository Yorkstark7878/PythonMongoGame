from config.database import get_db
from models import Personnage

def afficher_choix(persos_db, deja_pris):
    print(f"\nChoix du perso  : ")
    for n, p in enumerate(persos_db, 1):
        mark = "X" if n-1 in deja_pris else " "
        print(f"[{mark}] {n}. {p['nom']} - ATK:{p['atk']} DEF:{p['defn']} PV:{p['pv']}")

def choix_perso(persos_db, deja_pris):
    while True:
        choix = input("Numéro : ")
        try:
            choix = int(choix)
            if 1 <= choix <= len(persos_db) and choix-1 not in deja_pris:
                return choix-1
            else:
                print("Choix invalide ou déjà pris.")
        except:
            print("Entrée invalide.")

def gerer_equipe(persos_db, equipe, deja_pris, choix):
    d = persos_db[choix]
    equipe.append(Personnage(d["nom"], d["atk"], d["defn"], d["pv"]))
    deja_pris.add(choix)

def creer_equipe():
    db = get_db()
    persos_db = list(db.personnages.find())
    equipe = []
    deja_pris = set()

    print("\n=== CREATION DE L'EQUIPE ===\n")

    for _ in range(3):
        afficher_choix(persos_db, deja_pris)
        choix = choix_perso(persos_db, deja_pris)
        gerer_equipe(persos_db, equipe, deja_pris, choix)

    print("\nEquipe prête !")
    from utils import afficher_equipe
    afficher_equipe([{"nom": p.nom, "atk": p.atk, "defn": p.defn, "pv": p.pv} for p in equipe])
    return equipe