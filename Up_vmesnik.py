import tkinter
from Potek_igre import *


class Gui():
    VELIKOST_STRANICE_PLOŠČE = 400
    ROB = 200

    r = 10

    def __init__(self, master):

        master.protocol("WM_DELETE_WINDOW", lambda: self.zapri_okno(master))

        # Glavni menu
        menu = tkinter.Menu(master)
        master.config(menu=menu)

        # Podmenu za izbiro igre
        menu_igra = tkinter.Menu(menu)
        menu.add_cascade(label="Igra", menu=menu_igra)
        menu_igra.add_command(label="Nova igra",
                              command=self.zacni_igro)

        # Igralno območje
        self.plosca = tkinter.Canvas(master,
                                     width=Gui.VELIKOST_STRANICE_PLOŠČE + 2 * Gui.ROB,
                                     height=Gui.VELIKOST_STRANICE_PLOŠČE + 2 * Gui.ROB,
                                     bg = 'white')

        self.plosca.grid()

        self.seznam_id = []
        self.seznam_polj = []
        self.seznam_povezav = [(0,2), (2,4),(4,6),(6,8),(8,10), (10,12), (12,19), (19,17), (15,13), (17,15), (13,11), (11,9), (9,7), (7,5), (5,3), (3,1), (1,14), (14,16), (16,18), (18,0), (20,21), (21,22), (22,26), (26,25), (25,24), (24,23), (23,27), (27,20), (20,1), (21,5), (22,13), (25,12), (24,8), (23,0)]

        self.narisi_polja()

        for i in self.seznam_id:
            polje = Polje(self.plosca, i, sredisce(self.plosca.coords(i)))
            self.seznam_polj.append(polje)


        for (p1, p2) in self.seznam_povezav:
            self.seznam_polj[p1].sosedi.append(self.seznam_polj[p2].id_polja)
            self.seznam_polj[p2].sosedi.append(self.seznam_polj[p1].id_polja)
            p = self.plosca.create_line(self.seznam_polj[p1].koordinate, self.seznam_polj[p2].koordinate)
            self.plosca.tag_lower(p)
        self.spremeni_posebna_polja()

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
            self.seznam_id.append(id)
            id = self.plosca.create_oval(x_b1 + i / 6 * Gui.VELIKOST_STRANICE_PLOŠČE - Gui.r, y_b1 - Gui.r,
                                         x_a1 + i / 6 * Gui.VELIKOST_STRANICE_PLOŠČE + Gui.r, y_b1 + Gui.r,
                                         fill="white")
            self.seznam_id.append(id)

        # navpično
        for i in range(1, 4):
            id = self.plosca.create_oval(x_a1 - Gui.r, y_b1 + i / 4 * Gui.VELIKOST_STRANICE_PLOŠČE - Gui.r,
                                         x_b1 + Gui.r, y_b1 + i / 4 * Gui.VELIKOST_STRANICE_PLOŠČE + Gui.r,
                                         fill="white")
            self.seznam_id.append(id)

            id = self.plosca.create_oval(x_a2 - Gui.r, y_b2 + i / 4 * Gui.VELIKOST_STRANICE_PLOŠČE - Gui.r,
                                         x_b2 + Gui.r, y_b2 + i / 4 * Gui.VELIKOST_STRANICE_PLOŠČE + Gui.r,
                                         fill="white")
            self.seznam_id.append(id)

        # Notranji kvadrat
        # vodoravno
        for i in range(3):
            id = self.plosca.create_oval(
                x_b1 + 1 / 3 * Gui.VELIKOST_STRANICE_PLOŠČE + i / 2 * 1 / 3 * Gui.VELIKOST_STRANICE_PLOŠČE - Gui.r,
                y_b1 + 1 / 3 * Gui.VELIKOST_STRANICE_PLOŠČE - Gui.r,
                x_b1 + 1 / 3 * Gui.VELIKOST_STRANICE_PLOŠČE + i / 2 * 1 / 3 * Gui.VELIKOST_STRANICE_PLOŠČE + Gui.r,
                y_b1 + 1 / 3 * Gui.VELIKOST_STRANICE_PLOŠČE + Gui.r, fill="white")
            self.seznam_id.append(id)

        for i in range(3):
            id = self.plosca.create_oval(
                x_b1 + 1 / 3 * Gui.VELIKOST_STRANICE_PLOŠČE + i / 2 * 1 / 3 * Gui.VELIKOST_STRANICE_PLOŠČE - Gui.r,
                y_b1 + 2 / 3 * Gui.VELIKOST_STRANICE_PLOŠČE - Gui.r,
                x_b1 + 1 / 3 * Gui.VELIKOST_STRANICE_PLOŠČE + i / 2 * 1 / 3 * Gui.VELIKOST_STRANICE_PLOŠČE + Gui.r,
                y_b1 + 2 / 3 * Gui.VELIKOST_STRANICE_PLOŠČE + Gui.r, fill="white")
            self.seznam_id.append(id)

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

        self.seznam_id.append(id1)

        self.seznam_id.append(id2)

        return self.seznam_id


root = tkinter.Tk()
aplikacija = Gui(root)
root.mainloop()
