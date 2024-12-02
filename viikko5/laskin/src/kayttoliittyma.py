from enum import Enum
from tkinter import ttk, constants, StringVar


from enum import Enum
from tkinter import ttk, constants, StringVar


class Komento(Enum):
    SUMMA = 1
    EROTUS = 2
    NOLLAUS = 3
    KUMOA = 4


class Kayttoliittyma:
    def __init__(self, sovelluslogiikka, root):
        self._sovelluslogiikka = sovelluslogiikka
        self._root = root
        self._edellinen_komento = None  # Muistaa edellisen suoritetun komennon

        # Komentojen määrittely
        self._komennot = {
            Komento.SUMMA: Summa(self._sovelluslogiikka, self._lue_syote),
            Komento.EROTUS: Erotus(self._sovelluslogiikka, self._lue_syote),
            Komento.NOLLAUS: Nollaus(self._sovelluslogiikka)
        }

    def kaynnista(self):
        self._arvo_var = StringVar()
        self._arvo_var.set(self._sovelluslogiikka.arvo())
        self._syote_kentta = ttk.Entry(master=self._root)

        tulos_teksti = ttk.Label(textvariable=self._arvo_var)

        summa_painike = ttk.Button(
            master=self._root,
            text="Summa",
            command=lambda: self._suorita_komento(Komento.SUMMA)
        )

        erotus_painike = ttk.Button(
            master=self._root,
            text="Erotus",
            command=lambda: self._suorita_komento(Komento.EROTUS)
        )

        self._nollaus_painike = ttk.Button(
            master=self._root,
            text="Nollaus",
            state=constants.DISABLED,
            command=lambda: self._suorita_komento(Komento.NOLLAUS)
        )

        self._kumoa_painike = ttk.Button(
            master=self._root,
            text="Kumoa",
            state=constants.DISABLED,
            command=lambda: self._suorita_komento(Komento.KUMOA)
        )

        tulos_teksti.grid(columnspan=4)
        self._syote_kentta.grid(columnspan=4, sticky=(constants.E, constants.W))
        summa_painike.grid(row=2, column=0)
        erotus_painike.grid(row=2, column=1)
        self._nollaus_painike.grid(row=2, column=2)
        self._kumoa_painike.grid(row=2, column=3)

    def _lue_syote(self):
        """Lukee syötteen tekstikentästä."""
        try:
            return int(self._syote_kentta.get())
        except ValueError:
            return 0

    def _suorita_komento(self, komento):
        """Suorittaa annetun komennon."""
        if komento == Komento.KUMOA and self._edellinen_komento:
            self._edellinen_komento.kumoa()
            self._edellinen_komento = None  # Kumoa voi suorittaa vain kerran
            self._kumoa_painike["state"] = constants.DISABLED
        elif komento in self._komennot:
            komento_olio = self._komennot[komento]
            komento_olio.suorita()
            self._edellinen_komento = komento_olio  # Tallenna viimeisin komento
            self._kumoa_painike["state"] = constants.NORMAL

        if self._sovelluslogiikka.arvo() == 0:
            self._nollaus_painike["state"] = constants.DISABLED
        else:
            self._nollaus_painike["state"] = constants.NORMAL

        self._syote_kentta.delete(0, constants.END)
        self._arvo_var.set(self._sovelluslogiikka.arvo())


# Komentoluokat
class Summa:
    def __init__(self, sovelluslogiikka, syotteen_lukija):
        self._sovelluslogiikka = sovelluslogiikka
        self._syotteen_lukija = syotteen_lukija
        self._edellinen_arvo = None

    def suorita(self):
        """Suorittaa summan lisäämällä annetun arvon."""
        self._edellinen_arvo = self._sovelluslogiikka.arvo()
        arvo = self._syotteen_lukija()
        self._sovelluslogiikka.plus(arvo)

    def kumoa(self):
        """Kumoaa summan laskemisen."""
        if self._edellinen_arvo is not None:
            self._sovelluslogiikka.aseta_arvo(self._edellinen_arvo)


class Erotus:
    def __init__(self, sovelluslogiikka, syotteen_lukija):
        self._sovelluslogiikka = sovelluslogiikka
        self._syotteen_lukija = syotteen_lukija
        self._edellinen_arvo = None

    def suorita(self):
        """Suorittaa erotuksen vähentämällä annetun arvon."""
        self._edellinen_arvo = self._sovelluslogiikka.arvo()
        arvo = self._syotteen_lukija()
        self._sovelluslogiikka.miinus(arvo)

    def kumoa(self):
        """Kumoaa erotuksen laskemisen."""
        if self._edellinen_arvo is not None:
            self._sovelluslogiikka.aseta_arvo(self._edellinen_arvo)


class Nollaus:
    def __init__(self, sovelluslogiikka):
        self._sovelluslogiikka = sovelluslogiikka
        self._edellinen_arvo = None

    def suorita(self):
        """Nollaa laskimen arvon."""
        self._edellinen_arvo = self._sovelluslogiikka.arvo()
        self._sovelluslogiikka.nollaa()

    def kumoa(self):
        """Kumoaa nollauksen."""
        if self._edellinen_arvo is not None:
            self._sovelluslogiikka.aseta_arvo(self._edellinen_arvo)
