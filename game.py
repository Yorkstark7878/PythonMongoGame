import random
from models import Personnage, Monstre
from utils import get_db, sauvegarder_score, afficher_equipe, mettre_a_jour_stats

def afficher_choix(persos_db,deja_pris):
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

def gerer_equipe(persos_db,equipe,deja_pris,choix):
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
        choix = choix_perso(persos_db,deja_pris)
        gerer_equipe(persos_db, equipe, deja_pris, choix)

    print("\nEquipe prête !")
    afficher_equipe([{"nom": p.nom, "atk": p.atk, "defn": p.defn, "pv": p.pv} for p in equipe])
    return equipe

# On convertit le curseur Mongo en liste avant random.choice
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

def tour_de_combat(equipe, monstre, vague, callback_degats=None):
    """Gère un tour de combat entre l'équipe et le monstre."""
    afficher_etat_combat(equipe, monstre, vague)

    print("ATTAQUE DE L'EQUIPE")
    vivants = [p for p in equipe if p.est_vivant()] # évite d’appeler attaquer() sur un pnj mort

    for joueur in vivants:
        degats = joueur.attaquer(monstre)
        monstre.prendre_degats(degats)

        # callback utilisé pour compter les dégâts cumulés sans variable globale
        if callback_degats:
            try:
                callback_degats(degats)
            except Exception:
                pass
        print(f"{joueur.nom} → {monstre.nom} ({degats} dmg)")

    if not monstre.est_vivant():
        print(f"{monstre.nom} est mort !")
        return "victoire"

    print("\nATTAQUE DU MONSTRE")
    if not vivants:
        print("Aucun personnage vivant pour être ciblé.")
        return "defaite"

    cible = random.choice(vivants)
    degats = monstre.attaquer(cible)
    cible.prendre_degats(degats)
    print(f"{monstre.nom} → {cible.nom} ({degats} dmg)")

    if all(not p.est_vivant() for p in equipe):
        print("Toute l'équipe est morte.")
        return "defaite"

    input("Appuyez sur Entrée pour continuer...")
    return "continuer"

def jouer(joueur, equipe):
    vague = 0
    monstres_battus = 0
    # conteneur mutable pour que la callback puisse modifier la valeur
    degats_total_container = {"total": 0}

    print("\nLe combat commence !")
    input("Appuyez sur Entrée pour démarrer...")

    while True:
        vague += 1
        monstre = obtenir_monstre_aleatoire()

        # Combat jusqu'à ce que le monstre ou l'équipe meurt
        while monstre.est_vivant() and any(p.est_vivant() for p in equipe):
            resultat = tour_de_combat(
                equipe,
                monstre,
                vague,
                callback_degats=lambda d: degats_total_container.__setitem__('total', degats_total_container['total'] + d)
            )

            if resultat == "victoire":
                monstres_battus += 1
                print(f"Vague {vague} gagnée !")
                input("Monstre suivant...")
                break

            elif resultat == "defaite":
                sauvegarder_score(joueur, vague - 1)
                mettre_a_jour_stats(joueur, vague - 1, monstres_battus, degats_total_container['total'])
                print(f"Vous avez survécu à {vague - 1} vagues.")
                return vague - 1