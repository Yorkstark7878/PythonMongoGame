def afficher_boutique(pieces):
    """Affiche le catalogue de la boutique avec les pièces disponibles."""
    print("\n" + "="*50)
    print("Boutique d'items")
    print("="*50)
    print(f" Vous avez : {pieces} pièces\n")
    print("CATALOGUE :")
    print("1. Potion de soin (+50 PV) coûte 10 pièces")
    print("2. Grande potion (restaure tout) coûte 25 pièces")
    print("3. Boost d'attaque (+5 ATK/vague) coûte 15 pièces")
    print("4. Bouclier (+3 DEF permanent) coûte 20 pièces")
    print("5. Quitter la boutique d'items")
    print("="*50)

def acheter_item(choix, equipe, pieces, buffs_temporaires):
    if choix == 1:  # Potion de soin
        cout = 10
        if pieces >= cout:
            # Soigner tous les personnages vivants de 50 PV
            vivants = [p for p in equipe if p.est_vivant()]
            if not vivants:
                return pieces, "Aucun personnage à soigner !", buffs_temporaires
            
            for p in vivants:
                p.pv = min(p.pv + 50, p.pv_max)
            
            pieces -= cout
            return pieces, "Potion de soin achetée ! +50 PV pour l'équipe.", buffs_temporaires
        else:
            return pieces, "Pas assez de pièces !", buffs_temporaires
    
    elif choix == 2:  # Grande potion
        cout = 25
        if pieces >= cout:
            vivants = [p for p in equipe if p.est_vivant()]
            if not vivants:
                return pieces, "Aucun personnage à soigner !", buffs_temporaires
            
            for p in vivants:
                p.pv = p.pv_max
            
            pieces -= cout
            return pieces, "Grande potion achetée ! PV restaurés à 100% !", buffs_temporaires
        else:
            return pieces, "Pas assez de pièces !", buffs_temporaires
    
    elif choix == 3:  # Boost d'attaque temporaire
        cout = 15
        if pieces >= cout:
            buffs_temporaires['boost_atk'] = True
            pieces -= cout
            return pieces, "Boost d'attaque acheté ! +5 ATK pour la prochaine vague.", buffs_temporaires
        else:
            return pieces, "Pas assez de pièces !", buffs_temporaires
    
    elif choix == 4:  # Bouclier permanent
        cout = 20
        if pieces >= cout:
            for p in equipe:
                p.defn += 3
            pieces -= cout
            return pieces, "Bouclier acheté ! +3 DEF permanent pour toute l'équipe.", buffs_temporaires
        else:
            return pieces, "Pas assez de pièces !", buffs_temporaires
    
    elif choix == 5:  # Quitter
        return pieces, "À la prochaine !", buffs_temporaires
    
    else:
        return pieces, "Choix invalide.", buffs_temporaires

def gerer_boutique(equipe, pieces, buffs_temporaires):
    """
    Boucle principale de la boutique.
    Retourne (pieces_restantes, buffs_temporaires_mis_a_jour)
    """
    while True:
        afficher_boutique(pieces)
        
        try:
            choix = int(input("\nVotre choix : "))
            
            if choix == 5:
                print("Vous quittez la boutique.")
                return pieces, buffs_temporaires
            
            pieces, message, buffs_temporaires = acheter_item(choix, equipe, pieces, buffs_temporaires)
            print(f"\n{message}")
            
            if choix == 5:
                return pieces, buffs_temporaires
            
            input("\nAppuyez sur Entrée pour continuer...")
        
        except ValueError:
            print("\nEntrée invalide.")
            input("\nAppuyez sur Entrée pour continuer...")