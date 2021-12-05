from settings import *
from solution import *
from rider import *
from driver import *

class Population:
    def __init__(self, riderData, driverData): 
        self.solutions = []
        self.bestValue = 0
        self.bestSolution = 0
        self.riders = []
        self.drivers = []
        self.initialize(riderData, driverData)

    def initialize(self, riderData, driverData): #inicijaliziraj početnu populaciju
        #riderData - lista u kojoj su liste s podacima za svakog putnika(id, start, end, depTime, arrTime)
        #driverData - lista u kojoj su liste s podacima za svakog vozača(id, start, end, depTime, arrTime, kapacitet)
        for data in riderData:
            self.riders.append(Rider(data))
        for data in driverData:
            self.drivers.append(Driver(data))
        while len(self.solutions) < NUM_OF_SOLUTIONS:
            solution = Solution(self.riders, self.drivers)
            solution.initialize()
            self.solutions.append(solution)
    
    def selection(self):
        ...

    
    def findBestSolutions(self): #pronađi najbolja rješenja (najmanja funkcija dobrote) za elitizam i spremi bestValue (i možda najbolje rješenje)
        maxSol = self.solutions[0]
        maxVal = maxSol.fitness
        secMaxSol = 0
        for solution in self.solutions:
            if solution.fitness > maxVal:
                maxSol = solution
                maxVal = solution.fitness
        self.bestValue = maxVal
        self.bestSolution = maxSol
        if maxSol == self.solutions[0]:
            secMaxSol = self.solutions[1]
        else:
            secMaxSol = self.solutions[0]
        maxVal = secMaxSol.fitness
        for solution in self.solutions:
            if solution.fitness > maxVal and solution != maxSol:
                maxVal = solution.fitness
                secMaxSol = solution
        return maxSol, secMaxSol
        
    
    def evaluate(self):
        for solution in self.solutions:
            solution.calculateFitness()
    
    def makeNewSolutions(self):

    
    