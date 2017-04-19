from tkinter import *
from Potek_igre import *


class Gui():
    VELIKOST_STRANICE_PLOŠČE = 400
    ROB = 100
    r = 10

    def __init__(self, master):


        self.oznacen = False #ali smo izbrali figure za premik
        self.igralec_na_potezi = 'Lisice' #vedno začnejo lisice
        self.trenutna_figura = None #kliknjena figura
        self.zacetni_seznam_polj = [] #bomo potrebovali ob začetku nove igre
        master.protocol("WM_DELETE_WINDOW", lambda: self.zapri_okno(master))
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


        #Začetni napisi in obvestila kdo je na vrsti
        self.pozdrav = StringVar(master, value="Kdo bo nov zmagovalec in kdo nova zguba?")
        self.moderator = Label(master, textvariable=self.pozdrav).grid(row=0, column=0)



        # Igralno območje
        self.plosca = Canvas(master,width=Gui.VELIKOST_STRANICE_PLOŠČE + 2 * Gui.ROB,
                                     height=Gui.VELIKOST_STRANICE_PLOŠČE + 2 * Gui.ROB,
                                     bg = 'white')
        self.plosca.grid()
        self.izberi_nova_igra = self.plosca.create_text(Gui.ROB + 1/2*Gui.VELIKOST_STRANICE_PLOŠČE, 1/4*Gui.ROB, font=('Purisa', 20), text='V MENIJU IZBERI NOVA IGRA', fill='red')

        #gumb za igranje
        self.plosca.bind("<Button-1>", self.premik)
        
        #IGRALNA PLOSCA
        #nastavek za polja
        self.seznam_id_polj = []
        self.seznam_polj = []
        self.seznam_povezav = [(0,2), (2,4),(4,6),(6,8),(8,10), (10,12), (12,19), (19,17), (15,13), (17,15), (13,11), (11,9), (9,7), (7,5), (5,3), (3,1), (1,14), (14,16), (16,18), (18,0), (20,21), (21,22), (22,26), (26,25), (25,24), (24,23), (23,27), (27,20), (20,1), (21,5), (22,13), (25,12), (24,8), (23,0)]

        self.narisi_polja()
        self.daj_polja_v_razred()
        #narisana polja damo v razred Polje


        #risanje povezav
        for (p1, p2) in self.seznam_povezav:
            self.seznam_polj[p1].sosedi.append(self.seznam_polj[p2].id_polja)
            self.seznam_polj[p2].sosedi.append(self.seznam_polj[p1].id_polja)
            p = self.plosca.create_line(self.seznam_polj[p1].koordinate, self.seznam_polj[p2].koordinate)
            self.plosca.tag_lower(p)
        #kategoriziramo polja
        self.spremeni_posebna_polja()


        #POSTAVLJANJE FIGUR
        #1. lisice!!!
        self.lisica = PhotoImage('file=lisica.gif')
        self.lisice_id = []
        self.lisice = []
        self.ustvari_lisice()

        for i in self.lisice_id:
            lisica = Figura(self.plosca, i, sredisce(self.plosca.coords(i)), 'Lisice')
            self.lisice.append(lisica)
        #print(self.lisice)

        self.igra = Igra(self.plosca,(Gui.ROB + 1 / 2 * Gui.VELIKOST_STRANICE_PLOŠČE, Gui.ROB + 1 / 2 * Gui.VELIKOST_STRANICE_PLOŠČE),
                         self.seznam_polj)

    def daj_polja_v_razred(self):
        for i in self.seznam_id_polj:
            polje = Polje(self.plosca, i, sredisce(self.plosca.coords(i)))
            self.seznam_polj.append(polje)
        return self.seznam_polj


    def ustvari_lisice(self):

        for i in range(5):
            #ne rise lisic tako da narisem krogce
            # lisica_id = self.plosca.create_image(Gui.ROB + (i+1)/5 * Gui.VELIKOST_STRANICE_PLOŠČE, Gui.ROB ,image=self.lisica)

            lisica_id = self.plosca.create_oval(Gui.ROB + (i+1)/6 * Gui.VELIKOST_STRANICE_PLOŠČE - 10, Gui.ROB /2 -10, Gui.ROB + (i+1)/6 * Gui.VELIKOST_STRANICE_PLOŠČE + 10, Gui.ROB /2 +10  ,fill = 'orange')
            self.lisice_id.append(lisica_id)

    # 1. zajci!!!
        self.zajec = PhotoImage('file=zajec.gif')
        self.zajci_id = []
        self.zajci = []
        self.ustvari_zajce()
        for i in self.zajci_id:
            zajec = Figura(self.plosca, i, sredisce(self.plosca.coords(i)), 'Zajci')
            self.zajci.append(zajec)
            # print(self.lisice)

    def ustvari_zajce(self):

        for i in range(5):
            # ne rise zajcev tako da narisem krogce
            # zajec_id = self.plosca.create_image(Gui.ROB + (i+1)/5 * Gui.VELIKOST_STRANICE_PLOŠČE, Gui.ROB ,image=self.zajec)

            zajec_id = self.plosca.create_oval(Gui.ROB + (i + 1) / 6 * Gui.VELIKOST_STRANICE_PLOŠČE - 10,
                                               Gui.ROB + Gui.VELIKOST_STRANICE_PLOŠČE + Gui.ROB / 2 - 10,
                                               Gui.ROB + (i + 1) / 6 * Gui.VELIKOST_STRANICE_PLOŠČE + 10,
                                               Gui.ROB + Gui.VELIKOST_STRANICE_PLOŠČE + Gui.ROB / 2 + 10, fill='grey')
            self.zajci_id.append(zajec_id)


    #dodajanje posebnih polj(zmagovalna, vstopna)
    def spremeni_posebna_polja(self):
        self.seznam_polj[0].namen = 'vstopno_zajec'
        self.seznam_polj[12].namen = 'vstopno_zajec'
        self.seznam_polj[1].namen = 'vstopno_lisica'
        self.seznam_polj[13].namen = 'vstopno_lisica'
        self.seznam_polj[7].namen = 'zmagovalec_je_zajec'
        self.plosca.itemconfig(self.seznam_polj[7].id_polja, fill='IndianRed1')
        self.seznam_polj[6].namen = 'zmagovalec_je_lisica'
        self.plosca.itemconfig(self.seznam_polj[6].id_polja, fill='IndianRed1')
        #print(self.seznam_polj)

    def zapri_okno(self, master):
        # """Ta metoda se pokliče, ko uporabnik zapre aplikacijo."""
        # Kasneje bo tu treba še kaj narediti
        master.destroy()

    def zacni_novo_igro(self):
        self.igralec_na_potezi = 'Lisice'
        self.pozdrav.set('Na vrsti za potezo so {}'.format(self.igralec_na_potezi))
        self.igra.igra_poteka = True
        self.plosca.delete(self.izberi_nova_igra)

        for i in self.seznam_polj:
            i.zasedenost = False
            if i.namen == 'zmagovalec_je_zajec' or i.namen == 'zmagovalec_je_lisica':
                self.plosca.itemconfig(i.id_polja, fill='IndianRed1')
            else:
                self.plosca.itemconfig(i.id_polja, fill='white')

        for lisica in self.lisice:
            if lisica.id_polja_pod_figuro != None:
                lisica.koordinate_figure = lisica.zacetne_koordinate
                lisica.id_polja_pod_figuro = None
                (z1, z2) = lisica.zacetne_koordinate
                self.plosca.coords(lisica.id_figure, z1 - Gui.r, z2 - Gui.r, z1 + Gui.r, z2 + Gui.r)

        for zajec in self.zajci:
            if zajec.id_polja_pod_figuro != None:
                zajec.koordinate_figure = zajec.zacetne_koordinate
                zajec.id_polja_pod_figuro = None
                (z1, z2) = zajec.zacetne_koordinate
                self.plosca.coords(zajec.id_figure, z1 - Gui.r, z2 - Gui.r, z1 + Gui.r, z2 + Gui.r)






    def narisi_polja(self):
        # oglišča
        (x_a1, y_a1) = (Gui.ROB, Gui.ROB + Gui.VELIKOST_STRANICE_PLOŠČE)
        (x_a2, y_a2) = (Gui.ROB + Gui.VELIKOST_STRANICE_PLOŠČE, Gui.ROB + Gui.VELIKOST_STRANICE_PLOŠČE)
        (x_b1, y_b1) = (Gui.ROB, Gui.ROB)
        (x_b2, y_b2) = (Gui.ROB + Gui.VELIKOST_STRANICE_PLOŠČE, Gui.ROB)

        #krogci za označitev posebnih polj
        self.plosca.create_oval(x_a1 - 3/2 * Gui.r, y_a1 - 3/2 * Gui.r,
                                x_a1 + 3/2 * Gui.r, y_a1 + 3/2 * Gui.r,
                                fill='cyan2')
        self.plosca.create_oval(x_a2 - 3/2 * Gui.r, y_a2 - 3/2 * Gui.r,
                                x_a2 + 3/2 * Gui.r, y_a2 + 3/2 * Gui.r,
                                fill='cyan2')
        self.plosca.create_oval(x_b1 - 3/2 * Gui.r, y_b1 - 3/2 * Gui.r,
                                x_b1 + 3/2 * Gui.r, y_b1 + 3/2 * Gui.r,
                                fill='cyan2')
        self.plosca.create_oval(x_b2 - 3/2 * Gui.r, y_b2 - 3/2 * Gui.r,
                                x_b2 + 3/2 * Gui.r, y_b2 + 3/2 * Gui.r,
                                fill='cyan2')

        # zunanji kvadrat
        # vodoravno
        for i in range(7):
            id = self.plosca.create_oval(x_a1 + i / 6 * Gui.VELIKOST_STRANICE_PLOŠČE - Gui.r, y_a1 - Gui.r,
                                         x_a1 + i / 6 * Gui.VELIKOST_STRANICE_PLOŠČE + Gui.r, y_a1 + Gui.r,
                                         fill="white")
            self.seznam_id_polj.append(id)
            id = self.plosca.create_oval(x_b1 + i / 6 * Gui.VELIKOST_STRANICE_PLOŠČE - Gui.r, y_b1 - Gui.r,
                                         x_a1 + i / 6 * Gui.VELIKOST_STRANICE_PLOŠČE + Gui.r, y_b1 + Gui.r,
                                         fill="white")
            self.seznam_id_polj.append(id)

        # navpično
        for i in range(1, 4):
            id = self.plosca.create_oval(x_a1 - Gui.r, y_b1 + i / 4 * Gui.VELIKOST_STRANICE_PLOŠČE - Gui.r,
                                         x_b1 + Gui.r, y_b1 + i / 4 * Gui.VELIKOST_STRANICE_PLOŠČE + Gui.r,
                                         fill="white")
            self.seznam_id_polj.append(id)

            id = self.plosca.create_oval(x_a2 - Gui.r, y_b2 + i / 4 * Gui.VELIKOST_STRANICE_PLOŠČE - Gui.r,
                                         x_b2 + Gui.r, y_b2 + i / 4 * Gui.VELIKOST_STRANICE_PLOŠČE + Gui.r,
                                         fill="white")
            self.seznam_id_polj.append(id)

        # Notranji kvadrat
        # vodoravno
        for i in range(3):
            id = self.plosca.create_oval(
                x_b1 + 1 / 3 * Gui.VELIKOST_STRANICE_PLOŠČE + i / 2 * 1 / 3 * Gui.VELIKOST_STRANICE_PLOŠČE - Gui.r,
                y_b1 + 1 / 3 * Gui.VELIKOST_STRANICE_PLOŠČE - Gui.r,
                x_b1 + 1 / 3 * Gui.VELIKOST_STRANICE_PLOŠČE + i / 2 * 1 / 3 * Gui.VELIKOST_STRANICE_PLOŠČE + Gui.r,
                y_b1 + 1 / 3 * Gui.VELIKOST_STRANICE_PLOŠČE + Gui.r, fill="white")
            self.seznam_id_polj.append(id)

        for i in range(3):
            id = self.plosca.create_oval(
                x_b1 + 1 / 3 * Gui.VELIKOST_STRANICE_PLOŠČE + i / 2 * 1 / 3 * Gui.VELIKOST_STRANICE_PLOŠČE - Gui.r,
                y_b1 + 2 / 3 * Gui.VELIKOST_STRANICE_PLOŠČE - Gui.r,
                x_b1 + 1 / 3 * Gui.VELIKOST_STRANICE_PLOŠČE + i / 2 * 1 / 3 * Gui.VELIKOST_STRANICE_PLOŠČE + Gui.r,
                y_b1 + 2 / 3 * Gui.VELIKOST_STRANICE_PLOŠČE + Gui.r, fill="white")
            self.seznam_id_polj.append(id)

        id1 = self.plosca.create_oval(x_b1 + 2 / 3 * Gui.VELIKOST_STRANICE_PLOŠČE - Gui.r,
                                      y_b1 + 1 / 2 * Gui.VELIKOST_STRANICE_PLOŠČE - Gui.r,
                                      x_b1 + 2 / 3 * Gui.VELIKOST_STRANICE_PLOŠČE + Gui.r,
                                      y_b1 + 1 / 2 * Gui.VELIKOST_STRANICE_PLOŠČE + Gui.r,
                                      fill="white")

        id2 = self.plosca.create_oval(x_b1 + 1 / 3 * Gui.VELIKOST_STRANICE_PLOŠČE - Gui.r,
                                      y_b1 + 1 / 2 * Gui.VELIKOST_STRANICE_PLOŠČE - Gui.r,
                                      x_b1 + 1 / 3 * Gui.VELIKOST_STRANICE_PLOŠČE + Gui.r,
                                      y_b1 + 1 / 2 * Gui.VELIKOST_STRANICE_PLOŠČE + Gui.r,
                                      fill="white")

        self.seznam_id_polj.append(id1)
        self.seznam_id_polj.append(id2)
        return self.seznam_id_polj



    def premik(self, event):
        if self.igra.igra_poteka:
            x,y = event.x, event.y
            print (x,y)
            if self.oznacen == False:
                self.trenutna_figura = self.oznacena_figura(x ,y, self.igralec_na_potezi)
                if self.trenutna_figura != None: #če smo klinkili na figuro
                    self.oznacen = True
                    self.igra.pokazi_veljavne_poteze(self.trenutna_figura)
            else:
                self.potencialna_figura = self.oznacena_figura(x, y, self.igralec_na_potezi)
                if self.potencialna_figura != None:
                    self.igra.skrij_veljavne_poteze(self.trenutna_figura)
                    self.trenutna_figura = self.potencialna_figura
                    self.igra.pokazi_veljavne_poteze(self.trenutna_figura)
                else:
                    self.premakni_figuro(self.trenutna_figura, x, y)


    def oznacena_figura(self, x, y, igralec_na_potezi):
        if self.igralec_na_potezi == 'Lisice':
            for i in self.lisice:
                f1, f2 = i.koordinate_figure
                if (f1 - x)**2 + (f2 - y)**2 <= 100: #100 je kvadrat polmera krogca, bova spremenili v lisice
                    #print(x, y, 'koordinte miške')
                    #print (f1,f2, 'koordinate kjer so figure')
                    #print (int((f1 - x)**2 + (f2 - y)**2), 'kvadrat razdalje')
                    return i
                #else:

        if self.igralec_na_potezi == 'Zajci':
            for i in self.zajci:
                f1, f2 = i.koordinate_figure
                if (f1 - x)**2 + (f2 - y)**2 <= 100: #100 je kvadrat polmera krogca, bova spremenili v zajce
                    return i


    def premakni_figuro(self, figura, x, y):
        #print(figura)
        trenutni_polozaj_figure = figura.koordinate_figure
        for polje in self.seznam_polj:
            #print (polje)
            f1, f2 = polje.koordinate

            if (f1, f2) == (trenutni_polozaj_figure):
                polje.zasedeno = False

            if (f1 - x) ** 2 + (f2 - y) ** 2 <= (Gui.r)**2:
                if self.igra.veljaven_premik(figura, polje, self.seznam_polj):

                    self.plosca.coords(figura.id_figure, f1 - 10, f2 - 10,  f1 + 10, f2 + 10)
                    print('premaknil figuro na {},{}'.format(f1, f2))
                    self.oznacen = False
                    polje.zasedeno = figura.ekipa
                    self.igra.skrij_veljavne_poteze(figura)

                    figura.id_polja_pod_figuro = polje.id_polja
                    figura.koordinate_figure = f1, f2

                    #if self.igra.ali_je_nasprotnik_obkoljen(figura, polje, self.zajci, self.lisice) != None:
                    #    self.igra.ubij_obkoljenega(self.igra.ali_je_nasprotnik_obkoljen(figura, polje, self.zajci, self.lisice), Gui.r)

                    if self.igra.ali_je_zmaga(figura, self.seznam_polj, polje):
                        self.pozdrav.set('Bravo!')

                    if self.igralec_na_potezi == 'Lisice':
                        self.igralec_na_potezi = 'Zajci'

                    else:
                        self.igralec_na_potezi = 'Lisice'
                    if self.igra.igra_poteka:
                        self.pozdrav.set('Na vrsti za potezo so {}'.format(self.igralec_na_potezi))
                    print(polje)
                    print (figura)
        return figura






root = Tk()
root.title('Gui')
aplikacija = Gui(root)
root.mainloop()
