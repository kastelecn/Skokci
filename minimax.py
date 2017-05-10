import logging

from Igra import *


# Algoritem minimax

class Minimax:
    # Algoritem minimax predstavimo z objektom, ki hrani stanje igre in
    # algoritma, nima pa dostopa do GUI (ker ga ne sme uporabljati, saj deluje
    # v drugem vlaknu kot tkinter).

    def __init__(self, globina):
        self.globina = globina  # do katere globine iščemo?
        self.prekinitev = False # ali moramo končati?
        self.igra = None # objekt, ki opisuje igro (ga dobimo kasneje)
        self.jaz = None  # katerega igralca igramo (podatek dobimo kasneje)
        self.poteza = (None, None) # sem napišemo potezo, ko jo najdemo
        self.igra = Igra()


    def prekini(self):
        # Metoda, ki jo pokliče GUI, če je treba nehati razmišljati, ker je uporabnik zaprl okno ali izbral novo igro.
        self.prekinitev = True

    def izracunaj_potezo(self, igra):
        # Izračuna potezo za trenutno stanje dane igre
        # To metodo pokliÄčemo iz vzporednega vlakna
        self.igra = igra
        self.prekinitev = False # Glavno vlakno bo to nastvilo na True, če moramo nehati
        self.jaz = self.igra.na_potezi
        self.poteza = None, None # Sem napišemo potezo, ko jo najdemo. Poteza je oblike (figura, polje)
        #  kje je figura oblike (kdo, kje je zdaj). figura[1] je None, če je na začetnih koordinatah
        # Poženemo minimax
        (figura, polje, vrednost) = self.minimax(self.globina, True)
        self.jaz = None
        self.igra = None
        if not self.prekinitev:
            # Potezo izvedemo v primeru, da nismo bili prekinjeni
            logging.debug("minimax: figura {0}, polje{1},  vrednost {2}".format(figura, polje, vrednost))
            self.poteza = figura, polje

    # Vrednosti igre
    ZMAGA = 100000
    NESKONCNO = ZMAGA + 1 # Več kot zmaga

    #kje se figure premikajo (seznam idjev povezanih polj. Zadnje polje v seznamu je vedno zmagovalno)
    POTI_ZA_ZAJCE = [[3,4,5,6,7,8,9,10,11,12,13], [3,2,1,0,19,18,17,16,15,14,13], [3,4,21,22,23,24,25,14,13], [3,4,5,6,22,23,24,10,11,12,13],
                     [3,2,1,0,20,27,26,25,14,13], [3,2,1,0,20,27,26,16,15,14,13], [6,7,8,9,10, 24,25,14,13], [0,19,18,17,16,26,25,14,13]]
    POTI_ZA_LISICE = [[13,12,11,10,9,8,7,6,5,4,3], [13,14,15,16,17,18,19,0,1,2,3], [13,12,11,10,24,23,22,21,4,3], [13,14,15,16,26,27,20,21,4,3],
                      [13,12,11,10,24,23,22,21,4,3], [13,12,11,10,24,23,22,6,5,4,3], [16,17,18,19,0,20,21,4,3], [10,9,8,7,6,22,21,4,3]]
    ZGORNJA_VRSTA_IDJI = [i for i in range(10, 17)]
    SPODNJA_VRSTA_IDJI = [i for i in range(7)]


    def vrednost_pozicije(self):
        #vrednost pozicije v danem trenutku
        vrednost = 0
        #če je igralec lisica:
        if self.jaz == Igra.lisice:
            #če bomo imeli več kot 3 lisice na plošči vrednost malo zmanjšamo, da se ne zacikla
            if len(self.igra.lisice) > 3:
                vrednost -= 100 * len(self.igra.lisice)

            #vstopna polja nasprotnika so veliko vredna
            if (0 or 6) in self.igra.lisice:
                vrednost += 500

            #poskrbimo da bodo nekatere figure branile cilj:
            napadalni_zajci = 0
            for i in self.igra.zajci:
                if i in [11,12,13,14,15,24,25,26]:
                    napadalni_zajci += 1
            branilne_lisice = 0
            for i in self.igra.lisice:
                if i in [12,13,14,25]:
                    branilne_lisice +=1
            vrednost += (branilne_lisice - napadalni_zajci ) * 150

            #obravnavamo posebno situacijo blizu konca
            zasedenost = ''
            for i in Minimax.SPODNJA_VRSTA_IDJI:
                if i in self.igra.zajci:
                    zasedenost += 'Z'
                elif i in self.igra.lisice:
                    zasedenost += 'L'
                else:
                    zasedenost += 'N'
            if 'LZNL' in zasedenost:
                vrednost += 20000
            if 'LNZL' in zasedenost:
                vrednost += 20000

            #pogledamo kako blizu cilja smo
            for i in self.igra.lisice:
                dolzine = []
                slabe_dolzine = []

                for pot in Minimax.POTI_ZA_LISICE:
                    if i in pot:
                        indeks = pot.index(i)
                        if pot[indeks+1] not in self.igra.zajci: #pogledamo če bomo potem lahko nadaljevali
                            dolzine.append(len(pot[indeks:]))
                            if len(pot) > indeks +2 and pot[indeks + 2]  in self.igra.zajci: #če smo blizu nasprotnikom ni najbolje
                                vrednost -= 50
                        else:
                            slabe_dolzine.append(len(pot[indeks:]))

                if len(dolzine) > 0:
                    vrednost += Minimax.ZMAGA // 10 - min(dolzine) * 200
                elif len(slabe_dolzine) > 0:
                    vrednost += Minimax.ZMAGA // 10 - min(slabe_dolzine) * 250

                #poglejmo še če smo koga obkolili
                (figura, polje) = ((Igra.lisica, i), i)
                if self.igra.ali_je_obkoljen(figura, polje):
                    vrednost += 400000

            #pogledamo še če je nasprotnik obkoljen
            for i in self.igra.zajci:
                (figura, polje) = ((Igra.zajec, i), i)
                if self.igra.ali_je_obkoljen(figura, polje):
                    vrednost -= 400000

        #če je igralec zajec
        if self.jaz == Igra.zajci:
            #Poskrbimo da ne dajemo preveč figur ven
            if len(self.igra.zajci) > 3:
                vrednost -= 100 * len(self.igra.zajci)
            #vstopna polja nasprotnika so veliko vredna
            if (16 or 10) in self.igra.zajci:
                vrednost += 500

            # poskrbimo da bodo nekatere figure branile cilj:
            napadalne_lisice = 0
            for i in self.igra.lisice:
                if i in [1,2,3,4,5,21,22,20]:
                    napadalne_lisice += 1
            branilni_zajci = 0
            for i in self.igra.zajci:
                if i in [2,3,4,21]:
                    branilni_zajci += 1
            vrednost += (branilni_zajci - napadalne_lisice) * 150

            #pogledamo poseben primer ob koncu igre
            zasedenost = ''
            for i in Minimax.ZGORNJA_VRSTA_IDJI:
                if i in self.igra.zajci:
                    zasedenost += 'Z'
                elif i in self.igra.lisice:
                    zasedenost += 'L'
                else:
                    zasedenost += 'N'
            if 'ZNLZ' in zasedenost:
                vrednost += 20000
            if 'ZLNZ' in zasedenost:
                vrednost += 20000

            #koliko nam manjka še do cilja
            for i in self.igra.zajci:
                dolzine = []
                slabe_dolzine = []
                for pot in Minimax.POTI_ZA_ZAJCE:
                    if i in pot:
                        indeks = pot.index(i)
                        if pot[indeks + 1] not in self.igra.lisice:
                            dolzine.append(len(pot[indeks:]))
                            if len(pot) > indeks +2 and pot[indeks + 2] in self.igra.zajci:
                                vrednost -= 50

                        else:
                            slabe_dolzine.append(len(pot[indeks:]))
                if len(dolzine) > 0:
                    vrednost += Minimax.ZMAGA // 10 - min(dolzine) * 200
                elif len(slabe_dolzine) > 0:
                    vrednost += Minimax.ZMAGA // 10 - min(slabe_dolzine) * 250

                #preverimo če smo koga obkolili
                (figura, polje) = ((Igra.zajec, i), i)

                if self.igra.ali_je_obkoljen(figura, polje):
                    vrednost += 400000

            #enako pogledamo se za nasprotnika
            for i in self.igra.lisice:
                (figura, polje) = ((Igra.lisica, i), i)
                if self.igra.ali_je_obkoljen(figura, polje):
                    vrednost += 400000


        return(vrednost)




    def minimax(self, globina, maksimiziramo):
        if self.prekinitev:
            logging.debug ("Minimax prekinja, globina = {0}".format(globina))
            return (None, None, 0)
        zmagovalec = self.igra.stanje_igre()
        if zmagovalec in (Igra.lisice, Igra.zajci):
            # Igre je konec, vrnemo njeno vrednost
            if zmagovalec == self.jaz:
                return (None, None, Minimax.ZMAGA)
            elif zmagovalec == nasprotnik(self.jaz):
                return (None, None, -Minimax.ZMAGA)
        elif zmagovalec == None:
            # Igre ni konec
            if globina == 0:
                return (None, None, self.vrednost_pozicije())
            else:
                # Naredimo eno stopnjo minimax
                if maksimiziramo:
                    # Maksimiziramo
                    najboljsa_poteza = (None, None)

                    vrednost_najboljse = -Minimax.NESKONCNO
                    for (figura, polja) in self.igra.veljavne_poteze()[self.igra.na_potezi]:
                        #za vsako figuro mora preveriti vrednost vseh možnih polj
                        for polje in polja:
                            r = self.igra.povleci_potezo(figura, polje)
                            assert (r != (None, None)), "minimax je hotel poveči neveljavno potezo {0}".format((figura, polje))
                            vrednost = self.minimax(globina - 1, not maksimiziramo)[2]
                            self.igra.razveljavi()
                            if vrednost > vrednost_najboljse:
                                vrednost_najboljse = vrednost
                                najboljsa_poteza = (figura, polje)
                else:
                    # Minimiziramo
                    najboljsa_poteza = (None, None)
                    vrednost_najboljse = Minimax.NESKONCNO
                    for (figura, polja) in self.igra.veljavne_poteze()[self.igra.na_potezi]:
                        for polje in polja:
                            self.igra.povleci_potezo(figura, polje)
                            vrednost = self.minimax(globina - 1, not maksimiziramo)[2]
                            self.igra.razveljavi()
                            if vrednost < vrednost_najboljse:
                                vrednost_najboljse = vrednost
                                najboljsa_poteza = (figura, polje)

                assert (najboljsa_poteza != (None, None)), "minimax: izračunana poteza je None, None"
                return (najboljsa_poteza[0], najboljsa_poteza[1], vrednost_najboljse)
        else:
            assert False, "minimax: nedefinirano stanje igre"
