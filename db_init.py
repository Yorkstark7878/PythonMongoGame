from pymongo import MongoClient

def init_database():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["python_game"]

    db.personnages.drop()
    db.monstres.drop()
    db.scores.drop()
    db.statistiques.drop()  

    pnj = [
        {"nom": "Guerrier", "atk": 15, "defn": 10, "pv": 100},
        {"nom": "Mage", "atk": 20, "defn": 5, "pv": 80},
        {"nom": "Archer", "atk": 18, "defn": 7, "pv": 90},
        {"nom": "Voleur", "atk": 22, "defn": 8, "pv": 85},
        {"nom": "Paladin", "atk": 14, "defn": 12, "pv": 110},
        {"nom": "Sorcier", "atk": 25, "defn": 3, "pv": 70},
        {"nom": "Chevalier", "atk": 17, "defn": 15, "pv": 120},
        {"nom": "Moine", "atk": 19, "defn": 9, "pv": 95},
        {"nom": "Berserker", "atk": 23, "defn": 6, "pv": 105},
        {"nom": "Chasseur", "atk": 16, "defn": 11, "pv": 100},
    ]

    monstres = [
        {"nom": "Gobelin", "atk": 10, "defn": 5, "pv": 50},
        {"nom": "Orc", "atk": 20, "defn": 8, "pv": 120},
        {"nom": "Dragon", "atk": 35, "defn": 20, "pv": 300},
        {"nom": "Zombie", "atk": 12, "defn": 6, "pv": 70},
        {"nom": "Troll", "atk": 25, "defn": 15, "pv": 200},
        {"nom": "Spectre", "atk": 18, "defn": 10, "pv": 100},
        {"nom": "Golem", "atk": 30, "defn": 25, "pv": 250},
        {"nom": "Vampire", "atk": 22, "defn": 12, "pv": 150},
        {"nom": "Loup-garou", "atk": 28, "defn": 18, "pv": 180},
        {"nom": "Squelette", "atk": 15, "defn": 7, "pv": 90},
    ]

    db.personnages.insert_many(pnj)
    db.monstres.insert_many(monstres)

    db.scores.create_index("joueur")    
    db.statistiques.create_index("joueur")

    print("DB prête.")
    print(len(pnj), "persos ajoutés")
    print(len(monstres), "monstres ajoutés")
    print("Collections scores et statistiques créées")

if __name__ == "__main__":
    init_database()
