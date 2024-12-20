class KiviPaperiSakset:
    def pelaa(self):
        tuomari = self._tuomari()
        ekan_siirto = self._ensimmaisen_siirto()

        while self._onko_ok_siirto(ekan_siirto):
            tokan_siirto = self._toisen_siirto(ekan_siirto)
            tuomari.kirjaa_siirto(ekan_siirto, tokan_siirto)
            print(tuomari)

            ekan_siirto = self._ensimmaisen_siirto()

        print("Kiitos!")
        print(tuomari)

    def _ensimmaisen_siirto(self):
        return input("Ensimmäisen pelaajan siirto: ")
    
    # tämän metodin toteutus vaihtelee eri pelityypeissä
    def _toisen_siirto(self, ensimmaisen_siirto):
        raise Exception("Tämä metodi pitää korvata aliluokassa")

    def _onko_ok_siirto(self, siirto):
        return siirto == "k" or siirto == "p" or siirto == "s"

    def _tuomari(self):
        from tuomari import Tuomari
        return Tuomari()