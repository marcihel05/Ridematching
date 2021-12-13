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
       for i in range(NUM_OF_SOLUTIONS):
           r = random.randrange(0,len(ridersCopy))
           rider = ridersCopy[r]
           ridersCopy.remove(rider)
           random.shuffle(self.routes)
           for driver in self.routes:
               if driver.taken + rider.numOfPassengers <= driver.capacity: #putnik stane u auto
                   if driver.depTime < rider.depTime and driver.arrivalTime > rider.arrivalTime: #vremenski okvir je okej
                       for stop in driver.stops:



            
        
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

    def checkIfFeasible(self): #pogledaj dal više vozača ne vozi istog putnika
        for route in self.routes:
            ...
        return True
    
    def fix(self): #popravi ako nije dopustivo
        ...