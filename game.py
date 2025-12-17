import time
from services.combat_service import obtenir_monstre_aleatoire, tour_de_combat
from utils import sauvegarder_score, mettre_a_jour_stats, formater_temps
from shop import gerer_boutique

def jouer(joueur, equipe):
    vague = 0
    monstres_battus = 0
    degats_total_container = {"total": 0}
    pieces = 0
    buffs_temporaires = {}

    temps_debut = time.time()

    print("\nLe combat commence !")
    input("Appuyez sur Entrée pour démarrer...")

    while True:
        vague += 1
        monstre = obtenir_monstre_aleatoire()

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
                mettre_a_jour_stats(joueur, monstres_battus, monstres_battus, degats_total_container['total'], duree_combat)

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