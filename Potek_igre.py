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
    def __init__(self, canvas, id_figure, polozaj, ekipa):
        self.canvas = canvas
        self.id_figure = id_figure
        self.polozaj = polozaj  #id polja, na katerem se nahaja
        self.ekipa = ekipa #modri in rdeci

        #lisice:
        self.lisica = PhotoImage('file=lisica.gif')
        #self.id_lisica1 = self.canvas.create_image()




