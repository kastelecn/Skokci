
class Igra():

    vstopno_zajec = 'VSTOPNO_ZAJEC'
    vstopno_lisica = 'VSTOPNO_LISICA'
    zmagovalno_zajec = 'ZMAGOVALNO_ZAJEC'
    zmagovalno_lisica = 'ZMAGOVALNO_LISICA'
    navadno = 'NAVADNO'
    zajci = 'ZAJCI'
    lisice = 'LISICE'
    lisica = 'LISICA'
    zajec = 'ZAJEC'
    polje = 'POLJE'
    cakajoci_zajec = 'CAKAJOCI_ZAJEC'
    cakajoca_lisica = 'CAKAJOCA_LISICA'


    povezave = [(0,1), (1,2), (2,3), (3,4), (4,5), (5,6), (6,7), (7,8), (8,9), (9,10), (10,11), (11,12), (12,13), (13,14),
                (14,15), (15,16), (16,17), (17,18), (18,19), (0, 19), (20,21), (21,22), (22,23), (23,24), (24,25), (25,26),
                (26,27), (20,27), (0,20), (4,21), (6,22), (10,24), (14,25), (16,26)]

    def __init__(self):
        self.na_potezi = Igra.lisice #zajci ali lisice
        self.lisice = [] #polja, kjer se nahajajo lisice
        self.zajci = [] #polja, kjer se nahajajo zajci
        self.igra_poteka = True


    def tip_polja(self, k):
        if k == 0 or k == 6:
            return Igra.vstopno_zajec
        if k == 10 or k == 16:
            return Igra.vstopno_lisica
        if k == 13:
            return Igra.zmagovalno_zajec
        if k == 3:
            return Igra.zmagovalno_lisica
        return Igra.navadno


    def spremeni_stanje(self, figura, polje):
        if self.igra_poteka:
            if figura[0] == Igra.zajec or figura[0] == Igra.cakajoci_zajec:
                self.zajci.append(polje)
                if figura[1] != None:
                    self.zajci.remove(figura[1])
                self.na_potezi = Igra.lisice
            if figura[0] == Igra.lisica or figura[0] == Igra.cakajoca_lisica:
                self.lisice.append(polje)
                if figura[1] != None:
                    self.lisice.remove(figura[1])
                self.na_potezi = Igra.zajci
            for i in self.ali_je_obkoljen(figura, polje):
                if i in self.zajci:
                    self.zajci.remove(i)
                if i in self.lisice:
                    self.lisice.remove(i)
            if self.ali_je_zmaga(figura, polje) != None:
                self.igra_poteka = False


    def veljavna_poteza(self, figura, polje):
        if polje in self.lisice or polje in self.zajci:
            return False
        if figura[0] == Igra.zajec:
            if ((figura[1], polje) in Igra.povezave) or ((polje, figura[1]) in Igra.povezave):
                return True
        if figura[0] == Igra.cakajoci_zajec and self.tip_polja(polje) == Igra.vstopno_zajec:
            return True

        if figura[0] == Igra.lisica:
            if ((figura[1], polje) in Igra.povezave) or ((polje, figura[1]) in Igra.povezave):
                return True
        if figura[0] == Igra.cakajoca_lisica and self.tip_polja(polje) == Igra.vstopno_lisica:
            return True

    def ali_je_obkoljen(self, figura, polje):
        obkoljeni = []
        for povezava in Igra.povezave:
            if polje in povezava:
                (x, y) = povezava
                if x == polje:
                    sosed = y
                if y == polje:
                    sosed = x
                #PREVERJAMO ČE JE LISICA OBKOLILA ZAJCA
                if (figura[0] == Igra.lisica or figura[0] == Igra.cakajoca_lisica) and sosed in self.zajci:
                    print('gledam')
                    je_kandidat = True
                    sosedi_nasprotnika = []
                    for naveza in Igra.povezave:
                        print(naveza)
                        (a,b) = naveza
                        if sosed in naveza:
                            if sosed == a:
                                sosedi_nasprotnika.append(b)

                            else:
                                sosedi_nasprotnika.append(a)
                    for element in sosedi_nasprotnika:
                        if element not in self.lisice:
                            je_kandidat = False
                        else:
                            print(element)
                    if je_kandidat:
                        obkoljeni.append(sosed)
                #PREVERJAMO ČE JE ZAJEC OBKOLIL LISICO
                if (figura[0] == Igra.zajec or figura[0] == Igra.cakajoci_zajec) and sosed in self.lisice:
                    print('gledam')
                    je_kandidat = True
                    sosedi_nasprotnika = []
                    for naveza in Igra.povezave:
                        (a,b) = naveza
                        print(naveza)
                        if sosed in naveza:
                            if sosed == a:
                                sosedi_nasprotnika.append(b)
                            else:
                                sosedi_nasprotnika.append(a)
                            print(sosedi_nasprotnika)
                    for element in sosedi_nasprotnika:
                        if element not in self.zajci:
                            je_kandidat = False
                    if je_kandidat:
                        obkoljeni.append(sosed)
        return obkoljeni

    def ali_je_zmaga(self, figura, polje):
        if figura[0] == Igra.lisica and self.tip_polja(polje) == Igra.zmagovalno_lisica:
            return Igra.lisice
        print(figura[0], self.tip_polja(polje))
        if figura[0] == Igra.zajec and self.tip_polja(polje) == Igra.zmagovalno_zajec:
            return Igra.zajci



    def mozna_polja(self, figura):
        if figura != None:
            za_pobarvat = []
            if figura[0] == self.lisica or figura[0] == self.zajec:
                for povezava in Igra.povezave:
                    if figura[1] in povezava:
                        (x,y) = povezava
                        if x == figura[1]:
                            if (y not in self.zajci) or (y not in self.lisice):
                                za_pobarvat.append(y)
                        else:
                            if (y not in self.zajci) or (y not in self.lisice):
                                za_pobarvat.append(x)
            if figura[0] == self.cakajoca_lisica:
                za_pobarvat.append(10)
                za_pobarvat.append(16)
            if figura[0] == self.cakajoci_zajec:
                za_pobarvat.append(0)
                za_pobarvat.append(6)
            return za_pobarvat
