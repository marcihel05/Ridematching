import random

from settings import *

class Solution:
    def __init__(self):
        self.routes = []
        self.fitness = 0
        self.unmatched = []
        self.numOfRoutes = 0 #len(self.routes)
    
    def initialize(self, data): #inicijaliziraj početno rješenje 
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
        ...

    def checkIfFeasible(self):
        ...
    
    def fix(self): #popravi ako nije dopustivo
        ...