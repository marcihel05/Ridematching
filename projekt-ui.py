
from tkinter import *
from parseData import *
from distAndTime import *
from genAlg import *
from solution import *
import graf
import graphValues
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
        self.k_label = []
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
        
        self.vlabel = StringVar()
        self.vlabel.set('')
        self.L2 = Label(self, textvariable = self.vlabel)
        self.L2.grid(row = 1, column = 0, columnspan = 2)
        
        self.vlabel1 = StringVar()
        self.vlabel1.set('')
        self.L3 = Label(self, textvariable = self.vlabel1)
        self.L3.grid(row = 2, column = 0, columnspan = 3)
        
        self.G1 = Button(self, text = 'Ucitaj', command = self.ucitaj).grid(row = 0, column = 2)

        self.G2 = Button(self, text = 'Izracunaj', command = self.izracunaj).grid(row = 1, column = 2)
        return

    def ucitaj(self):
        s = str(self.vchoice.get())
        #pretpostavka da je se u istom direktoriju nalazi dir instances
        #s poddir instances_metadata koji sadrzi datoteke - mijenjati po potrebi
        f = open(os.path.join('./instances/instances_metadata', s), 'r')
        self.riders, self.drivers, self.koordinate = parseData(f)
        #if s in ['RM698_L15.txt', 'RM698_L60.txt', 'RM744_L15.txt', 'RM744_L60.txt']: self.riders, self.drivers, self.koordinate = parseData2(f, 0) #za vozace biramo one koji imaju najvecu udaljenost
        #else: self.riders, self.drivers, self.koordinate = parseData2(f, 1) #vozace biramo nasumicno
        f.close()
        self.distMat = distances(self.koordinate)
        self.timeMat = times(self.koordinate, self.distMat)
        self.k_label = ['' for i in range(len(self.koordinate))]
        self.vlabel.set('Ucitavanje uspjesno!')
        return

    def izracunaj(self):
        value, S, matched, distance, time, riderTime = genAlg(self.riders, self.drivers, self.distMat, self.timeMat)
        s = S[len(S) - 1]
        self.vlabel.set('Izracun uspjesan!\n Broj nesparenih putnika: ' + str(len(s.unmatched)) + '\nBroj sparenih putnika: ' + str(len(s.riders)-len(s.unmatched)))
        #for i in value:
            #print(i)
        #print('end val')
        #for s in S:
            #print([driver.printDriver() for driver in s.routes])
            #print('end sol')
        
        G = []
        br = 1
        poruka = ''
        #s = S[len(S) - 1]
        a = """  for s in S:
            if poruka != '':
                poruka += '\n'
            poruka += 'Broj nesparenih putnika u gen ' + str(br) + ': ' + str(len(s.unmatched))
            self.vlabel1.set(poruka)
            n = len(s.routes)   #broj drivera (routes) u solution (uzeti n-1!)
            X = []
            Y = []
            I = set()
            L = []
            for i in range(n-1):
                if len(s.routes[i].stops):
                    x = []
                    y = []
                    x.append(self.koordinate[s.routes[i].start][0])
                    y.append(self.koordinate[s.routes[i].start][1])
                    if self.k_label[s.routes[i].start] == '':
                        self.k_label[s.routes[i].start] = 'd'+ str(s.routes[i].id) + '+'
                    else:
                        self.k_label[s.routes[i].start] += '\nd'+ str(s.routes[i].id) + '+'
                    I.add(s.routes[i].start)
                    for r in s.routes[i].stops:
                        x.append(self.koordinate[r[1]][0])
                        y.append(self.koordinate[r[1]][1])
                        #d_id r_id +/- oznaka za svaku točku na putu
                        if r[2]:
                            c = '-'     #arrival
                        else:
                            c = '+'     #departure
                        if self.k_label[r[1]] == '':
                            self.k_label[r[1]] = 'd'+ str(s.routes[i].id) + ' r' + str(r[0].id) + c
                        else:
                            self.k_label[r[1]] += '\nd'+ str(s.routes[i].id) + ' r' + str(r[0].id) + c
                        I.add(r[1])
                    x.append(self.koordinate[s.routes[i].end][0])
                    y.append(self.koordinate[s.routes[i].end][1])
                    if self.k_label[s.routes[i].start] == '':
                        self.k_label[s.routes[i].end] = 'd'+ str(s.routes[i].id) + '-'
                    else:
                        self.k_label[s.routes[i].end] += '\nd'+ str(s.routes[i].id) + '-'
                    I.add(s.routes[i].end)
                    X.append(x)
                    Y.append(y)
            
            for i in I:
                L.append((self.koordinate[i], self.k_label[i]))
            G.append((X,Y,L,br))
            br += 1
            self.k_label = ['' for i in range(len(self.koordinate))]"""

        poruka += 'Broj nesparenih putnika u gen ' + str(br) + ': ' + str(len(s.unmatched))
        #self.vlabel1.set(poruka)
        n = len(s.routes)   #broj drivera (routes) u solution (uzeti n-1!)
        X = []
        Y = []
        I = set()
        L = []
        for i in range(n-1):
            if len(s.routes[i].stops):
                x = []
                y = []
                x.append(self.koordinate[s.routes[i].start][0])
                y.append(self.koordinate[s.routes[i].start][1])
                if self.k_label[s.routes[i].start] == '':
                    self.k_label[s.routes[i].start] = 'd'+ str(s.routes[i].id) + '+'
                else:
                    self.k_label[s.routes[i].start] += '\nd'+ str(s.routes[i].id) + '+'
                I.add(s.routes[i].start)
                for r in s.routes[i].stops:
                    x.append(self.koordinate[r[1]][0])
                    y.append(self.koordinate[r[1]][1])
                    #d_id r_id +/- oznaka za svaku točku na putu
                    if r[2]:
                        c = '-'     #arrival
                    else:
                        c = '+'     #departure
                    if self.k_label[r[1]] == '':
                        self.k_label[r[1]] = 'd'+ str(s.routes[i].id) + ' r' + str(r[0].id) + c
                    else:
                        self.k_label[r[1]] += '\nd'+ str(s.routes[i].id) + ' r' + str(r[0].id) + c
                    I.add(r[1])
                x.append(self.koordinate[s.routes[i].end][0])
                y.append(self.koordinate[s.routes[i].end][1])
                if self.k_label[s.routes[i].start] == '':
                    self.k_label[s.routes[i].end] = 'd'+ str(s.routes[i].id) + '-'
                else:
                    self.k_label[s.routes[i].end] += '\nd'+ str(s.routes[i].id) + '-'
                I.add(s.routes[i].end)
                X.append(x)
                Y.append(y)
            
        for i in I:
            L.append((self.koordinate[i], self.k_label[i]))
        G.append((X,Y,L,br))
        #br += 1
        self.k_label = ['' for i in range(len(self.koordinate))]
        
        for route in s.routes:
            route.printDriver()
        print(value[len(value) - 1])
        graf.main(G)
        graf.plotSolutionOnMap(G)
        graphValues.graphValues(value)
        #graphValues.graphUnmatched(matched)
        #graphValues.graphDistance(distance)
        graphValues.graphAll(value,matched, distance, time, riderTime)
        
        return

    
#poziva sucelje
p = Prozor(Tk())
p.mainloop()
