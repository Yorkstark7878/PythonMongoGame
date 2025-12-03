import random
from models import Personnage, Monstre
from utils import get_db, sauvegarder_score, afficher_equipe, mettre_a_jour_stats

def creer_equipe():
    db = get_db()
    persos_db = list(db.personnages.find())
    equipe = []
    deja_pris = set()

    print("\n=== CREATION DE L'EQUIPE ===\n")

    for i in range(3):
        while True:
            print(f"\nChoix du perso {i+1}")
            for n, p in enumerate(persos_db, 1):
                mark = "X" if n-1 in deja_pris else " "
                print(f"[{mark}] {n}. {p['nom']} - ATK:{p['atk']} DEF:{p['defn']} PV:{p['pv']}")

            choix = input("Numéro : ")
            try:
                choix = int(choix)
                if 1 <= choix <= len(persos_db) and choix-1 not in deja_pris:
                    d = persos_db[choix-1]
                    equipe.append(Personnage(d["nom"], d["atk"], d["defn"], d["pv"]))
                    deja_pris.add(choix-1)
                    break
                else:
                    print("Choix invalide ou déjà pris.")
            except:
                print("Entrée invalide.")

    print("\nEquipe prête !")
    afficher_equipe([{"nom": p.nom, "atk": p.atk, "defn": p.defn, "pv": p.pv} for p in equipe])
    return equipe

def obtenir_monstre_aleatoire():
    db = get_db()
    data = random.choice(list(db.monstres.find()))
    return Monstre(data["nom"], data["atk"], data["defn"], data["pv"])

def afficher_etat_combat(equipe, monstre, vague):
    print("\n==============================")
    print(f"VAGUE {vague}")
    print("==============================")
    print(monstre.afficher_stats(), "\n")
    print("EQUIPE :")
    for i, p in enumerate(equipe, 1):
        etat = "VIVANT" if p.est_vivant() else "MORT"
        print(f"{i}. {p.afficher_stats()} [{etat}]")
    print()

def tour_de_combat(equipe, monstre, vague):
    afficher_etat_combat(equipe, monstre, vague)

    print("ATTAQUE DE L'EQUIPE")
    vivants = [p for p in equipe if p.est_vivant()]
    for p in vivants:
        d = p.attaquer(monstre)
        monstre.prendre_degats(d)
        print(f"{p.nom} → {monstre.nom} ({d} dmg)")

    if not monstre.est_vivant():
        print(f"{monstre.nom} est mort !")
        return "victoire"

    print("\nATTAQUE DU MONSTRE")
    cible = random.choice(vivants)
    d = monstre.attaquer(cible)
    cible.prendre_degats(d)
    print(f"{monstre.nom} → {cible.nom} ({d} dmg)")

    if all(not p.est_vivant() for p in equipe):
        print("Toute l'équipe est morte.")
        return "defaite"

    input("Entrée pour continuer...")
    return "continuer"

def jouer(joueur, equipe):
    vague = 0
    monstres_battus = 0
    degats_total = 0

    print("\nLe combat commence !")
    input("Entrée pour démarrer...")

    while True:
        vague += 1
        monstre = obtenir_monstre_aleatoire()

        while True:
            r = tour_de_combat(equipe, monstre, vague, lambda d: globals().__setitem__('degats_total', degats_total + d))

            if r == "victoire":
                monstres_battus += 1
                print(f"Vague {vague} gagnée !")
                input("Monstre suivant...")
                break
            elif r == "defaite":
                # Sauvegarde du score et mise à jour des stats
                sauvegarder_score(joueur, vague-1)
                mettre_a_jour_stats(joueur, vague-1, monstres_battus, degats_total)
                print(f"Vous avez survécu à {vague-1} vagues.")
                return vague-1
            
def tour_de_combat(equipe, monstre, vague, callback_degats=None):
    """Suivi des dégâts"""
    afficher_etat_combat(equipe, monstre, vague)

    print("ATTAQUE DE L'EQUIPE")
    vivants = [p for p in equipe if p.est_vivant()]
    for p in vivants:
        d = p.attaquer(monstre)
        monstre.prendre_degats(d)
        if callback_degats:
            callback_degats(d)
        print(f"{p.nom} → {monstre.nom} ({d} dmg)")

    if not monstre.est_vivant():
        print(f"{monstre.nom} est mort !")
        return "victoire"

    print("\nATTAQUE DU MONSTRE")
    cible = random.choice(vivants)
    d = monstre.attaquer(cible)
    cible.prendre_degats(d)
    print(f"{monstre.nom} → {cible.nom} ({d} dmg)")

    if all(not p.est_vivant() for p in equipe):
        print("Toute l'équipe est morte.")
        return "defaite"

    input("Entrée pour continuer...")
    return "continuer"