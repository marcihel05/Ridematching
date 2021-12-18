
from tkinter import *
import graf
import parseData
import os

class Prozor(Frame):

    def __init__(self, root):
        super().__init__(root)
        self.R = root
        self.R.title('')
        self.grid(rows = 10, columns = 10)      #moze i pomocu pack, sto ispadne urednije
        self.podaci = []            #podatke prenosimo iz ucitaj u izracunaj
        self.kreirajSucelje()
        return
    
    def kreirajSucelje(self):

        self.L1 = Label(self, text = 'Ime ulazne datoteke: ')
        self.L1.grid(row = 0, column = 0)
        
        self.vchoice = StringVar()
        self.vchoice.set('RM698_L15.txt')
        self.choices = ['RM698_L15.txt', 'RM698_L60.txt', 'RM698_R15.txt', 'RM698_R60.txt', 'RM744_L15.txt', 'RM744_L60.txt', 'RM744_R15.txt', 'RM698_R60.txt']
        self.option = OptionMenu(self, self.vchoice, *self.choices)
        self.option.grid(row = 0, column = 1)
        
        self.G1 = Button(self, text = 'Ucitaj', command = self.ucitaj).grid(row = 0, column = 2)

        self.G2 = Button(self, text = 'Izracunaj', command = self.izracunaj).grid(row = 1, column = 2)
        return

    def ucitaj(self):
        s = str(self.vchoice.get())
        #pretpostavka da je se u istom direktoriju nalazi dir instances
        #s poddir instances_metadata koji sadrzi datoteke - mijenjati po potrebi
        f = open(os.path.join('./instances/instances_metadata', s), 'r')
        self.podaci = parseData.parseData(f)
        f.close()

##        #test
##        print('\n')
##        print(self.podaci)
##        print('\n')
        return

    def izracunaj(self):
        #posalji podatke u algoritam - pokreni main sa self.podaci
        #primi nazad i prikazi graf(ove)

        #test
        koord_x = [self.podaci[0][0][1][0], self.podaci[0][0][2][0]]
        koord_y = [self.podaci[0][0][1][1], self.podaci[0][0][2][1]]
        #print(koord_x)
        #print(koord_y)
        x = [koord_x[0], koord_x[1]]
        y = [koord_y[0], koord_y[1]]
        labels = ['A','B']
        #poziv grafa - ako radi
        #print([x])
        graf.main([x],[y],[labels])
        return

    
#poziva sucelje
p = Prozor(Tk())
