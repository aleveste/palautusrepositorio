class IntJoukko:
    KAPASITEETTI = 5
    OLETUSKASVATUS = 5

    def __init__(self, kapasiteetti=None, kasvatuskoko=None):
        self.kapasiteetti = kapasiteetti if kapasiteetti is not None else self.KAPASITEETTI
        self.kasvatuskoko = kasvatuskoko if kasvatuskoko is not None else self.OLETUSKASVATUS

        if not isinstance(self.kapasiteetti, int) or self.kapasiteetti < 0:
            raise ValueError("Virheellinen kapasiteetti")
        if not isinstance(self.kasvatuskoko, int) or self.kasvatuskoko < 0:
            raise ValueError("Virheellinen kasvatuskoko")

        self.ljono = [0] * self.kapasiteetti
        self.alkioiden_lkm = 0

    def kuuluu(self, n):
        """Tarkistaa, kuuluuko luku joukkoon."""
        return n in self.ljono[:self.alkioiden_lkm]

    def lisaa(self, n):
        """Lisää luvun joukkoon, jos se ei jo kuulu joukkoon."""
        if self.kuuluu(n):
            return False
        if self.alkioiden_lkm >= len(self.ljono):
            self._laajenna()
        self.ljono[self.alkioiden_lkm] = n
        self.alkioiden_lkm += 1
        return True

    def poista(self, n):
        """Poistaa luvun joukosta, jos se kuuluu joukkoon."""
        if n not in self.ljono[:self.alkioiden_lkm]:
            return False
        index = self.ljono.index(n)
        self._siirra_vasemmalle(index)
        self.alkioiden_lkm -= 1
        return True

    def kopioi_lista(self, alkuperainen, kohde):
        """Kopioi elementit alkuperäisestä listasta kohdelistaan."""
        for i in range(len(alkuperainen)):
            kohde[i] = alkuperainen[i]

    def to_int_list(self):
        """Palauttaa joukon listana."""
        return self.ljono[:self.alkioiden_lkm]

    def mahtavuus(self):
        """Palauttaa joukossa olevien alkioiden lukumäärän."""
        return self.alkioiden_lkm

    @staticmethod
    def yhdiste(a, b):
        """Palauttaa kahden joukon yhdisteen."""
        x = IntJoukko()
        for n in a.to_int_list():
            x.lisaa(n)
        for n in b.to_int_list():
            x.lisaa(n)
        return x

    @staticmethod
    def leikkaus(a, b):
        """Palauttaa kahden joukon leikkauksen."""
        y = IntJoukko()
        for n in a.to_int_list():
            if b.kuuluu(n):
                y.lisaa(n)
        return y

    @staticmethod
    def erotus(a, b):
        """Palauttaa kahden joukon erotuksen."""
        z = IntJoukko()
        for n in a.to_int_list():
            z.lisaa(n)
        for n in b.to_int_list():
            z.poista(n)
        return z

    def _laajenna(self):
        """Laajentaa taulukkoa, kun se on täynnä."""
        uusi_koko = len(self.ljono) + self.kasvatuskoko
        uusi_lista = [0] * uusi_koko
        self.kopioi_lista(self.ljono, uusi_lista)
        self.ljono = uusi_lista

    def _siirra_vasemmalle(self, aloituskohta):
        """Siirtää taulukon elementtejä vasemmalle poistamisen jälkeen."""
        for i in range(aloituskohta, self.alkioiden_lkm - 1):
            self.ljono[i] = self.ljono[i + 1]
        self.ljono[self.alkioiden_lkm - 1] = 0

    def __str__(self):
        """Palauttaa joukon merkkijonoesityksen."""
        if self.alkioiden_lkm == 0:
            return "{}"
        return "{" + ", ".join(map(str, self.ljono[:self.alkioiden_lkm])) + "}"

