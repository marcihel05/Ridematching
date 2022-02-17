from settings import *
from solution import *
from rider import *
from driver import *
import random

class Population:
    def __init__(self, riderData, driverData, distMatrix, timeMatrix, vals): 
        self.solutions = []
        self.bestValue = 0
        self.bestSolution = 0
        self.riders = []
        self.drivers = []
        for data in riderData:
            self.riders.append(Rider(data, timeMatrix, vals[4:8]))
        for data in driverData:
            color = (random.randrange(0,255), random.randrange(0,255), random.randrange(0,255))
            self.drivers.append(Driver(distMatrix, timeMatrix, data, vals[4:8], color))
        self.drivers.sort(key = lambda x: x.depTime[0]) #sort drivera po dep time - za insertUnmatched2
        while len(self.solutions) < vals[8]:
            driverCopy = [driver.copy() for driver in self.drivers]
            solution = Solution(distMatrix,timeMatrix, self.riders, driverCopy)
            solution.initialize()
            self.solutions.append(solution)

    
    def selection(self): #binary tournament
        r1 = random.randrange(len(self.solutions))
        r2 = random.randrange(len(self.solutions))
        candidate1 = self.solutions[r1].copy()
        candidate2 = self.solutions[r2].copy()
        if candidate1.fitness <= candidate2.fitness:
            return candidate1
        else:
            return candidate2

    
    def findBestSolutions(self): #pronađi najbolja rješenja (najmanja funkcija dobrote) za elitizam i spremi bestValue (i možda najbolje rješenje)
        minSol = self.solutions[0]
        minVal = minSol.fitness
        secMinSol = 0
        for solution in self.solutions:
            if solution.fitness < minVal:# and solution.fitness < self.bestValue:
                minSol = solution
                minVal = solution.fitness
        self.bestValue = minVal
        self.bestSolution = minSol
        if minSol == self.solutions[0]: secMinSol = self.solutions[1]
        else: secMinSol = self.solutions[0]
        secMinVal = secMinSol.fitness
        for solution in self.solutions:
            if solution.fitness <= secMinVal and self.solutions.index(solution) != self.solutions.index(minSol):
                secMinVal = solution.fitness
                secMinSol = solution
        return minSol.copy(), secMinSol.copy()
    
    def findBestSolutions2(self):
        bestSol = 0
        bestVal = 0
        secBestSol = 0
        for solution in self.solutions:
            if 1/solution.fitness > bestVal:# and solution.fitness < self.bestValue:
                bestSol = solution
                bestVal = 1/solution.fitness
        self.bestValue = bestSol.fitness
        self.bestSolution = bestSol.copy()
        secBestVal = 0
        for solution in self.solutions:
            if 1/solution.fitness >= secBestVal and self.solutions.index(solution) != self.solutions.index(bestSol):
                secBestVal = 1/solution.fitness
                secBestSol = solution
        return bestSol, secBestSol


    def rouletteWheelSelection(self):
        sumOfFitness = 0
        for solution in self.solutions:
            sumOfFitness += solution.fitness
        r = random.random()
        sum = 0
        for solution in self.solutions:
            sum += (1 - solution.fitness/sumOfFitness)
            if sum > r: return solution
        return self.solutions[len(self.solutions)-1]
    
    def evaluate(self, vals):
        for solution in self.solutions:
            solution.calculateFitness(vals)
    
    def findWorstSolution(self):
        sol = 0
        for route in self.solutions:
            if route.fitness > sol:
                sol = route.fitness
        return sol 
        

    
    
