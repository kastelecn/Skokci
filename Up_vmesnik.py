import tkinter

class Gui():

    VELIKOST_STRANICE_PLOŠČE = 400
    ROB = 200

    r = 5

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
                                     height=Gui.VELIKOST_STRANICE_PLOŠČE + 2* Gui.ROB)
       
        self.plosca.grid()

        
        self.seznam_id = []

        
        self.narisi_polja()

        


    def zapri_okno(self, master):
    #"""Ta metoda se pokliče, ko uporabnik zapre aplikacijo."""
    # Kasneje bo tu treba še kaj narediti
        master.destroy()


    def zacni_igro(self):
        pass


    def narisi_polja(self):
        # oglišča
        (x_a1, y_a1) = (Gui.ROB, Gui.ROB + Gui.VELIKOST_STRANICE_PLOŠČE)
        (x_a2, y_a2)= (Gui.ROB + Gui.VELIKOST_STRANICE_PLOŠČE, Gui.ROB + Gui.VELIKOST_STRANICE_PLOŠČE)
        (x_b1, y_b1) = (Gui.ROB, Gui.ROB)
        (x_b2, y_b2) = (Gui.ROB + Gui.VELIKOST_STRANICE_PLOŠČE, Gui.ROB)
        

        # zunanji kvadrat
        #vodoravno
        for i in range(7):
            id = self.plosca.create_oval(x_a1 + i / 6 * Gui.VELIKOST_STRANICE_PLOŠČE - Gui.r, y_a1 - Gui.r, x_a1 + i / 6 * Gui.VELIKOST_STRANICE_PLOŠČE + Gui.r, y_a1 + Gui.r )
            self.seznam_id.append(id)
            id = self.plosca.create_oval(x_b1 + i / 6 * Gui.VELIKOST_STRANICE_PLOŠČE - Gui.r, y_b1 - Gui.r, x_a1 + i / 6 * Gui.VELIKOST_STRANICE_PLOŠČE + Gui.r, y_b1 + Gui.r )
            self.seznam_id.append(id)

        
        #navpično
        for i in range(1,4):
            id = self.plosca.create_oval(x_a1  - Gui.r, y_b1 + i / 4 * Gui.VELIKOST_STRANICE_PLOŠČE- Gui.r,
                                         x_b1 + Gui.r, y_b1  + i / 4 * Gui.VELIKOST_STRANICE_PLOŠČE + Gui.r)
            self.seznam_id.append(id)

            id = self.plosca.create_oval(x_a2  - Gui.r, y_b2 + i / 4 * Gui.VELIKOST_STRANICE_PLOŠČE- Gui.r,
                                         x_b2 + Gui.r, y_b2  + i / 4 * Gui.VELIKOST_STRANICE_PLOŠČE + Gui.r)
            self.seznam_id.append(id)
            
        #Notranji kvadrat
        #vodoravno
        for i in range(3):
            id = self.plosca.create_oval(x_b1 + 1/3*Gui.VELIKOST_STRANICE_PLOŠČE + i/2 *1/3 * Gui.VELIKOST_STRANICE_PLOŠČE -Gui.r, y_b1 + 1/3 *Gui.VELIKOST_STRANICE_PLOŠČE - Gui.r,
                                         x_b1 + 1/3*Gui.VELIKOST_STRANICE_PLOŠČE + i/2 *1/3 * Gui.VELIKOST_STRANICE_PLOŠČE +Gui.r, y_b1 + 1/3 *Gui.VELIKOST_STRANICE_PLOŠČE + Gui.r)
            self.seznam_id.append(id)

        for i in range(3):
            id = self.plosca.create_oval(x_b1 + 1/3*Gui.VELIKOST_STRANICE_PLOŠČE + i/2 *1/3 * Gui.VELIKOST_STRANICE_PLOŠČE -Gui.r, y_b1 + 2/3 *Gui.VELIKOST_STRANICE_PLOŠČE - Gui.r,
                                         x_b1 + 1/3*Gui.VELIKOST_STRANICE_PLOŠČE + i/2 *1/3 * Gui.VELIKOST_STRANICE_PLOŠČE +Gui.r, y_b1 + 2/3 *Gui.VELIKOST_STRANICE_PLOŠČE + Gui.r)
            self.seznam_id.append(id)

        id1 = self.plosca.create_oval(x_b1 + 2/3 * Gui.VELIKOST_STRANICE_PLOŠČE -Gui.r, y_b1 + 1/2 *Gui.VELIKOST_STRANICE_PLOŠČE - Gui.r,
                                         x_b1 + 2/3 * Gui.VELIKOST_STRANICE_PLOŠČE +Gui.r, y_b1 + 1/2*Gui.VELIKOST_STRANICE_PLOŠČE + Gui.r)

        id2 = self.plosca.create_oval(x_b1 + 1/3 * Gui.VELIKOST_STRANICE_PLOŠČE -Gui.r, y_b1 + 1/2 *Gui.VELIKOST_STRANICE_PLOŠČE - Gui.r,
                                         x_b1 + 1/3 * Gui.VELIKOST_STRANICE_PLOŠČE +Gui.r, y_b1 + 1/2*Gui.VELIKOST_STRANICE_PLOŠČE + Gui.r)

        self.seznam_id.append(id1)

        self.seznam_id.append(id2)
        
        
        
        
        return self.seznam_id

    print (self.seznam_id)           



##class Polje():
##
##    def __init__(self, id):
##        self.seznam_id = [2]
##        self.id = id
##        self.sredisce = None
##        self.sosedi = []
##
##        
##
##    def poveži(self, other):
##        self.sosedi.append(other)
##        other.sosedi.append(self)
##
##    #print(self.seznam_id1)



root = tkinter.Tk()
aplikacija = Gui(root)
root.mainloop()
