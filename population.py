from settings import *
from solution import *
from rider import *
from driver import *
import random

class Population:
    def __init__(self, riderData, driverData, distMatrix, timeMarix): 
        self.solutions = []
        self.bestValue = 0
        self.bestSolution = 0
        self.riders = []
        self.drivers = []
        self.initialize(riderData, driverData, distMatrix, timeMarix)

    def initialize(self, riderData, driverData, distMatrix, timeMatrix): #inicijaliziraj početnu populaciju
        #riderData - lista u kojoj su liste s podacima za svakog putnika(id, start, end, depTime, arrTime, brojPutnika)
        #driverData - lista u kojoj su liste s podacima za svakog vozača(id, start, end, depTime, arrTime, kapacitet)
        for data in riderData:
            self.riders.append(Rider(data))
        for data in driverData:
            self.drivers.append(Driver(distMatrix, timeMatrix, data))
        while len(self.solutions) < NUM_OF_SOLUTIONS:
            #for driver in self.drivers:
             #   driver.stops = []
            driverCopy = [driver.copy() for driver in self.drivers]
            riderCopy = [rider.copy() for rider in self.riders]
            solution = Solution(distMatrix,timeMatrix, riderCopy, driverCopy)
            solution.initialize()
            self.solutions.append(solution)
    
    def selection(self): #binary tournament
        r1 = random.randrange(len(self.solutions))
        r2 = random.randrange(len(self.solutions)) # tražimo li da r1!=r2 ?
        candidate1 = self.solutions[r1]
        candidate2 = self.solutions[r2]
        if candidate1.fitness >= candidate2.fitness:
            return candidate1
        else:
            return candidate2

    
    def findBestSolutions(self): #pronađi najbolja rješenja (najmanja funkcija dobrote) za elitizam i spremi bestValue (i možda najbolje rješenje)
        minSol = self.solutions[0]
        minVal = minSol.fitness
        secMinSol = 0
        for solution in self.solutions:
            if solution.fitness < minVal:
                minSol = solution
                minVal = solution.fitness
        self.bestValue = minVal
        self.bestSolution = minSol
        if minSol == self.solutions[0]:
            secMinSol = self.solutions[1]
        else:
            secMinSol = self.solutions[0]
        minVal = secMinSol.fitness
        for solution in self.solutions:
            if solution.fitness < minVal and solution != minSol:
                minVal = solution.fitness
                secMinSol = solution
        return minSol, secMinSol

    def rouletteWheelSelection(self):
        sumOfFitness = 0
        for solution in self.solutions:
            sumOfFitness += solution.fitness
        r = random.uniform(0,1)
        sum = 0
        for solution in self.solutions:
            sum += (solution.fitness/sumOfFitness)
            if sum > r:
                return solution
        return self.solutions[len(self.solutions)-1]
    
    def evaluate(self):
        for solution in self.solutions:
            solution.calculateFitness()
        

    
    