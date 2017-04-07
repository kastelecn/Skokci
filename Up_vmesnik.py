from tkinter import *
from Potek_igre import *


class Gui():
    VELIKOST_STRANICE_PLOŠČE = 400
    ROB = 200
    r = 10

    def __init__(self, master):

        self.igralec_na_potezi = 'Lisice' #vedno začnejo lisice
        self.trenutna_figura = None #kliknjena figura
        master.protocol("WM_DELETE_WINDOW", lambda: self.zapri_okno(master))
        # Glavni menu
        menu = Menu(master)
        master.config(menu=menu)
        # Podmenu za izbiro igre
        menu_igra = Menu(menu)
        menu.add_cascade(label="Igra", menu=menu_igra)
        menu_igra.add_command(label="Nova igra",
                              command=self.zacni_igro)
        # Igralno območje
        self.plosca = Canvas(master,width=Gui.VELIKOST_STRANICE_PLOŠČE + 2 * Gui.ROB,
                                     height=Gui.VELIKOST_STRANICE_PLOŠČE + 2 * Gui.ROB,
                                     bg = 'white')
        self.plosca.grid()
        self.oznacen = False #ali smo izbrali figure za premik
        #IGRALNA PLOSCA
        #nastavek za polja
        self.seznam_id_polj = []
        self.seznam_polj = []
        self.seznam_povezav = [(0,2), (2,4),(4,6),(6,8),(8,10), (10,12), (12,19), (19,17), (15,13), (17,15), (13,11), (11,9), (9,7), (7,5), (5,3), (3,1), (1,14), (14,16), (16,18), (18,0), (20,21), (21,22), (22,26), (26,25), (25,24), (24,23), (23,27), (27,20), (20,1), (21,5), (22,13), (25,12), (24,8), (23,0)]

        self.narisi_polja()
        #narisana polja damo v razred Polje
        for i in self.seznam_id_polj:
            polje = Polje(self.plosca, i, sredisce(self.plosca.coords(i)))
            self.seznam_polj.append(polje)

        #risanje povezav
        for (p1, p2) in self.seznam_povezav:
            self.seznam_polj[p1].sosedi.append(self.seznam_polj[p2].id_polja)
            self.seznam_polj[p2].sosedi.append(self.seznam_polj[p1].id_polja)
            p = self.plosca.create_line(self.seznam_polj[p1].koordinate, self.seznam_polj[p2].koordinate)
            self.plosca.tag_lower(p)
        #kategoriziramo polja
        self.spremeni_posebna_polja()


        #postavljanje figur
        self.lisica = PhotoImage('file=lisica.gif')
        self.lisice_id = []
        self.lisice = []
        self.ustvari_lisice()
        for i in self.lisice_id:
            lisica = Figura(self.plosca, i, sredisce(self.plosca.coords(i)), 'Lisice')
            self.lisice.append(lisica)
        print(self.lisice)
    #ustvarimo lisice
    def ustvari_lisice(self):

        for i in range(5):
            #ne rise lisic tako da narisem krogce
            # lisica_id = self.plosca.create_image(Gui.ROB + (i+1)/5 * Gui.VELIKOST_STRANICE_PLOŠČE, Gui.ROB ,image=self.lisica)

            lisica_id = self.plosca.create_oval(Gui.ROB + (i+1)/6 * Gui.VELIKOST_STRANICE_PLOŠČE - 10, Gui.ROB /2 -10, Gui.ROB + (i+1)/6 * Gui.VELIKOST_STRANICE_PLOŠČE + 10, Gui.ROB /2 +10  ,fill = 'orange')
            self.lisice_id.append(lisica_id)


    #dodajanje posebnih polj(zmagovalna, vstopna)
    def spremeni_posebna_polja(self):
        self.seznam_polj[0].namen = 'vstopno_a'

        self.seznam_polj[12].namen = 'vstopno_a'
        self.seznam_polj[1].namen = 'vstopno_b'
        self.seznam_polj[13].namen = 'vstopno_b'
        self.seznam_polj[7].namen = 'zmagovalec_a'
        self.seznam_polj[6].namen = 'zmagovalec_b'
        print(self.seznam_polj)

    def zapri_okno(self, master):
        # """Ta metoda se pokliče, ko uporabnik zapre aplikacijo."""
        # Kasneje bo tu treba še kaj narediti
        master.destroy()

    def zacni_igro(self):
        pass

    def narisi_polja(self):
        # oglišča
        (x_a1, y_a1) = (Gui.ROB, Gui.ROB + Gui.VELIKOST_STRANICE_PLOŠČE)
        (x_a2, y_a2) = (Gui.ROB + Gui.VELIKOST_STRANICE_PLOŠČE, Gui.ROB + Gui.VELIKOST_STRANICE_PLOŠČE)
        (x_b1, y_b1) = (Gui.ROB, Gui.ROB)
        (x_b2, y_b2) = (Gui.ROB + Gui.VELIKOST_STRANICE_PLOŠČE, Gui.ROB)

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

        self.plsoca.bind("<Button-1>", self.premik(event, self.oznacen))

    def premik(self, oznacen, event):
        x,y = event.x, event.y
        if oznacen == False:
            self.trenutna_figura = self.oznacena_figura(x,y, self.igralec_na_potezi)
            if self.trenutna_figura != None: #če smo klinkili na figuro
                self.oznacen = True
                self.pokazi_veljavne_poteze(figura)
        else:
            premakni_figuro(x,y)

    def pokazi_veljavne_poteze(self, figura):
        pass

    def oznacena_figura(self, x, y, igralec_na_potezi):
        if igralec_na_potezi == 'Lisice':
            for i in self.lisice:
                f1, f2 = i.koordinate_figure
                if (f1 - x)^2 + (f2 - y)^2 <= 100: #100 je kvadrat polmera krogca, bova spremenili v lisice
                    return i
        if igralec_na_potezi == 'Zajci':
            for i in self.zajci:
                f1, f2 = i.koordinate_figure
                if (f1 - x)^2 + (f2 - y)^2 <= 100: #100 je kvadrat polmera krogca, bova spremenili v zajci
                    return i
    def premakni_figuro(self, x, y):
        for polje in self.seznam_polj:
            f1, f2 = polje.koordinate
            if (f1 - x) ^ 2 + (f2 - y) ^ 2 <= (Gui.r)^2:





root = Tk()
root.title('Gui')
aplikacija = Gui(root)
root.mainloop()
