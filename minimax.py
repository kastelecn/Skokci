import logging

from Igra import *

razdalje_zajci = {14: 1, 12: 1, 15: 2, 25: 2, 11: 2, 16: 3, 26: 3, 24: 3, 10: 3, 17: 4,
                  9: 4}  # razdalja do zmagovalnega polje ki jih gledajo zajci
razdalje_lisice = {2: 1, 4: 1, 1: 2, 5: 2, 21: 2, 0: 3, 6: 3, 20: 3, 22: 3, 19: 4, 7: 4}
######################################################################
## Algoritem minimax

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
        """Metoda, ki jo pokliče GUI, Äe je treba nehati razmišljati, ker
           je uporabnik zaprl okno ali izbral novo igro."""
        self.prekinitev = True

    def izracunaj_potezo(self, igra):
        """IzraÄunaj potezo za trenutno stanje dane igre."""
        # To metodo pokliÄemo iz vzporednega vlakna
        self.igra = igra
        self.prekinitev = False # Glavno vlakno bo to nastvilo na True, Äe moramo nehati
        self.jaz = self.igra.na_potezi
        self.poteza = None, None # Sem napiĹĄemo potezo, ko jo najdemo
        # PoĹženemo minimax
        (figura, polje, vrednost) = self.minimax(self.globina, True)
        self.jaz = None
        self.igra = None
        if not self.prekinitev:
            # Potezo izvedemo v primeru, da nismo bili prekinjeni
            logging.debug("minimax: figura {0}, polje{1},  vrednost {2}".format(figura, polje, vrednost))
            self.poteza = figura, polje

    # Vrednosti igre
    ZMAGA = 100000 # Mora biti vsaj 10^5
    NESKONCNO = ZMAGA + 1 # Več kot zmaga

    #kje se figure premikajo
    POTI_ZA_ZAJCE = [[3,4,5,6,7,8,9,10,11,12,13], [3,2,1,0,19,18,17,16,15,14,13], [3,4,21,22,23,24,25,14,13], [3,4,5,6,22,23,24,10,11,12,13],
                     [3,2,1,0,20,27,26,25,14,13], [3,2,1,0,20,27,26,16,15,14,13], [6,7,8,9,10, 24,25,14,13], [0,19,18,17,16,26,25,14,13]]
    POTI_ZA_LISICE = [[13,12,11,10,9,8,7,6,5,4,3], [13,14,15,16,17,18,19,0,1,2,3], [13,12,11,10,24,23,22,21,4,3], [13,14,15,16,26,27,20,21,4,3],
                      [13,12,11,10,24,23,22,21,4,3], [13,12,11,10,24,23,22,6,5,4,3], [16,17,18,19,0,20,21,4,3], [10,9,8,7,6,22,21,4,3]]


    def vrednost_pozicije(self):
        #vrednost pozicije v danem trenutku
        vrednost = 0
        #če je igralec lisica:
        if self.jaz == Igra.lisice:
            #če bomo imeli več kot 3 lisice na plošči vrednost malo zmanjšamo, da se ne zacikla
            if len(self.igra.lisice) > 3:
                vrednost -= 100 * len(self.igra.lisice)

            #poskrbimo da bodo figure, ki branijo cilj nasprotnikov:
            napadalni_zajci = 0
            for i in self.igra.zajci:
                if i in [11,12,13,14,15,24,25,26]:
                    napadalni_zajci += 1
            branilne_lisice = 0
            for i in self.igra.lisice:
                if i in [12,13,14,25]:
                    branilne_lisice +=1
            vrednost += (branilne_lisice - napadalni_zajci ) * 100
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
                    vrednost += Minimax.ZMAGA // 100 - min(dolzine) * 50
                elif len(slabe_dolzine) > 0:
                    vrednost += Minimax.ZMAGA // 100 - min(slabe_dolzine) * 90

                #poglejmo še če sm koga obkolili
                (figura, polje) = ((Igra.lisica, i), i)
                if self.igra.ali_je_obkoljen(figura, polje):
                    vrednost += 40000


            for i in self.igra.zajci:
                dolzine = []
                slabe_dolzine = []
                for pot in Minimax.POTI_ZA_ZAJCE:
                    if i in pot:
                        indeks = pot.index(i)
                        if pot[indeks+1] not in self.igra.lisice:
                            dolzine.append(len(pot[indeks:]))
                            if len(pot) > indeks +2 and pot[indeks + 2] in self.igra.lisice:
                                vrednost += 50

                        else:
                            slabe_dolzine.append(len(pot[indeks:]))
                if len(dolzine) > 0:
                    vrednost -= Minimax.ZMAGA // 100 - min(dolzine) * 50
                elif len(slabe_dolzine) > 0:
                    vrednost -= Minimax.ZMAGA // 100 - min(slabe_dolzine) *90

                (figura, polje) = ((Igra.zajec, i), i)
                if self.igra.ali_je_obkoljen(figura, polje):
                    vrednost -= 40000

        if self.jaz == Igra.zajci:
            if len(self.igra.zajci) > 3:
                vrednost -= 100 * len(self.igra.zajci)
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
                    vrednost += Minimax.ZMAGA // 100 - min(dolzine) * 50
                elif len(slabe_dolzine) > 0:
                    vrednost += Minimax.ZMAGA // 100 - min(slabe_dolzine) * 90
                (figura, polje) = ((Igra.zajec, i), i)
                if self.igra.ali_je_obkoljen(figura, polje):
                    vrednost += 4000

            for i in self.igra.lisice:
                dolzine = []
                for pot in Minimax.POTI_ZA_LISICE:
                    if i in pot:
                        indeks = pot.index(i)
                        if pot[indeks + 1] not in self.igra.zajci:
                            dolzine.append(len(pot[indeks:]))
                            if len(pot) > indeks +2 and pot[indeks + 2] in self.igra.lisice:
                                vrednost += 50

                            if len(pot) > indeks +2 and pot[indeks + 2] in self.igra.zajci:
                                vrednost += 50

                        else:
                            slabe_dolzine.append(len(pot[indeks:]))
                if len(dolzine) > 0:
                    vrednost -= Minimax.ZMAGA // 100 - min(dolzine) * 50
                elif len(slabe_dolzine) > 0:
                    vrednost -= Minimax.ZMAGA // 100 - min(slabe_dolzine) * 90
                (figura, polje) = ((Igra.lisica, i), i)
                if self.igra.ali_je_obkoljen(figura, polje):
                    vrednost += 40000


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
            print(self.vrednost_pozicije())
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
                            print ("minimax: poteza {0}, {1} v poziciji:\n{2}".format(figura, polje, (self.igra.zajci, self.igra.lisice)))
                            r = self.igra.povleci_potezo(figura, polje)
                            assert (r is not None), "minimax je hotel poveči nevejavno potezo {0}".format((figura, polje))
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
