from utils import (
    afficher_menu_principal,
    afficher_classement,
    afficher_statistiques,
    valider_entree_numerique,
    valider_entree_texte
)
from game import creer_equipe, jouer

def main():
    while True:
        afficher_menu_principal()
        choix = valider_entree_numerique("Votre choix: ", 1, 4)

        if choix == 1:
            joueur = valider_entree_texte("Votre nom: ")
            print(f"\nBienvenue {joueur} !\n")
            equipe = creer_equipe()
            jouer(joueur, equipe)
            afficher_classement()

        elif choix == 2:
            afficher_classement()

        elif choix == 3:
            joueur = valider_entree_texte("Entrez votre nom : ")
            afficher_statistiques(joueur)

        elif choix == 4:
            print("\nMerci d'avoir joué !")
            break

if __name__ == "__main__":
    main()
