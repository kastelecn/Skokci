

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
    def __init__(self, canvas):
        self.canvas = canvas

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

    def ali_je_zmaga(self, figura):
        if figura.ekipa == 'Lisice' and polje.najdi_polje_z_idjem(figura.id_polja_pod_figuro, Gui.seznam_polj).namen == 'zmagovalec_je_lisica':
            print('Zmagala lisica')
            return True






class Clovek():
    def __init__(self):
        pass
class Robot():
    def __init__(self):
        pass






