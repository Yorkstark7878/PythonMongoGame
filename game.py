import random
import time
from models import Personnage, Monstre
from utils import get_db, sauvegarder_score, afficher_equipe, mettre_a_jour_stats
from shop import gerer_boutique

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

def verifier_effet_special():
    """Vérifie si un éffet spécial se déclenche."""
    chance = random.randint(1, 100)

    # buff positif (10% de chance)
    if chance <= 10:
        buffs = [
            ("Coup Critique", "Les dégâts sont doublés à ce tour !"),
            ("regen", "Régénération ! 20 PV pour toutes l'équipe !"),
            ("Défense Suprême", "+5 points de défense pour ce tour !")
        ]
        return random.choice(buffs)
    
    # 5% de chance de debuff (entre 11 et 15)
    elif chance <= 15:
        debuffs = [
            ("Affiblissement", "Vous êtes affaiblis ! -30% ATK ce tour !"),
            ("louper", "Vous avez manqué votre attaque !"),
        ]
        return random.choice(debuffs)
    
    return None, None

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

def jouer(joueur, equipe):
    vague = 0
    monstres_battus = 0
    # conteneur mutable pour que la callback puisse modifier la valeur
    degats_total_container = {"total": 0}
    pieces = 0 # pièces du joueur
    buffs_temporaires = {}

    # Phase de boutique d'items avec chrono activé avant le combat
    temps_debut = time.time()

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
                callback_degats=lambda d: degats_total_container.__setitem__('total', degats_total_container['total'] + d),
                buffs_temporaires=buffs_temporaires
            )

            if resultat == "victoire":
                monstres_battus += 1
                pieces += 10
                print(f"Vague {vague} gagnée !")
                print(f"Vous gagnez 10 pièces ! Total pièces : {pieces}")

                buffs_temporaires.clear()

                while True:
                    choix = input("Voulez-vous visiter la boutique ? (o/n) : ").strip().lower()
                    if choix == 'o':
                        pieces, buffs_temporaires = gerer_boutique(equipe, pieces, buffs_temporaires)
                        break
                    elif choix == 'n':
                        print("Monstre suivant...")
                        break
                    else:
                        print("Choix invalide. Veuillez entrer 'o' ou 'n'.")

            elif resultat == "defaite":
                temps_fin = time.time()
                duree_combat = int(temps_fin - temps_debut)

                sauvegarder_score(joueur, monstres_battus)
                mettre_a_jour_stats(joueur, monstres_battus, degats_total_container['total'], duree_combat)

                print(f"\n{'='*50}")
                print(f"RÉSULTATS FINAUX")
                print(f"{'='*50}")
                print(f"Vagues survécues : {monstres_battus}")
                print(f"Monstres battus : {monstres_battus}")
                print(f"Dégâts infligés : {degats_total_container['total']}")
                print(f"Pièces gagnées : {pieces}")
                print(f"Temps de combat : {formater_temps(duree_combat)}")
                print(f"{'='*50}")
                
                return monstres_battus