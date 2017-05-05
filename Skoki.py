from tkinter import *
from Igra import *
from clovek import *
import logging
from racunalnik import *

# Privzeta minimax globina, Äe je nismo podali ob zagonu v ukazni vrstici
MINIMAX_GLOBINA = 3

def sredisce(lst):
    """Središče krogca na Canvasu z danim bounding box."""
    (x1, y1, x2, y2) = lst
    return ((x1+x2)/2, (y1+y2)/2)

class Gui():
    ROB = 100
    VELIKOST_STRANICE_PLOSCE = 400
    r = 10

    def __init__(self, master):
        self.igralec_lisice = None
        self.igralec_zajci = None
        master.protocol("WM_DELETE_WINDOW", lambda: self.zapri_okno(master))

        self.plosca = Canvas(master, width=Gui.VELIKOST_STRANICE_PLOSCE + 2 * Gui.ROB,
                         height=Gui.VELIKOST_STRANICE_PLOSCE + 2 * Gui.ROB,
                         bg='white')
        #Začetni napisi in obvestila kdo je na vrsti
        self.pozdrav = StringVar(master, value="Kdo bo nov zmagovalec in kdo nova zguba?")
        self.moderator = Label(master, textvariable=self.pozdrav).grid(row=0, column=0)
        self.plosca.grid()
        # Glavni menu
        menu = Menu(master)
        master.config(menu=menu)
        # Podmenu za izbiro igre
        menu_igra = Menu(menu)
        menu.add_cascade(label="Igra", menu=menu_igra)

        menu_igra.add_command(label="Lisice=Človek, Zajci=Človek",
                              command=lambda: self.zacni_novo_igro(Clovek(self),
                                                              Clovek(self)))

        menu_igra.add_command(label="Lisice=Človek, Zajci=Računalnik",
                            command=lambda: self.zacni_novo_igro(Clovek(self),
                                                          Racunalnik(self, Minimax(3))))
        menu_igra.add_command(label="Lisice=Računalnik, Zajci=Človek",
                            command=lambda: self.zacni_novo_igro(Racunalnik(self, Minimax(3)),
                                                          Clovek(self)))
        menu_igra.add_command(label="Lisice=Računalnik, Zajci=Računalnik",
                            command=lambda: self.zacni_novo_igro(Racunalnik(self, Minimax(3)),
                                                          Racunalnik(self, Minimax(3))))




        self.plosca.bind("<Button-1>", self.kliknjeno_polje)

        self.oznacena_figura = None
        self.polja = []
        self.igra = Igra()
        self.lisice_gid= []
        self.zajci_gid = []
        self.oznacen = False
        self.napis_na_koncu = None


        #ZAČETNE KOORDINATE FIGUR
        self.zacetna_lisice = [(Gui.ROB + Gui.VELIKOST_STRANICE_PLOSCE - i/7 * Gui.VELIKOST_STRANICE_PLOSCE, 1/2*Gui.ROB) for i in range(5)]
        self.zacetna_zajci = [(Gui.ROB + Gui.VELIKOST_STRANICE_PLOSCE - i/7 * Gui.VELIKOST_STRANICE_PLOSCE, 3/2*Gui.ROB + Gui.VELIKOST_STRANICE_PLOSCE) for i in range(5)]


        #POUDARIVA VSTOPNA VPOLJA
        p = self.plosca.create_oval(Gui.ROB - 3/2*Gui.r, Gui.ROB - 3/2*Gui.r,
                                Gui.ROB + 3/2*Gui.r, Gui.ROB + 3/2*Gui.r , fill='DeepPink3')
        self.plosca.tag_lower(p)
        p = self.plosca.create_oval(Gui.ROB + Gui.VELIKOST_STRANICE_PLOSCE - 3/2 * Gui.r, Gui.ROB - 3/2 * Gui.r,
                                Gui.ROB + Gui.VELIKOST_STRANICE_PLOSCE + 3/2 * Gui.r, Gui.ROB + 3/2 * Gui.r,
                                fill='DeepPink3')
        self.plosca.tag_lower(p)
        p = self.plosca.create_oval(Gui.ROB - 3/2*Gui.r, Gui.ROB + Gui.VELIKOST_STRANICE_PLOSCE - 3/2*Gui.r,
                                Gui.ROB + 3 / 2 * Gui.r, Gui.ROB + Gui.VELIKOST_STRANICE_PLOSCE + 3 / 2 * Gui.r,
                                fill='DeepPink3')
        self.plosca.tag_lower(p)
        p = self.plosca.create_oval(Gui.ROB + Gui.VELIKOST_STRANICE_PLOSCE - 3 / 2 * Gui.r, Gui.ROB + Gui.VELIKOST_STRANICE_PLOSCE - 3 / 2 * Gui.r,
                                Gui.ROB + Gui.VELIKOST_STRANICE_PLOSCE + 3 / 2 * Gui.r, Gui.ROB + Gui.VELIKOST_STRANICE_PLOSCE + 3 / 2 * Gui.r,
                                fill='DeepPink3')
        self.plosca.tag_lower(p)

        #NARIŠEMO SPODNJO ZUNANJO VRSTO
        for i in range(7):
            #bounding_box
            bounding_box = (Gui.ROB + i/6 * Gui.VELIKOST_STRANICE_PLOSCE - Gui.r,
                                             Gui.ROB + Gui.VELIKOST_STRANICE_PLOSCE - Gui.r,
                                             Gui.ROB + i / 6 * Gui.VELIKOST_STRANICE_PLOSCE + Gui.r,
                                             Gui.ROB + Gui.VELIKOST_STRANICE_PLOSCE + Gui.r)

            krogec = self.plosca.create_oval(bounding_box)

            self.polja.append(((sredisce(bounding_box)), krogec))

        #NARIŠEMO DESNO ZUNANJO VRSTO OD SPODAJ NAVZGOR
        for i in range(4):
             bounding_box = (Gui.ROB + Gui.VELIKOST_STRANICE_PLOSCE - Gui.r,
                             Gui.ROB + ((3-i) * Gui.VELIKOST_STRANICE_PLOSCE / 4) - Gui.r,
                             Gui.ROB + Gui.VELIKOST_STRANICE_PLOSCE + Gui.r,
                             Gui.ROB + ((3-i)) * Gui.VELIKOST_STRANICE_PLOSCE / 4 + Gui.r)
             krogec = self.plosca.create_oval(bounding_box)
             self.polja.append(((sredisce(bounding_box)), krogec))

        #NARIŠEMO ZGORNJO ZUNANJO VRSTO OD DESNE PROTI LEVI
        for i in range(6):
            bounding_box = ((Gui.ROB + (5 - i)/6 * Gui.VELIKOST_STRANICE_PLOSCE - Gui.r,
                             Gui.ROB - Gui.r,
                             Gui.ROB + (5 - i)/6 * Gui.VELIKOST_STRANICE_PLOSCE + Gui.r,
                             Gui.ROB + Gui.r))

            krogec = self.plosca.create_oval(bounding_box)
            self.polja.append(((sredisce(bounding_box)), krogec))

        #NARIŠEMO ZUNANJO LEVO VRSTO OD ZGORAJ DOL
        for i in range(3):
            bounding_box = (Gui.ROB - Gui.r,
                            Gui.ROB + ((i + 1) * Gui.VELIKOST_STRANICE_PLOSCE / 4) - Gui.r,
                            Gui.ROB + Gui.r,
                            Gui.ROB + ((i + 1)) * Gui.VELIKOST_STRANICE_PLOSCE / 4 + Gui.r)
            krogec = self.plosca.create_oval(bounding_box)
            self.polja.append(((sredisce(bounding_box)), krogec))

        #NARIŠEMO SPODNJO NOTRANJO VRSTO OD LEVE PROTI DESNI
        for i in range(3):
            bounding_box = (Gui.ROB + 1/3 * Gui.VELIKOST_STRANICE_PLOSCE + i / 6 * Gui.VELIKOST_STRANICE_PLOSCE - Gui.r,
                            Gui.ROB + 2/3 * Gui.VELIKOST_STRANICE_PLOSCE - Gui.r,
                            Gui.ROB + 1 / 3 * Gui.VELIKOST_STRANICE_PLOSCE + i / 6 * Gui.VELIKOST_STRANICE_PLOSCE + Gui.r,
                            Gui.ROB + 2 / 3 * Gui.VELIKOST_STRANICE_PLOSCE + Gui.r)
            krogec = self.plosca.create_oval(bounding_box, fill='white')
            self.polja.append(((sredisce(bounding_box)), krogec))

        # #NARIŠEMO DESNO NOTRANJO VRSTO OD SPODAJ NAVZGOR
        for i in range(2):
             bounding_box = (Gui.ROB + 2/3 * Gui.VELIKOST_STRANICE_PLOSCE - Gui.r,
                             Gui.ROB + 1/3 * Gui.VELIKOST_STRANICE_PLOSCE + (1-i)/6 * Gui.VELIKOST_STRANICE_PLOSCE - Gui.r,
                             Gui.ROB + 2 / 3 * Gui.VELIKOST_STRANICE_PLOSCE + Gui.r,
                             Gui.ROB + 1 / 3 * Gui.VELIKOST_STRANICE_PLOSCE + (1 - i) / 6 * Gui.VELIKOST_STRANICE_PLOSCE + Gui.r)

             krogec = self.plosca.create_oval(bounding_box,fill='white')
             self.polja.append(((sredisce(bounding_box)), krogec))

        #NARIŠEMO ZGORNJO NOTRANJO VRSTO OD DESNE PROTI LEVI
        for i in range(2):
             bounding_box = (Gui.ROB + 1 / 3 * Gui.VELIKOST_STRANICE_PLOSCE + (1-i) / 6 * Gui.VELIKOST_STRANICE_PLOSCE - Gui.r,
                             Gui.ROB + 1 / 3 * Gui.VELIKOST_STRANICE_PLOSCE - Gui.r,
                             Gui.ROB + 1 / 3 * Gui.VELIKOST_STRANICE_PLOSCE + (1-i) / 6 * Gui.VELIKOST_STRANICE_PLOSCE + Gui.r,
                             Gui.ROB + 1 / 3 * Gui.VELIKOST_STRANICE_PLOSCE + Gui.r)

             krogec = self.plosca.create_oval(bounding_box,fill='white')
             self.polja.append(((sredisce(bounding_box)), krogec))

        #NARIŠEMO ŠE ZADNJEGA (27)
        bounding_box = (Gui.ROB + 1/3 * Gui.VELIKOST_STRANICE_PLOSCE - Gui.r,
                         Gui.ROB + 1/2 * Gui.VELIKOST_STRANICE_PLOSCE - Gui.r,
                         Gui.ROB + 1 / 3 * Gui.VELIKOST_STRANICE_PLOSCE + Gui.r,
                         Gui.ROB + 1 / 2 * Gui.VELIKOST_STRANICE_PLOSCE + Gui.r)

        krogec = self.plosca.create_oval(bounding_box,fill='white')
        self.polja.append(((sredisce(bounding_box)), krogec))

        #NARIŠIVA POVEZAVE
        for (i,j) in self.igra.povezave:
            p = self.plosca.create_line(self.polja[i][0], self.polja[j][0])
            self.plosca.tag_lower(p)

        #NARIŠIVA ZAJCE IN LISICE
        for i in range(5):
            zajec = self.plosca.create_oval(Gui.ROB + 1/2 * Gui.VELIKOST_STRANICE_PLOSCE - Gui.r,
                                            3/2 * Gui.ROB + Gui.VELIKOST_STRANICE_PLOSCE - Gui.r,
                                            Gui.ROB + 1 / 2 * Gui.VELIKOST_STRANICE_PLOSCE + Gui.r,
                                            3 / 2 * Gui.ROB + Gui.VELIKOST_STRANICE_PLOSCE + Gui.r,
                                            fill = 'grey')
            self.zajci_gid.append(zajec)

            lisica = self.plosca.create_oval(Gui.ROB + 1/2 * Gui.VELIKOST_STRANICE_PLOSCE - Gui.r,
                                             1/2 * Gui.ROB - Gui.r,
                                             Gui.ROB + 1 / 2 * Gui.VELIKOST_STRANICE_PLOSCE + Gui.r,
                                             1 / 2 * Gui.ROB + Gui.r,
                                             fill = 'orange')
            self.lisice_gid.append(lisica)

        self.premakni_figure() #Začetno stanje na plošči

    def premakni_figure(self):
        #osveži stanje na plošči
        #PREMAKNIVA LISICE
        k = 0
        na_plosci = len(self.igra.lisice)
        while k < na_plosci:
            (x, y) = self.polja[self.igra.lisice[k]][0]
            self.plosca.coords(self.lisice_gid[k], x - Gui.r, y - Gui.r, x + Gui.r, y + Gui.r)
            k += 1
        i = 0
        while k < self.igra.stevilo_lisic_v_igri:

            (x, y) = self.zacetna_lisice[i]
            self.plosca.coords(self.lisice_gid[k], x - Gui.r, y - Gui.r, x + Gui.r, y + Gui.r)
            i += 1
            k += 1
        #PREMAKNIVA ZAJCE
        k = 0
        na_plosci = len(self.igra.zajci)
        while k < na_plosci:
            (x, y) = self.polja[self.igra.zajci[k]][0]
            self.plosca.coords(self.zajci_gid[k], x - Gui.r, y - Gui.r, x + Gui.r, y + Gui.r)
            k += 1
        i = 0
        while k < self.igra.stevilo_zajcev_v_igri:
            (x, y) = self.zacetna_zajci[i]
            self.plosca.coords(self.zajci_gid[k], x - Gui.r, y - Gui.r, x + Gui.r, y + Gui.r)
            i += 1
            k += 1

    def kliknjeno_polje(self, event):
        #pokliče označeno figuro
        x, y = event.x, event.y
        kliknjeno_polje = None
        for i in range(len(self.polja)):
            f1, f2 = self.polja[i][0]
            if (x-f1)**2 + (y-f2)**2 < Gui.r**2:
                kliknjeno_polje = i
                continue
        if self.oznacen == False:
            self.oznacena_figura = self.isci_figuro(x,y,kliknjeno_polje)
            if self.igra.igra_poteka and self.oznacena_figura != None:
                self.pobarvaj(self.igra.mozna_polja(self.oznacena_figura), 'SeaGreen2')
        if self.oznacen == True and kliknjeno_polje != None:
            if self.igra.veljavna_poteza(self.oznacena_figura, kliknjeno_polje):
                self.pobarvaj(self.igra.mozna_polja(self.oznacena_figura), 'white')
                self.igra.spremeni_stanje(self.oznacena_figura, kliknjeno_polje)
                self.premakni_figure()
                if self.igra.ali_je_zmaga(self.oznacena_figura, kliknjeno_polje) != None:
                    self.naredi_napis_na_koncu(self.igra.ali_je_zmaga(self.oznacena_figura, kliknjeno_polje))

                self.oznacen = False


    def isci_figuro(self, x, y, kliknjeno_polje):
        #Išče figuro in polje, kamor se prestavi figura
        if kliknjeno_polje == None:
            if self.igra.na_potezi == Igra.zajci:
                for k in range(self.igra.stevilo_zajcev_v_igri - len(self.igra.zajci)):
                    f1, f2 = self.zacetna_zajci[k]
                    if (x - f1) ** 2 + (y - f2) ** 2 < Gui.r ** 2:
                        self.oznacen = True

                        return (self.igra.cakajoci_zajec, None)
            if self.igra.na_potezi == Igra.lisice:
                for k in range(self.igra.stevilo_lisic_v_igri-len(self.igra.lisice)):
                    f1, f2 = self.zacetna_lisice[k]
                    if (x - f1) ** 2 + (y - f2) ** 2 < Gui.r ** 2:
                        self.oznacen = True
                        return (self.igra.cakajoca_lisica, None)
            return None
        if kliknjeno_polje in self.igra.zajci and self.igra.na_potezi == Igra.zajci:
            self.oznacen = True
            return (self.igra.zajec, kliknjeno_polje)
        if kliknjeno_polje in self.igra.lisice and self.igra.na_potezi == Igra.lisice:
            self.oznacen = True
            return (self.igra.lisica, kliknjeno_polje)

    def povleci_potezo(self, poteza):
        
        figura, polje = poteza
        r = self.igra.povleci_potezo(figura, polje)
        if r is None:
            pass
        else:
            self.premakni_figure()


    def pobarvaj(self, za_pobarvat, barva):
        #Pobarva možna polja.
        for i in za_pobarvat:
            self.plosca.itemconfig(self.polja[i][1], fill=barva)

    def zacni_novo_igro(self, igralec_lisice, igralec_zajci):
        self.prekini_igralce()
        self.igralec_lisice = igralec_lisice
        self.igralec_zajci = igralec_zajci
        self.igra.igra_poteka = True
        self.igra.na_potezi = Igra.lisice
        self.igra.lisice = []
        self.igra.zajci = []
        self.igra.stevilo_lisic_v_igri = 5
        self.igra.stevilo_zajcev_v_igri = 5
        self.premakni_figure()
        self.plosca.delete(self.napis_na_koncu)
        self.igralec_lisice.igraj()

    def prekini_igralce(self):
        """Sporoči igralcem, da morajo nehati razmišlljati."""
        logging.debug ("prekinjam igralce")
        if self.igralec_lisice: self.igralec_lisice.prekini()
        if self.igralec_zajci: self.igralec_zajci.prekini()

    def naredi_napis_na_koncu(self, zmagovalec):
        #Nakoncu na platno izpiše, kdo je zmagal
        self.napis_na_koncu = self.plosca.create_text(Gui.ROB + 1/2 * Gui.VELIKOST_STRANICE_PLOSCE, Gui.ROB + 1/2 * Gui.VELIKOST_STRANICE_PLOSCE, font=('Purisa', 20), text='ZMAGOVALCI SO {}'.format(zmagovalec),
                                fill='red')


    def zapri_okno(self, master):
        # """Ta metoda se pokliče, ko uporabnik zapre aplikacijo."""
        # Kasneje bo tu treba še kaj narediti
        master.destroy()


root = Tk()
root.title('Gui')
aplikacija = Gui(root)
root.mainloop()