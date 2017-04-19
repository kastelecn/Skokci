

class Polje():
    def __init__(self, canvas, id_polja, koordinate):
        self.canvas = canvas 
        self.id_polja = id_polja
        self.koordinate = koordinate
        self.zasedeno = False
        self.sosedi = []
        self.namen = 'navadno' #lahko je se vstopno_a, vstopno_b ali zmagovalec_a, zmagovalec_b

    def __repr__(self):
        return ('Id polja: {}, koordinate: {}, sosedi: {}, namen: {}, zasedenost:{}'.format(self.id_polja, self.koordinate, self.sosedi, self.namen, self.zasedeno))

    def najdi_polje_z_idjem(self, id, seznam_polj):
        for polje in seznam_polj:
            if id == polje.id_polja:
                return polje
        

def sredisce(lst):
    """Središče krogca na Canvasu z danim bounding box."""
    (x1, y1, x2, y2) = lst
    return ((x1+x2)/2, (y1+y2)/2)
    


class Figura():
    def __init__(self, canvas, id_figure, koordinate_figure, ekipa):
        self.canvas = canvas
        self.id_figure = id_figure
        self.koordinate_figure = koordinate_figure  #polozaj v koordinatah
        self.id_polja_pod_figuro = None #to pomeni, da je na zacetnem polju (ta nimajo id-ja)
        #self.polje_pod_figuro = 'zacetno'
        self.ekipa = ekipa #zajci in lisice
        self.zacetne_koordinate = koordinate_figure


    def __repr__(self):
        return('Id figure:{}, polozaj:{}, ekipa: {}, zacetne koordinate:{}'.format(self.id_figure, self.koordinate_figure, self.ekipa, self.zacetne_koordinate))



class Igra():
    def __init__(self, canvas, koordinate_sredisca, seznam_polj):
        self.canvas = canvas
        self.igra_poteka = False
        self.koordinate_sredisca = koordinate_sredisca
        self.seznam_polj = seznam_polj

    def veljaven_premik(self, figura, polje, seznam_polj):
        print (polje)
        #ali je polje, na katerega se želimo premakniti, sosedno
        polje_pred_premikom = polje.najdi_polje_z_idjem(figura.id_polja_pod_figuro, seznam_polj)

        if polje_pred_premikom == None:
            if figura.ekipa == 'Lisice' and polje.namen == 'vstopno_lisica':
                return True
            if figura.ekipa == 'Zajci' and polje.namen == 'vstopno_zajec':
                return True
        print( polje_pred_premikom.sosedi)
        if polje.id_polja in polje_pred_premikom.sosedi and polje.zasedeno == False:

            print ('je sosedno')
            return True
        print('neki je narobe s sosedi')
        return False

    def ali_je_zmaga(self, figura, seznam_polj, polje):
        je_zmaga = False
        if figura.ekipa == 'Lisice' and polje.najdi_polje_z_idjem(figura.id_polja_pod_figuro, seznam_polj).namen == 'zmagovalec_je_lisica':
            print('Zmagala lisica')
            zmagovalec = 'LISICE'
            self.igra_poteka = False
            je_zmaga = True

        if figura.ekipa == 'Zajci' and polje.najdi_polje_z_idjem(figura.id_polja_pod_figuro, seznam_polj).namen == 'zmagovalec_je_zajec':
            print('Zmagal zajec')
            zmagovalec = 'ZAJCE'
            self.igra_poteka = False
            je_zmaga = True
        if je_zmaga:
            self.canvas.create_text(self.koordinate_sredisca, font=('Purisa', 20), text='ZMAGA ZA {}'.format(zmagovalec), fill='red')
        return je_zmaga


    def pokazi_veljavne_poteze(self, figura):
        for polje in self.seznam_polj:
            if figura.id_polja_pod_figuro in polje.sosedi and polje.zasedeno == False:
                self.canvas.itemconfig(polje.id_polja, fill='SeaGreen2')

    def skrij_veljavne_poteze(self, figura):
        for polje in self.seznam_polj:
            if figura.id_polja_pod_figuro in polje.sosedi:
                self.canvas.itemconfig(polje.id_polja, fill='white')

    #Preveri, ali je kakšen nasprotnik obkoljen in vrne None ali pa obkoljeno figuro
    # def ali_je_nasprotnik_obkoljen(self, figura, polje, zajci, lisice):
    #     sosednji_nasprotniki = []
    #     if figura.ekipa == 'Lisice':
    #         for zajcek in zajci:
    #             if zajcek.id_polja_pod_figuro in polje.sosedi:
    #                 sosednji_nasprotniki.append(zajcek)
    #     else:
    #         for lisica in lisice:
    #             if lisica.id_polja_pod_figuro in polje.sosedi:
    #                 sosednji_nasprotniki.append(lisica)
    #     for nasprotnik in sosednji_nasprotniki:
    #         for polje in self.seznam_polj:
    #             if polje.id_polja == nasprotnik.id_polja_pod_figuro:
    #                 nasprotnikovo_polje = polje
    #                 continue
    #         for sosed in nasprotnikovo_polje.sosedi:
    #             sosed = Polje.najdi_polje_z_idjem(self, sosed, self.seznam_polj)
    #             je_obkoljen = True
    #             if sosed.zasedeno == False:
    #                 je_obkoljen = False
    #                 continue
    #             if figura.ekipa == 'Zajci': #preveri če je na tem sosednjem polju lisica
    #                 for lisica in lisice:
    #                     if lisica.id_polja_pod_figuro == sosed.id_polja:
    #                         je_obkoljen = False
    #             if figura.ekipa == 'Lisice':
    #                 for zajec in zajci:
    #                     if zajec.id_polja_pod_figuro == sosed.id_polja:
    #                         je_obkoljen = False
    #         if je_obkoljen:
    #             return nasprotnik
    #
    #
    # #Obkoljenega prisiljo vrne na začetno polje in sprosti polje kjer je bil prej
    # def ubij_obkoljenega(self, figura, r):
    #     x, y = figura.zacetne_koordinate
    #     self.canvas.coords(figura.id_figure, x - r, y - r, x + r, y + r)

class Clovek():
    def __init__(self):
        pass
class Robot():
    def __init__(self):
        pass






