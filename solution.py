import random
from driver import *
from settings import *

class Solution:
    def __init__(self, riders = [], drivers = []):
        self.routes = drivers #lista Drivera
        self.riders = riders #lista svih Ridera
        self.fitness = 0
        self.unmatched = [] #lista Ridera koji se ne voze
        self.numOfRoutes = 0 #len(self.routes)
    
    def initialize(self): #inicijaliziraj početno rješenje - posloži driver.stops i unmatched stops #DOVRŠITI
       ridersCopy = self.riders
       random.shuffle(self.routes)
       for driver in self.routes:
           for i in range(len(ridersCopy)):
               r = random.randrange(len(ridersCopy))
               rider = ridersCopy[r]
               if driver.taken + rider.numOfPassengers <= driver.capacity: #putnik stane u auto
                   if driver.depTime < rider.depTime and driver.arrivalTime > rider.arrivalTime: #vremenski okvir je okej
                       for stop in driver.stops:
                           #provjeri dal može
                           driver.stops.append([rider,rider.start,0]) #na pravi indeks
                           driver.stops.append([rider,rider.end,1]) #na pravi indeks
                           ridersCopy.remove(rider)
       self.unmatched = ridersCopy
       self.numOfRoutes = len(self.routes)
                   
            
        
    def mutate(self):
        self.pushBackward()
        self.pushForward()
        self.removeInsert()
        self.transfer()
        self.swap()
    
    def pushBackward(self): #first mutation operator
        for route in self.routes:
            r = random.random()
            if r < MUTATION_RATE:
                i = random.randrange(len(route.stops))
    
    def pushForward(self): #seconds mutation operator
        for route in self.routes:
            r = random.random()
            if r < MUTATION_RATE:
                i = random.randrange(len(route.stops))
    
    def removeInsert(self): #third mutation operator
        for route in self.routes:
            r = random.random()
            if r < MUTATION_RATE:
                i = random.randrange(len(route.stops))
                stop = route.stops[i]
                self.unmatched.append(stop[0])
                route.stops.remove(stop)
                route.stops.remove([stop[0], stop[0].end, 1])
                for rider in self.unmatched:
                    self.tryToInsert(rider)
                
    
    def transfer(self): #fourth mutation operator
        for route in self.routes:
            r = random.random()
            if r < MUTATION_RATE:
                i = random.randrange(len(route.stops))
                if self.tryToInsert(self.routes.index(route), route.stops[i][0]):
                    route.stops.remove(route.stops[i])
                    route.stops.remove([route.stops[i][0], route.stops[i][0].end, 1])
    
    def swap(self): #fifth mutation operator
        for route in self.routes:
            r = random.random()
            if r < MUTATION_RATE:
                i = random.randrange(len(route.stops))
                if route.stops[i][0] != route.stops[i+1][0]:
                    route.stops[i], route.stops[i+1] = route.stops[i+1], route.stops[i]

    def crossover(self, otherSolution):
        newSolution1, newSolution2 = self, otherSolution
        routeIndex = random.randrange(self.numOfRoutes)
        for i in range(routeIndex, len(self.routes)):
            newSolution1.routes[i], newSolution2.routes[i] = newSolution2.routes[i], newSolution1.routes[i]
        newSolution1.checkIfFeasibleAfterCrossAndFix(routeIndex)
        newSolution2.checkIfFeasibleAfterCrossAndFix(routeIndex)
        newSolution1.modifyUnmatched()
        newSolution2.modifyUnmatched()
        newSolution1.insertUnmatched()
        newSolution2.insertUnmatched()
        return newSolution1, newSolution2
    
    def calculateFitness(self): #racunaj funkciju dobrote (po onoj formuli) #DOVRŠITI
        val = 0
        dist = 0
        time = 0
        for driver in self.routes:
            dist += driver.calcDistance()
            time += T[driver.id][driver.end] - T[driver.id][driver.start] #T - matrica taka da T[i][j] = vrijeme u koje je vozač s id-em i došao na destinaciju j
        dist*=alpha
        time*=beta
        val+=dist
        val+=time
        return val

    def checkIfFeasibleAfterCrossAndFix(self, routeIndex): #pogledaj dal više vozača ne vozi istog putnika i makni ako ima toga
        for i in range(routeIndex):
            for stop1 in self.routes[i].stops:
                if stop1[2] == 0:
                    rider = stop2
                    for j in range(routeIndex,len(self.routes)):
                        for stop2 in self.routes[j].stops:
                            if stop2 == rider:
                                stop2.remove(rider)
                                stop2.remove([rider[0], rider[1],1])

            
        
    
    def modifyUnmatched(self):
        unmatchedNew = []
        for rider in self.riders:
            exists = False
            for route in self.routes:
                if route.stops.count([rider, rider.start,0]) > 0:
                    exists = True
                    break
            if not exists:
                unmatchedNew.append(rider)
        self.unmatched = unmatchedNew
    
    def insertUnmatched(self):
        for rider in self.unmatched:
            ...#probaj ga negde ubaciti - slično ka inicijalizacija
            for driver in self.routes:
                if driver.taken + rider.numOfPassengers <= driver.capacity: #putnik stane u auto
                   if driver.depTime < rider.depTime and driver.arrivalTime > rider.arrivalTime: #vremenski okvir je okej
                       for stop in driver.stops:
                           #provjeri dal može
                           ...

    def tryToInsert(self, rider, routeIndex = -1):
        for route in self.routes:
            if self.routes.index(route) != routeIndex:

        return False
