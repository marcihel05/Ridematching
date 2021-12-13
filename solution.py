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
    
    def initialize(self): #inicijaliziraj početno rješenje - posloži driver.stops i unmatched stops
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
                   
            
        
    def mutate(self):
        ...
    
    def pushBackward(self): #first mutation operator
        ...
    
    def pushForward(self): #seconds mutation operator
        ...
    
    def removeInsert(self): #third mutation operator
        ...
    
    def transfer(self): #fourth mutation operator
        ...
    
    def swap(self): #fifth mutation operator
        ...

    def crossover(self, otherSolution):
        newSolution1, newSolution2 = Solution(), Solution()
        newSolution1.routes = self.routes
        newSolution2.routes = otherSolution.routes
        routeIndex = random.randrange(self.numOfRoutes)
        newSolution1.routes[routeIndex], newSolution2.routes[routeIndex] = newSolution2.routes[routeIndex], newSolution1.routes[routeIndex]
        if not newSolution1.checkIfFeasibleAfterCross(routeIndex):
            newSolution1.fix(routeIndex)
        if not newSolution2.checkIfFeasibleAfterCross(routeIndex):
            newSolution2.fix(routeIndex)
        return newSolution1, newSolution2
    
    def calculateFitness(self): #racunaj funkciju dobrote (po onoj formuli)
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

    def checkIfFeasibleAfterCrossAndFix(self, routeIndex): #pogledaj dal više vozača ne vozi istog putnik 0a
        for i in range(routeIndex+1):
            for stop1 in self.routes[i].stops:
                if stop1[2] == 0:
                    rider = stop2
                    for j in range(routeIndex+1,len(self.routes)):
                        for stop2 in self.routes[j].stops:
                            if stop2 == rider:
                                stop2.remove(rider)
                                stop2.remove([rider[0], rider[1],1])

            
        
    
    def fix(self): #popravi ako nije dopustivo
        ...