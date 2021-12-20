
from tkinter import *
from parseData import *
from distAndTime import *
from genAlg import *
from solution import *
import graf
import os

class Prozor(Frame):

    def __init__(self, root):
        super().__init__(root)
        self.R = root
        self.R.title('')
        self.grid(rows = 10, columns = 10)      #moze i pomocu pack, sto ispadne urednije
        self.drivers = []           #podatke prenosimo iz ucitaj u izracunaj
        self.riders = []
        self.distMat = []
        self.timeMat = []
        self.koordinate = []
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
        self.riders, self.drivers, self.koordinate = parseData(f)
        f.close()
        self.distMat = distances(self.koordinate)
        self.timeMat = times(self.koordinate, self.distMat)
        print('ok')
        return

    def izracunaj(self):
        value, S = genAlg(self.riders, self.drivers, self.distMat, self.timeMat)
        #print(value)
        for i in value:
            print(i)
        print('end val')
        #for s in S:
            #print([driver.printDriver() for driver in s.routes])
            #print('end sol')
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
        
        print('ok')
        return

    
#poziva sucelje
p = Prozor(Tk())
