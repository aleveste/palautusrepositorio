import unittest
from unittest.mock import Mock, ANY
from kauppa import Kauppa
from viitegeneraattori import Viitegeneraattori
from varasto import Varasto
from tuote import Tuote

class TestKauppa(unittest.TestCase):
    def setUp(self):
        self.pankki_mock = Mock()
        self.viitegeneraattori_mock = Mock()
        self.viitegeneraattori_mock.uusi.side_effect = [42, 43, 44]
        self.varasto_mock = Mock()

        def varasto_saldo(tuote_id):
            tuotteet = {1: 10, 2: 5, 3: 0}
            return tuotteet.get(tuote_id, 0)

        def varasto_hae_tuote(tuote_id):
            tuotteet = {
                1: Tuote(1, "maito", 5),
                2: Tuote(2, "leipä", 3),
                3: Tuote(3, "juusto", 10)
            }
            return tuotteet.get(tuote_id, None)

        self.varasto_mock.saldo.side_effect = varasto_saldo
        self.varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

        self.kauppa = Kauppa(self.varasto_mock, self.pankki_mock, self.viitegeneraattori_mock)

    def test_ostoksen_paaytyttya_pankin_metodia_tilisiirto_kutsutaan(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called()

    def test_tilisiirto_oikeilla_parametreilla(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", ANY, 5)

    def test_kaksi_eri_tuotetta_tilisiirto_oikeilla_parametreilla(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(2)
        self.kauppa.tilimaksu("maija", "54321")

        self.pankki_mock.tilisiirto.assert_called_with("maija", 42, "54321", ANY, 8)

    def test_kaksi_samaa_tuotetta_tilisiirto_oikeilla_parametreilla(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("jussi", "67890")

        self.pankki_mock.tilisiirto.assert_called_with("jussi", 42, "67890", ANY, 10)

    def test_tuote_jota_on_ja_tuote_joka_on_loppu(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)  # On varastossa
        self.kauppa.lisaa_koriin(3)  # Loppu varastosta
        self.kauppa.tilimaksu("anna", "11111")

        self.pankki_mock.tilisiirto.assert_called_with("anna", 42, "11111", ANY, 5)
        
    def test_aloita_asiointi_nollaa_edellisen_ostoksen_tiedot(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        self.kauppa.aloita_asiointi()  # Nollaa ostoskori
        self.kauppa.lisaa_koriin(2)  # Uusi tuote
        self.kauppa.tilimaksu("maija", "54321")

        # Varmistetaan, että toinen tilisiirto käyttää vain toisen ostoksen hintaa
        self.pankki_mock.tilisiirto.assert_called_with("maija", 43, "54321", ANY, 3)

    def test_uusi_viitenumero_jokaiselle_maksutapahtumalle(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(2)
        self.kauppa.tilimaksu("maija", "54321")

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("anna", "11111")

        # Varmistetaan, että viitegeneraattorin uusi-metodia kutsutaan kolme kertaa
        self.assertEqual(self.viitegeneraattori_mock.uusi.call_count, 3)

        # Varmistetaan, että pankin tilisiirto käyttää oikeita viitenumeroita
        self.pankki_mock.tilisiirto.assert_any_call("pekka", 42, "12345", ANY, 5)
        self.pankki_mock.tilisiirto.assert_any_call("maija", 43, "54321", ANY, 3)
        self.pankki_mock.tilisiirto.assert_any_call("anna", 44, "11111", ANY, 5)

