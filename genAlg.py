from population import *
from solution import *

from settings import *

def genAlg(riderData, driverData):
    population = Population(riderData, driverData)
    numOfIt = 1
    valueOfFunc = [] #lista vrijednosti funkcije po iteracijama
    bestSolutions = []
    while numOfIt < NUM_OF_ITERATIONS: # or while |oldFunc-newFunc| > EPSILON
        newRoutes = []
        population.evaluate()
        best1, best2 = population.findBestSolutions()
        valueOfFunc.append(population.bestValue)
        bestSolutions.append(population.bestSolution)
        newRoutes.append(best1)
        newRoutes.append(best2)
        while len(newRoutes) < NUM_OF_SOLUTIONS:
            parent1 = population.selection()
            parent2 = population.selection()
            child1, child2 = parent1.crossover(parent2)
            if not child1.checkIfFeasible():
                child1.fix()
            if not child2.checkIfFeasible():
                child2.fix()
            child1.mutate()
            child2.mutate()
            newRoutes.append(child1)
            newRoutes.append(child2)
        population.routes = newRoutes
        numOfIt+=1
        