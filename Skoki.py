from tkinter import *
from Igra import *
from clovek import *
import logging
from racunalnik import *

# Privzeta minimax globina
GLOBINA = 3


def sredisce(lst):
    """Središče krogca na Canvasu z danim bounding box."""
    (x1, y1, x2, y2) = lst
    return ((x1+x2)/2, (y1+y2)/2)

class Gui():
    ROB = 100
    VELIKOST_STRANICE_PLOSCE = 400
    # Velikost polj in figur
    r = 15

    def __init__(self, master):
        # Ob novi igri se nastavita na človek/računalnik
        self.igralec_lisice = None
        self.igralec_zajci = None

        master.protocol("WM_DELETE_WINDOW", lambda: self.zapri_okno(master))
        # Narišemo platno
        self.plosca = Canvas(master, width=Gui.VELIKOST_STRANICE_PLOSCE + 2 * Gui.ROB,
                         height=Gui.VELIKOST_STRANICE_PLOSCE + 2 * Gui.ROB,
                         bg='white')
        # Motivacijski napis, ki se ne spremeni do zmage
        self.pozdrav = StringVar(master, value="Na vrsti za potezo so LISICE.")
        self.moderator = Label(master, textvariable=self.pozdrav).grid(row=0, column=0)
        self.plosca.grid()
        # Glavni menu
        menu = Menu(master)
        master.config(menu=menu)
        # Podmenu za izbiro načina igre
        menu_igra = Menu(menu)
        menu.add_cascade(label="Igra", menu=menu_igra)

        menu_igra.add_command(label="Lisice=Človek, Zajci=Človek",
                              command=lambda: self.zacni_novo_igro(Clovek(self),
                                                              Clovek(self)))

        menu_igra.add_command(label="Lisice=Človek, Zajci=Računalnik",
                            command=lambda: self.zacni_novo_igro(Clovek(self),
                                                          Racunalnik(self, Minimax(GLOBINA))))
        menu_igra.add_command(label="Lisice=Računalnik, Zajci=Človek",
                            command=lambda: self.zacni_novo_igro(Racunalnik(self, Minimax(GLOBINA)),
                                                          Clovek(self)))
        menu_igra.add_command(label="Lisice=Računalnik, Zajci=Računalnik",
                            command=lambda: self.zacni_novo_igro(Racunalnik(self, Minimax(GLOBINA)),
                                                          Racunalnik(self, Minimax(GLOBINA))))



        # Klik pokliče funkcijo kliknjeno polje
        self.plosca.bind("<Button-1>", self.kliknjeno_polje)
        # Pove nam, če imamo oznaceno figuro. Bo uporabno, ko bo gui ugotovil, ali izbiramo figuro (prvi klik) ali polje za premik (drugi klik)
        self.oznacena_figura = None
        self.polja = []
        self.igra = None
        self.lisice_gid= []
        self.zajci_gid = []
        self.oznacen = False
        self.napis_na_koncu1 = None
        self.napis_na_koncu2 = None


        #ZAČETNE KOORDINATE FIGUR
        # na te koordinate bomo razvrstili lisice in zajce izven igralne plošče
        self.zacetna_lisice = [(Gui.ROB + Gui.VELIKOST_STRANICE_PLOSCE - i/7 * Gui.VELIKOST_STRANICE_PLOSCE, 1/2*Gui.ROB) for i in range(5)]
        self.zacetna_zajci = [(Gui.ROB + Gui.VELIKOST_STRANICE_PLOSCE - i/7 * Gui.VELIKOST_STRANICE_PLOSCE, 3/2*Gui.ROB + Gui.VELIKOST_STRANICE_PLOSCE) for i in range(5)]

        #POUDARIVA VSTOPNA POLJA
        # Samo za preglednost, ob kliku se vedno pobarvajo polja, kamor lahko premaknemo izbrano figuro
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

        #POUDARIVA ZMAGOVALNA POLJA
        # Rumena kvadratka označujeta zmagovalni polji.
        P = self.plosca.create_rectangle(Gui.ROB + 1/2 * Gui.VELIKOST_STRANICE_PLOSCE - 2*Gui.r,
                                         Gui.ROB - 2* Gui.r,
                                         Gui.ROB + 1 / 2 * Gui.VELIKOST_STRANICE_PLOSCE + 2 * Gui.r,
                                         Gui.ROB + 2 * Gui.r,fill='gold')
        P = self.plosca.create_rectangle(Gui.ROB + 1/2 * Gui.VELIKOST_STRANICE_PLOSCE - 2*Gui.r,
                                         Gui.ROB + Gui.VELIKOST_STRANICE_PLOSCE - 2* Gui.r,
                                         Gui.ROB + 1 / 2 * Gui.VELIKOST_STRANICE_PLOSCE + 2 * Gui.r,
                                         Gui.ROB + Gui.VELIKOST_STRANICE_PLOSCE + 2 * Gui.r,fill='gold')

        # Narišemo polja na plošči, ki jih ne bomo več spreminjali, in njihove gide spravimo v self.polja
        # NARIŠEMO SPODNJO ZUNANJO VRSTO
        for i in range(7):
            #bounding_box
            bounding_box = (Gui.ROB + i/6 * Gui.VELIKOST_STRANICE_PLOSCE - Gui.r,
                                             Gui.ROB + Gui.VELIKOST_STRANICE_PLOSCE - Gui.r,
                                             Gui.ROB + i / 6 * Gui.VELIKOST_STRANICE_PLOSCE + Gui.r,
                                             Gui.ROB + Gui.VELIKOST_STRANICE_PLOSCE + Gui.r)

            krogec = self.plosca.create_oval(bounding_box, fill = 'white')

            self.polja.append(((sredisce(bounding_box)), krogec))

        # NARIŠEMO DESNO ZUNANJO VRSTO OD SPODAJ NAVZGOR
        for i in range(4):
             bounding_box = (Gui.ROB + Gui.VELIKOST_STRANICE_PLOSCE - Gui.r,
                             Gui.ROB + ((3-i) * Gui.VELIKOST_STRANICE_PLOSCE / 4) - Gui.r,
                             Gui.ROB + Gui.VELIKOST_STRANICE_PLOSCE + Gui.r,
                             Gui.ROB + ((3-i)) * Gui.VELIKOST_STRANICE_PLOSCE / 4 + Gui.r)
             krogec = self.plosca.create_oval(bounding_box, fill = 'white')
             self.polja.append(((sredisce(bounding_box)), krogec))

        # NARIŠEMO ZGORNJO ZUNANJO VRSTO OD DESNE PROTI LEVI
        for i in range(6):
            bounding_box = ((Gui.ROB + (5 - i)/6 * Gui.VELIKOST_STRANICE_PLOSCE - Gui.r,
                             Gui.ROB - Gui.r,
                             Gui.ROB + (5 - i)/6 * Gui.VELIKOST_STRANICE_PLOSCE + Gui.r,
                             Gui.ROB + Gui.r))

            krogec = self.plosca.create_oval(bounding_box, fill = 'white')
            self.polja.append(((sredisce(bounding_box)), krogec))

        # NARIŠEMO ZUNANJO LEVO VRSTO OD ZGORAJ DOL
        for i in range(3):
            bounding_box = (Gui.ROB - Gui.r,
                            Gui.ROB + ((i + 1) * Gui.VELIKOST_STRANICE_PLOSCE / 4) - Gui.r,
                            Gui.ROB + Gui.r,
                            Gui.ROB + ((i + 1)) * Gui.VELIKOST_STRANICE_PLOSCE / 4 + Gui.r)
            krogec = self.plosca.create_oval(bounding_box, fill = 'white')
            self.polja.append(((sredisce(bounding_box)), krogec))

        # NARIŠEMO SPODNJO NOTRANJO VRSTO OD LEVE PROTI DESNI
        for i in range(3):
            bounding_box = (Gui.ROB + 1/3 * Gui.VELIKOST_STRANICE_PLOSCE + i / 6 * Gui.VELIKOST_STRANICE_PLOSCE - Gui.r,
                            Gui.ROB + 2/3 * Gui.VELIKOST_STRANICE_PLOSCE - Gui.r,
                            Gui.ROB + 1 / 3 * Gui.VELIKOST_STRANICE_PLOSCE + i / 6 * Gui.VELIKOST_STRANICE_PLOSCE + Gui.r,
                            Gui.ROB + 2 / 3 * Gui.VELIKOST_STRANICE_PLOSCE + Gui.r)
            krogec = self.plosca.create_oval(bounding_box, fill='white')
            self.polja.append(((sredisce(bounding_box)), krogec))

        # NARIŠEMO DESNO NOTRANJO VRSTO OD SPODAJ NAVZGOR
        for i in range(2):
             bounding_box = (Gui.ROB + 2/3 * Gui.VELIKOST_STRANICE_PLOSCE - Gui.r,
                             Gui.ROB + 1/3 * Gui.VELIKOST_STRANICE_PLOSCE + (1-i)/6 * Gui.VELIKOST_STRANICE_PLOSCE - Gui.r,
                             Gui.ROB + 2 / 3 * Gui.VELIKOST_STRANICE_PLOSCE + Gui.r,
                             Gui.ROB + 1 / 3 * Gui.VELIKOST_STRANICE_PLOSCE + (1 - i) / 6 * Gui.VELIKOST_STRANICE_PLOSCE + Gui.r)

             krogec = self.plosca.create_oval(bounding_box,fill='white')
             self.polja.append(((sredisce(bounding_box)), krogec))

        # NARIŠEMO ZGORNJO NOTRANJO VRSTO OD DESNE PROTI LEVI
        for i in range(2):
             bounding_box = (Gui.ROB + 1 / 3 * Gui.VELIKOST_STRANICE_PLOSCE + (1-i) / 6 * Gui.VELIKOST_STRANICE_PLOSCE - Gui.r,
                             Gui.ROB + 1 / 3 * Gui.VELIKOST_STRANICE_PLOSCE - Gui.r,
                             Gui.ROB + 1 / 3 * Gui.VELIKOST_STRANICE_PLOSCE + (1-i) / 6 * Gui.VELIKOST_STRANICE_PLOSCE + Gui.r,
                             Gui.ROB + 1 / 3 * Gui.VELIKOST_STRANICE_PLOSCE + Gui.r)

             krogec = self.plosca.create_oval(bounding_box,fill='white')
             self.polja.append(((sredisce(bounding_box)), krogec))

        # NARIŠEMO ŠE ZADNJEGA (27)
        bounding_box = (Gui.ROB + 1/3 * Gui.VELIKOST_STRANICE_PLOSCE - Gui.r,
                         Gui.ROB + 1/2 * Gui.VELIKOST_STRANICE_PLOSCE - Gui.r,
                         Gui.ROB + 1 / 3 * Gui.VELIKOST_STRANICE_PLOSCE + Gui.r,
                         Gui.ROB + 1 / 2 * Gui.VELIKOST_STRANICE_PLOSCE + Gui.r)

        krogec = self.plosca.create_oval(bounding_box,fill='white')
        self.polja.append(((sredisce(bounding_box)), krogec))


        # NARIŠIVA POVEZAVE
        for (i,j) in Igra.povezave:
            p = self.plosca.create_line(self.polja[i][0], self.polja[j][0])
            self.plosca.tag_lower(p)

        # NARIŠIVA ZAJCE IN LISICE (sivi oz oranžni krogci iste velikosti kot polja)
        # Njihove gide damo v seznam self.zajci_gid in self.lisice_gid
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

        # Čez 1 sekundo začnemo igro človeka proti računalniku
        self.plosca.after(1000,
                          lambda: self.zacni_novo_igro(Clovek(self), Racunalnik(self, Minimax(GLOBINA))))

    def premakni_figure(self):
        # Osveži stanje na plošči
        # Premaknimo lisice
        k = 0
        # Najprej premaknemo tiste, ki so na plošči (seznam idjev zasedenih polj dobimo s self.lisice in self.zajci)
        na_plosci = len(self.igra.lisice)
        while k < na_plosci:
            (x, y) = self.polja[self.igra.lisice[k]][0]
            self.plosca.itemconfig(self.lisice_gid[k], outline='black', fill='orange')
            self.plosca.coords(self.lisice_gid[k], x - Gui.r, y - Gui.r, x + Gui.r, y + Gui.r)
            k += 1
        i = 0
        # Narišemo lisice ki so še na začetnih koordinatah
        while k < self.igra.stevilo_lisic_v_igri:
            (x, y) = self.zacetna_lisice[i]
            self.plosca.itemconfig(self.lisice_gid[k], outline='black', fill='orange')
            self.plosca.coords(self.lisice_gid[k], x - Gui.r, y - Gui.r, x + Gui.r, y + Gui.r)
            i += 1
            k += 1
        # Obkoljene lisice naredimo nevidne uporabniku
        while k < len(self.lisice_gid):
            self.plosca.itemconfig(self.lisice_gid[k], outline ='white', fill='white')
            k += 1
        #PREMAKNIVA ZAJCE
        k = 0
        na_plosci = len(self.igra.zajci)
        # Zajci na plošči
        while k < na_plosci:
            (x, y) = self.polja[self.igra.zajci[k]][0]
            self.plosca.itemconfig(self.zajci_gid[k], outline='black', fill='grey')
            self.plosca.coords(self.zajci_gid[k], x - Gui.r, y - Gui.r, x + Gui.r, y + Gui.r)
            k += 1
        i = 0
        # Zajci na začetnih koordinatah
        while k < self.igra.stevilo_zajcev_v_igri:
            (x, y) = self.zacetna_zajci[i]
            self.plosca.itemconfig(self.zajci_gid[k], outline='black', fill='grey')
            self.plosca.coords(self.zajci_gid[k], x - Gui.r, y - Gui.r, x + Gui.r, y + Gui.r)
            i += 1
            k += 1
        # Naredimo nevidne obkoljene zajce
        while k < len(self.zajci_gid):
            self.plosca.itemconfig(self.zajci_gid[k], outline = 'white', fill = 'white')
            k += 1



    def kliknjeno_polje(self, event):
        # Pokliče se ob kliku
        if self.igra is None: return None# sploh ne igramo
        # Izračunamo potezo
        x, y = event.x, event.y
        kliknjeno_polje = None
        for i in range(len(self.polja)):
            f1, f2 = self.polja[i][0]
            if (x-f1)**2 + (y-f2)**2 < Gui.r**2:
                kliknjeno_polje = i
                continue
        if kliknjeno_polje is None:
            # nismo kliknili na polje
            if self.oznacen:
                # imamo oznaceno figuro, ne naredimo nic
                pass
            else:
                # pogledamo, ali smo kliknili na cakajoco figuro
                if self.igra.na_potezi == Igra.zajci:
                    # ali smo kliknili na zajca?
                    for k in range(self.igra.stevilo_zajcev_v_igri - len(self.igra.zajci)):
                        f1, f2 = self.zacetna_zajci[k]
                        if (x - f1) ** 2 + (y - f2) ** 2 < Gui.r ** 2:
                            # oznacimo zajca, ki je kliknjen
                            self.oznacen = True
                            self.oznacena_figura = (self.igra.cakajoci_zajec, None)
                            # pobarvamo moznosti z modro
                            self.pobarvaj(self.igra.mozna_polja(self.oznacena_figura), 'SeaGreen2')
                elif self.igra.na_potezi == Igra.lisice:
                    # ali smo kliknili na lisico?
                    for k in range(self.igra.stevilo_lisic_v_igri-len(self.igra.lisice)):
                        f1, f2 = self.zacetna_lisice[k]
                        if (x - f1) ** 2 + (y - f2) ** 2 < Gui.r ** 2:
                            # oznacimo lisico, ki je kliknjena
                            self.oznacen = True
                            self.oznacena_figura = (self.igra.cakajoca_lisica, None)
                            self.pobarvaj(self.igra.mozna_polja(self.oznacena_figura), 'SeaGreen2')
        else:
            # kliknili smo na polje
            if self.oznacen:
                # imamo oznaceno figuro in polje, kamor mora iti
                assert (self.oznacena_figura is not None)
                poteza = (self.oznacena_figura, kliknjeno_polje)
                # moznosti za oznaceno figuro odstranimo
                self.pobarvaj(self.igra.mozna_polja(self.oznacena_figura), 'white')
                self.oznacen = False
                self.oznacena_figura = None
                if self.igra.na_potezi == Igra.zajci:
                    self.igralec_zajci.klik(poteza)
                elif self.igra.na_potezi == Igra.lisice:
                    self.igralec_lisice.klik(poteza)
            else:
                # ali je treba oznaciti figuro?
                if (kliknjeno_polje in self.igra.zajci) and self.igra.na_potezi == Igra.zajci:
                    self.oznacen = True
                    self.oznacena_figura = (self.igra.zajec, kliknjeno_polje)
                    self.pobarvaj(self.igra.mozna_polja(self.oznacena_figura), 'SeaGreen2')
                elif (kliknjeno_polje in self.igra.lisice) and self.igra.na_potezi == Igra.lisice:
                    self.oznacen = True
                    self.oznacena_figura = (self.igra.lisica, kliknjeno_polje)
                    self.pobarvaj(self.igra.mozna_polja(self.oznacena_figura), 'SeaGreen2')
                else:
                    # kliknjeno polje je prazno, ali pa je kliknil na figuro, ki ni na potezi
                    pass

    def povleci_potezo(self, poteza):
        # pokliče self.igra.povleci_potezo in če ta ne vrne None, premakne figure, zamenja igralca na potezi in v primeru zmage izpiše zmagovalni napis
        print ("GUI vleče potezo {0} v poziciji {1}".format(poteza, (self.igra.zajci, self.igra.lisice)))
        figura, polje = poteza
        r = self.igra.povleci_potezo(figura, polje)
        print ("GUI status poteze je {0}, pozicija je zdaj {1}".format(r, (self.igra.zajci, self.igra.lisice)))
        if r is None:
            # poteza ni veljavna
            pass
        else:
            # poteza je veljavna
            self.premakni_figure()
            self.pozdrav.set('Na vrsti za potezo so {}'.format(self.igra.na_potezi))
            # naslednji odigra potezo
            if self.igra.na_potezi == Igra.zajci:
                self.igralec_zajci.igraj()
            elif self.igra.na_potezi == Igra.lisice:
                self.igralec_lisice.igraj()
            elif self.igra.na_potezi == None:
                # igre je konec
                zmagovalec = self.igra.stanje_igre()
                self.naredi_napis_na_koncu(zmagovalec)
                self.pozdrav.set('Bravo!')

            else:
                assert False, "nedefinirano stanje igre"


    def pobarvaj(self, za_pobarvat, barva):
        #Pobarva možna polja.
        for i in za_pobarvat:
            self.plosca.itemconfig(self.polja[i][1], fill=barva)

    def zacni_novo_igro(self, igralec_lisice, igralec_zajci):
        self.plosca.itemconfig([self.polja], fill='white')
        self.pozdrav.set('Na vrsti za potezo so LISICE')
        self.prekini_igralce()
        self.igralec_lisice = igralec_lisice
        self.igralec_zajci = igralec_zajci
        self.igra = Igra()
        self.plosca.delete(self.napis_na_koncu1, self.napis_na_koncu2)
        self.premakni_figure()
        self.igralec_lisice.igraj()


    def prekini_igralce(self):
        # Sporoči igralcem, da morajo nehati razmišlljati
        logging.debug ("prekinjam igralce")
        if self.igralec_lisice: self.igralec_lisice.prekini()
        if self.igralec_zajci: self.igralec_zajci.prekini()

    def naredi_napis_na_koncu(self, zmagovalec):
        #Na koncu na platno izpiše, kdo je zmagal
        self.napis_na_koncu1 = self.plosca.create_text(Gui.ROB + 1/2 * Gui.VELIKOST_STRANICE_PLOSCE, Gui.ROB + 1/3 * Gui.VELIKOST_STRANICE_PLOSCE, font=('fixedsys', 30), text='ZMAGOVALCI SO',
                                fill='DodgerBlue2')
        self.napis_na_koncu2 = self.plosca.create_text(Gui.ROB + 1/2 * Gui.VELIKOST_STRANICE_PLOSCE, Gui.ROB + 1/2 * Gui.VELIKOST_STRANICE_PLOSCE, font=('fixedsys', 50), text='{}'.format(zmagovalec),
                                fill='red3')



    def zapri_okno(self, master):
        # Ta metoda se pokliče, ko uporabnik zapre aplikacijo
        master.destroy()


root = Tk()
root.title('Gui')
aplikacija = Gui(root)
root.mainloop()
