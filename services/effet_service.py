import random

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