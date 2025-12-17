import random
from config.database import get_db
from models import Monstre
from services.effet_service import verifier_effet_special

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

def tour_de_combat(equipe, monstre, vague, callback_degats=None, buffs_temporaires=None):
    if buffs_temporaires is None:
        buffs_temporaires = {}
    afficher_etat_combat(equipe, monstre, vague)

    # Vérifie les effets spéciaux
    effet, message = verifier_effet_special()
    if effet:
        print(f"\n' {message}\n")
        input("Appuyez sur Entrée pour continuer...")
    
    print("ATTAQUE DE L'EQUIPE")
    vivants = [p for p in equipe if p.est_vivant()] 

    for joueur in vivants:
        degats = joueur.attaquer(monstre)

        # Application des effets
        if buffs_temporaires.get('boost_atk', False):
            degats += 5
        elif effet == "critique":
            degats *= 2
            print(f" {joueur.nom} -> {monstre.nom} ({degats} dmg) [CRITIQUE!]")
        elif effet == "rate":
            degats = 0
            print(f" {joueur.nom} -> {monstre.nom} (0 dmg) [RATÉ!]")
        elif effet == "fatigue":
            degats = int(degats * 0.7)
            print(f" {joueur.nom} -> {monstre.nom} ({degats} dmg) [FATIGUÉ]")
        else:
            print(f"{joueur.nom} -> {monstre.nom} ({degats} dmg)")
        
        monstre.prendre_degats(degats)
        if callback_degats and degats > 0:
            try:
                callback_degats(degats)
            except Exception:
                pass

    if effet == "regen":
        for p in vivants:
            p.pv = min(p.pv + 20, p.pv_max)
            print("\n' L'équipe récupère 20 PV !")

    if not monstre.est_vivant():
        print(f"{monstre.nom} est mort !")
        return "victoire"

    print("\nATTAQUE DU MONSTRE")
    if not vivants:
        print("Aucun personnage vivant pour être ciblé.")
        return "defaite"

    cible = random.choice(vivants)
    degats = monstre.attaquer(cible)

    # Effets défense renforcée (réduit dégâts du monstre)
    if effet == "defense":
        degats = max(1, degats - 5)
        print(f"{monstre.nom} -> {cible.nom} ({degats} dmg) [REDUIT!]")
    else:
        print(f"{monstre.nom} -> {cible.nom} ({degats} dmg)")

    cible.prendre_degats(degats)

    if all(not p.est_vivant() for p in equipe):
        print("Toute l'équipe est morte.")
        return "defaite"

    input("Appuyez sur Entrée pour continuer...")
    return "continuer"