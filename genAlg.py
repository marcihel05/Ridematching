from population import *
from solution import *

from settings import *

def genAlg(riderData, driverData, distMatrix, timeMatrix):
    population = Population(riderData, driverData, distMatrix, timeMatrix)
    #print("imamo populaciju")
    numOfIt = 1
    valueOfFunc = [] #lista vrijednosti funkcije po iteracijama
    bestSolutions = []
    while numOfIt < NUM_OF_ITERATIONS: # or while |oldFunc-newFunc| > EPSILON
        #print(numOfIt)
        print(numOfIt)
        newRoutes = []
        #print("best value prije eval " + str(population.bestValue))
        population.evaluate()
        #print("best value nakon eval " + str(population.bestValue))
        best1, best2 = population.findBestSolutions()
        #print("best value nakon findBestSol " + str(population.bestValue))
        valueOfFunc.append(population.bestValue)
        bestSolutions.append(population.bestSolution)
        newRoutes.append(best1)
        newRoutes.append(best2)
        while len(newRoutes) < NUM_OF_SOLUTIONS:
            parent1 = population.selection()
            parent2 = population.selection()
            child1, child2 = parent1.crossover(parent2)
            child1.mutate()
            child2.mutate()
            newRoutes.append(child1)
            newRoutes.append(child2)
        population.routes = newRoutes
        numOfIt+=1
    return valueOfFunc, bestSolutions
        