from tkinter import *
from Igra import *

def sredisce(lst):
    """Središče krogca na Canvasu z danim bounding box."""
    (x1, y1, x2, y2) = lst
    return ((x1+x2)/2, (y1+y2)/2)

class Gui():
    rob = 100
    velikost_stranice_plosce = 400
    r = 10

    def __init__(self, master):

        master.protocol("WM_DELETE_WINDOW", lambda: self.zapri_okno(master))

        self.plosca = Canvas(master, width=Gui.velikost_stranice_plosce + 2 * Gui.rob,
                         height=Gui.velikost_stranice_plosce + 2 * Gui.rob,
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
        menu_igra.add_command(label="Nova igra",
                              command=self.zacni_novo_igro)
        menu_igra.add_command(label="Igram s clovekom",
                              command=lambda:self.zacni_novo_igro(Clovek(self), Clovek(self)))
        menu_igra.add_command(label="Nimam pravega soigralca",
                              command=lambda:self.zacni_novo_igro(Clovek(self), Robot(self)))
        menu_igra.add_command(label="Dolgcas mi je in ne da se mi igrat",
                              command=lambda:self.zacni_novo_igro(Robot(self), Robot(self)))


        self.plosca.bind("<Button-1>", self.kliknjeno_polje)

        self.oznacena_figura = None
        self.polja = []
        self.igra = Igra()
        self.lisice_gid= []
        self.zajci_gid = []
        self.oznacen = False


        #ZAČETNE KOORDINATE FIGUR
        self.zacetna_lisice = [(Gui.rob + Gui.velikost_stranice_plosce - i/7 * Gui.velikost_stranice_plosce, 1/2*Gui.rob) for i in range(5)]
        self.zacetna_zajci = [(Gui.rob + Gui.velikost_stranice_plosce - i/7 * Gui.velikost_stranice_plosce, 3/2*Gui.rob + Gui.velikost_stranice_plosce) for i in range(5)]

        #NARIŠEMO SPODNJO ZUNANJO VRSTO
        for i in range(7):
            #bounding_box
            bounding_box = (Gui.rob + i/6 * Gui.velikost_stranice_plosce - Gui.r,
                                             Gui.rob + Gui.velikost_stranice_plosce - Gui.r,
                                             Gui.rob + i / 6 * Gui.velikost_stranice_plosce + Gui.r,
                                             Gui.rob + Gui.velikost_stranice_plosce + Gui.r)

            krogec = self.plosca.create_oval(bounding_box)

            self.polja.append(((sredisce(bounding_box)), krogec))

        #NARIŠEMO DESNO ZUNANJO VRSTO OD SPODAJ NAVZGOR
        for i in range(4):
             bounding_box = (Gui.rob + Gui.velikost_stranice_plosce - Gui.r,
                             Gui.rob + ((3-i) * Gui.velikost_stranice_plosce / 4) - Gui.r,
                             Gui.rob + Gui.velikost_stranice_plosce + Gui.r,
                             Gui.rob + ((3-i)) * Gui.velikost_stranice_plosce / 4 + Gui.r)
             krogec = self.plosca.create_oval(bounding_box)
             self.polja.append(((sredisce(bounding_box)), krogec))

        #NARIŠEMO ZGORNJO ZUNANJO VRSTO OD DESNE PROTI LEVI
        for i in range(6):
            bounding_box = ((Gui.rob + (5 - i)/6 * Gui.velikost_stranice_plosce - Gui.r,
                             Gui.rob - Gui.r,
                             Gui.rob + (5 - i)/6 * Gui.velikost_stranice_plosce + Gui.r,
                             Gui.rob + Gui.r))

            krogec = self.plosca.create_oval(bounding_box)
            self.polja.append(((sredisce(bounding_box)), krogec))

        #NARIŠEMO ZUNANJO LEVO VRSTO OD ZGORAJ DOL
        for i in range(3):
            bounding_box = (Gui.rob - Gui.r,
                            Gui.rob + ((i + 1) * Gui.velikost_stranice_plosce / 4) - Gui.r,
                            Gui.rob + Gui.r,
                            Gui.rob + ((i + 1)) * Gui.velikost_stranice_plosce / 4 + Gui.r)
            krogec = self.plosca.create_oval(bounding_box)
            self.polja.append(((sredisce(bounding_box)), krogec))

        #NARIŠEMO SPODNJO NOTRANJO VRSTO OD LEVE PROTI DESNI
        for i in range(3):
            bounding_box = (Gui.rob + 1/3 * Gui.velikost_stranice_plosce + i / 6 * Gui.velikost_stranice_plosce - Gui.r,
                            Gui.rob + 2/3 * Gui.velikost_stranice_plosce - Gui.r,
                            Gui.rob + 1 / 3 * Gui.velikost_stranice_plosce + i / 6 * Gui.velikost_stranice_plosce + Gui.r,
                            Gui.rob + 2 / 3 * Gui.velikost_stranice_plosce + Gui.r)
            krogec = self.plosca.create_oval(bounding_box)
            self.polja.append(((sredisce(bounding_box)), krogec))

        # #NARIŠEMO DESNO NOTRANJO VRSTO OD SPODAJ NAVZGOR
        for i in range(2):
             bounding_box = (Gui.rob + 2/3 * Gui.velikost_stranice_plosce - Gui.r,
                             Gui.rob + 1/3 * Gui.velikost_stranice_plosce + (1-i)/6 * Gui.velikost_stranice_plosce - Gui.r,
                             Gui.rob + 2 / 3 * Gui.velikost_stranice_plosce + Gui.r,
                             Gui.rob + 1 / 3 * Gui.velikost_stranice_plosce + (1 - i) / 6 * Gui.velikost_stranice_plosce + Gui.r)

             krogec = self.plosca.create_oval(bounding_box)
             self.polja.append(((sredisce(bounding_box)), krogec))

        #NARIŠEMO ZGORNJO NOTRANJO VRSTO OD DESNE PROTI LEVI
        for i in range(2):
             bounding_box = (Gui.rob + 1 / 3 * Gui.velikost_stranice_plosce + (1-i) / 6 * Gui.velikost_stranice_plosce - Gui.r,
                             Gui.rob + 1 / 3 * Gui.velikost_stranice_plosce - Gui.r,
                             Gui.rob + 1 / 3 * Gui.velikost_stranice_plosce + (1-i) / 6 * Gui.velikost_stranice_plosce + Gui.r,
                             Gui.rob + 1 / 3 * Gui.velikost_stranice_plosce + Gui.r)

             krogec = self.plosca.create_oval(bounding_box)
             self.polja.append(((sredisce(bounding_box)), krogec))

        #NARIŠEMO ŠE ZADNJEGA (27)
        bounding_box = (Gui.rob + 1/3 * Gui.velikost_stranice_plosce - Gui.r,
                         Gui.rob + 1/2 * Gui.velikost_stranice_plosce - Gui.r,
                         Gui.rob + 1 / 3 * Gui.velikost_stranice_plosce + Gui.r,
                         Gui.rob + 1 / 2 * Gui.velikost_stranice_plosce + Gui.r)

        krogec = self.plosca.create_oval(bounding_box)
        self.polja.append(((sredisce(bounding_box)), krogec))

        #NARIŠIVA POVEZAVE
        for (i,j) in self.igra.povezave:
            self.plosca.create_line(self.polja[i][0], self.polja[j][0])

        #NARIŠIVA ZAJCE IN LISICE
        for i in range(5):
            zajec = self.plosca.create_oval(Gui.rob + 1/2 * Gui.velikost_stranice_plosce - Gui.r,
                                            3/2 * Gui.rob + Gui.velikost_stranice_plosce - Gui.r,
                                            Gui.rob + 1 / 2 * Gui.velikost_stranice_plosce + Gui.r,
                                            3 / 2 * Gui.rob + Gui.velikost_stranice_plosce + Gui.r,
                                            fill = 'grey')
            self.zajci_gid.append(zajec)

            lisica = self.plosca.create_oval(Gui.rob + 1/2 * Gui.velikost_stranice_plosce - Gui.r,
                                             1/2 * Gui.rob - Gui.r,
                                             Gui.rob + 1 / 2 * Gui.velikost_stranice_plosce + Gui.r,
                                             1 / 2 * Gui.rob + Gui.r,
                                             fill = 'orange')
            self.lisice_gid.append(lisica)

        self.premakni_figure()

    def premakni_figure(self):
        #PREMAKNIVA LISICE
        k = 0
        na_plosci = len(self.igra.lisice)
        while k < na_plosci:
            (x, y) = self.polja[self.igra.lisice[k]][0]
            self.plosca.coords(self.lisice_gid[k], x - Gui.r, y - Gui.r, x + Gui.r, y + Gui.r)
            k += 1
        i = 0
        while k < len(self.lisice_gid):
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
        while k < len(self.zajci_gid):
            (x, y) = self.zacetna_zajci[i]
            self.plosca.coords(self.zajci_gid[k], x - Gui.r, y - Gui.r, x + Gui.r, y + Gui.r)
            i += 1
            k += 1

    def kliknjeno_polje(self, event):
        x, y = event.x, event.y
        kliknjeno_polje = None
        for i in range(len(self.polja)):
            f1, f2 = self.polja[i][0]
            if (x-f1)**2 + (y-f2)**2 < Gui.r**2:
                kliknjeno_polje = i
                continue
        if self.oznacen == False:
            self.oznacena_figura = self.isci_figuro(x,y,kliknjeno_polje)
        if self.oznacen == True and kliknjeno_polje != None:
            if self.igra.veljavna_poteza(self.oznacena_figura, kliknjeno_polje):
                self.igra.spremeni_stanje(self.oznacena_figura, kliknjeno_polje)
                self.premakni_figure()
                self.oznacen = False


    def isci_figuro(self, x, y, kliknjeno_polje):
        if kliknjeno_polje == None:
            if self.igra.na_potezi == Igra.zajci:
                for k in range(5 - len(self.igra.zajci)):
                    f1, f2 = self.zacetna_zajci[k]
                    if (x - f1) ** 2 + (y - f2) ** 2 < Gui.r ** 2:
                        self.oznacen = True
                        return (self.igra.cakajoci_zajec, None)
            if self.igra.na_potezi == Igra.lisice:
                for k in range(5-len(self.igra.lisice)):
                    f1, f2 = self.zacetna_lisice[k]
                    if (x - f1) ** 2 + (y - f2) ** 2 < Gui.r ** 2:
                        self.oznacen = True
                        return (self.igra.cakajoca_lisica, None)
            return None
        if kliknjeno_polje in self.igra.zajci:
            self.oznacen = True
            return (self.igra.zajec, kliknjeno_polje)
        if kliknjeno_polje in self.igra.lisice:
            self.oznacen = True
            return (self.igra.lisica, kliknjeno_polje)






    def zacni_novo_igro(self):
        self.igra.igra_poteka = True
        self.igra.na_potezi = Igra.lisice
        self.igra.lisice = []
        self.igra.zajci = []
        self.premakni_figure()


    def zapri_okno(self, master):
        # """Ta metoda se pokliče, ko uporabnik zapre aplikacijo."""
        # Kasneje bo tu treba še kaj narediti
        master.destroy()

root = Tk()
root.title('Gui')
aplikacija = Gui(root)
root.mainloop()