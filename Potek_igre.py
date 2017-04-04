class Polje():
    def __init__(self, canvas, id_polja, koordinate, sosedi):#master?
        self.canvas = canvas 
        self.id_polja = id_polja
        self.koordinate = koordinate
        self.zasedeno = False
        self.sosedi = sosedi

    def __repr__(self):
        return ('Ploje id: {}, koordinate: {}, sosedi: {}'.format(self.id_polja, self.koordinate, self.sosedi))

    #def ali_je_sosed(self):
        

def sredisce(lst):
    """Središče krogca na Canvasu z danim bounding box."""
    (x1, y1, x2, y2) = lst
    return ((x1+x2)/2, (y1+y2)/2)
    
