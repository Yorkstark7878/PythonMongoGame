class Personnage:
    def __init__(self, nom, atk, defn, pv):
        self.nom = nom
        self.atk = atk
        self.defn = defn
        self.pv = pv
        self.pv_max = pv

    def attaquer(self, cible):
        d = self.atk - cible.defn
        return max(1, d)

    def prendre_degats(self, d):
        self.pv -= d
        if self.pv < 0:
            self.pv = 0

    def est_vivant(self):
        return self.pv > 0

    def afficher_stats(self):
        return f"{self.nom} - ATK:{self.atk} DEF:{self.defn} PV:{self.pv}/{self.pv_max}"


class Monstre:
    def __init__(self, nom, atk, defn, pv):
        self.nom = nom
        self.atk = atk
        self.defn = defn
        self.pv = pv
        self.pv_max = pv

    def attaquer(self, cible):
        d = self.atk - cible.defn
        return max(1, d)

    def prendre_degats(self, d):
        self.pv -= d
        if self.pv < 0:
            self.pv = 0

    def est_vivant(self):
        return self.pv > 0

    def afficher_stats(self):
        return f"{self.nom} - ATK:{self.atk} DEF:{self.defn} PV:{self.pv}/{self.pv_max}"
