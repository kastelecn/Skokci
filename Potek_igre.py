class Polje():
    def __init__(self, canvas, id_polja, koordinate):
        self.canvas = canvas 
        self.id_polja = id_polja
        self.koordinate = koordinate
        self.zasedeno = False
        self.sosedi = []
        self.namen = 'navadno' #lahko je se vstopno_a, vstopno_b ali zmagovalec_a, zmagovalec_b

    def __repr__(self):
        return ('Id polja: {}, koordinate: {}, sosedi: {}, namen: {}'.format(self.id_polja, self.koordinate, self.sosedi, self.namen))


        

def sredisce(lst):
    """Središče krogca na Canvasu z danim bounding box."""
    (x1, y1, x2, y2) = lst
    return ((x1+x2)/2, (y1+y2)/2)
    


class Figura():
    def __init__(self, canvas, id_figure, koordinate_figure, ekipa):
        self.canvas = canvas
        self.id_figure = id_figure
        self.koordinate_figure = koordinate_figure  #polozaj v koordinatah
        self.polje_pod_figuro = 'zacetno'
        self.ekipa = ekipa #zajci in lisice



    def __repr__(self):
        return('Id figure:{}, polozaj:{}, ekipa: {}'.format(self.id_figure, self.koordinate_figure, self.ekipa))


class Igra():
    def __init__(self, canvas):
        self.canvas = canvas









