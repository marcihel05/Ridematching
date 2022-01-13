
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
        self.L1.grid(row = 0, column = 0, columnspan = 2)
        
        self.vchoice = StringVar()
        self.vchoice.set('RM698_L15.txt')
        self.choices = ['RM698_L15.txt', 'RM698_L60.txt', 'RM698_R15.txt', 'RM698_R60.txt', 'RM744_L15.txt', 'RM744_L60.txt', 'RM744_R15.txt', 'RM744_R60.txt']
        self.option = OptionMenu(self, self.vchoice, *self.choices)
        self.option.grid(row = 0, column = 2, columnspan = 2)
        
        self.vlabel = StringVar()
        self.vlabel.set('')
        self.L2 = Label(self, textvariable = self.vlabel)
        self.L2.grid(row = 5, column = 0, columnspan = 4)
        
        self.vlabel1 = StringVar()
        self.vlabel1.set('')
        self.L3 = Label(self, textvariable = self.vlabel1)
        self.L3.grid(row = 6, column = 0, columnspan = 4)

        #parametri
        self.vlabel2 = DoubleVar()
        self.vlabel2.set(alpha)
        self.L4 = Label(self, text = 'alpha: ')
        self.E1 = Entry(self, textvariable = self.vlabel2, width = 5)

        self.vlabel3 = DoubleVar()
        self.vlabel3.set(beta)
        self.L5 = Label(self, text = 'beta: ')
        self.E2 = Entry(self, textvariable = self.vlabel3, width = 5)

        self.vlabel4 = DoubleVar()
        self.vlabel4.set(gamma)
        self.L6 = Label(self, text = 'gamma: ')
        self.E3 = Entry(self, textvariable = self.vlabel4, width = 5)

        self.vlabel5 = DoubleVar()
        self.vlabel5.set(delta)
        self.L7 = Label(self, text = 'delta: ')
        self.E4 = Entry(self, textvariable = self.vlabel5, width = 5)

        self.vlabel6 = DoubleVar()
        self.vlabel6.set(AT)
        self.L8 = Label(self, text = 'AT: ')
        self.E5 = Entry(self, textvariable = self.vlabel6, width = 5)

        self.vlabel7 = DoubleVar()
        self.vlabel7.set(BT)
        self.L9 = Label(self, text = 'BT: ')
        self.E6 = Entry(self, textvariable = self.vlabel7, width = 5)

        self.vlabel8 = DoubleVar()
        self.vlabel8.set(AD)
        self.L10 = Label(self, text = 'AD: ')
        self.E7 = Entry(self, textvariable = self.vlabel8, width = 5)

        self.vlabel9 = DoubleVar()
        self.vlabel9.set(BD)
        self.L11 = Label(self, text = 'BD: ')
        self.E8 = Entry(self, textvariable = self.vlabel9, width = 5)

        self.vlabel10 = DoubleVar()
        self.vlabel10.set(V)
        self.L12 = Label(self, text = 'V (km/min): ')
        self.E9 = Entry(self, textvariable = self.vlabel10, width = 5)

        self.vlabel11 = IntVar()
        self.vlabel11.set(NUM_OF_SOLUTIONS)
        self.L13 = Label(self, text = 'Vel. populacije: ')
        self.E10 = Entry(self, textvariable = self.vlabel11, width = 5)
        
        self.vlabel12 = IntVar()
        self.vlabel12.set(NUM_OF_ITERATIONS)
        self.L14 = Label(self, text = 'Broj generacija: ')
        self.E11 = Entry(self, textvariable = self.vlabel12, width = 5)

        self.vlabel13 = DoubleVar()
        self.vlabel13.set(MUTATION_RATE)
        self.L15 = Label(self, text = 'Mutation rate: ')
        self.E12 = Entry(self, textvariable = self.vlabel13, width = 5)

        self.L4.grid(row = 1, column = 0)
        self.L5.grid(row = 2, column = 0)
        self.L6.grid(row = 3, column = 0)
        self.L7.grid(row = 4, column = 0)
        self.L8.grid(row = 1, column = 2)
        self.L9.grid(row = 2, column = 2)
        self.L10.grid(row = 3, column = 2)
        self.L11.grid(row = 4, column = 2)
        self.L12.grid(row = 1, column = 4)
        self.L13.grid(row = 2, column = 4)
        self.L14.grid(row = 3, column = 4)
        self.L15.grid(row = 4, column = 4)

        self.E1.grid(row = 1, column = 1)
        self.E2.grid(row = 2, column = 1)
        self.E3.grid(row = 3, column = 1)
        self.E4.grid(row = 4, column = 1)
        self.E5.grid(row = 1, column = 3)
        self.E6.grid(row = 2, column = 3)
        self.E7.grid(row = 3, column = 3)
        self.E8.grid(row = 4, column = 3)
        self.E9.grid(row = 1, column = 5)
        self.E10.grid(row = 2, column = 5)
        self.E11.grid(row = 3, column = 5)
        self.E12.grid(row = 4, column = 5)

        #gumbi
        self.G1 = Button(self, text = 'Ucitaj', command = self.ucitaj).grid(row = 0, column = 4)

        self.G2 = Button(self, text = 'Izracunaj', command = self.izracunaj).grid(row = 5, column = 4)
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
        self.timeMat = times(self.koordinate, self.distMat, self.vlabel10.get())
        self.k_label = ['' for i in range(len(self.koordinate))]
        self.vlabel.set('Ucitavanje uspjesno!')
        return

    def izracunaj(self):
        vals = [self.vlabel2.get(), self.vlabel3.get(), self.vlabel4.get(), self.vlabel5.get(), self.vlabel6.get(), self.vlabel7.get(), self.vlabel8.get(), self.vlabel9.get(), self.vlabel11.get(), self.vlabel12.get(), self.vlabel13.get()]
        value, S, matched, distance, time, riderTime = genAlg(self.riders, self.drivers, self.distMat, self.timeMat, vals)
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
