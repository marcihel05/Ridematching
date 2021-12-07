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
       ...
            
        
    def mutate(self):
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
        for driver in self.routes:
            dist += driver.calcDistance()
            #driver.calcTime()
        dist*=alpha
        val+=dist
        return val

    def checkIfFeasible(self): #pogledaj dal više vozača ne vozi istog putnika
        for route in self.routes:
            ...
        return True
    
    def fix(self): #popravi ako nije dopustivo
        ...