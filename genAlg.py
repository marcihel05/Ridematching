from population import *
from solution import *

from settings import *

def genAlg(riderData, driverData, distMatrix, timeMatrix):
    population = Population(riderData, driverData, distMatrix, timeMatrix)
    #print("imamo populaciju")
    numOfIt = 0
    valueOfFunc = [] #lista vrijednosti funkcije po iteracijama
    bestSolutions = []
    numOfMatched = []
    distance = []
    time = []
    riderTime = []
    while numOfIt < NUM_OF_ITERATIONS: # or while |oldFunc-newFunc| > EPSILON
        #print(numOfIt)
        print(numOfIt)
        newRoutes = []
        #print("best value prije eval " + str(population.bestValue))
        population.evaluate()
        #print("evaluated")
        #print("best value nakon eval " + str(population.bestValue))
        best1, best2 = population.findBestSolutions2()
        #print("sol found")
        #print("best value nakon findBestSol " + str(population.bestValue))
        valueOfFunc.append(population.bestValue)
        bestSolutions.append(best1)
        numOfMatched.append(len(riderData)-len(best1.unmatched))
        distance.append(best1.distance)
        time.append(best1.time)
        riderTime.append(best1.riderTime)
        newRoutes.append(best1)
        newRoutes.append(best2)
        while len(newRoutes) < NUM_OF_SOLUTIONS:
            parent1 = population.selection()
            #parent1 = population.rouletteWheelSelection()
            parent2 = population.selection()
            #parent2 = population.rouletteWheelSelection()
            child1, child2 = parent1.crossover(parent2)
            #child = parent1.crossover2(parent2)
            #child.mutate()
            #newRoutes.append(child)
            child1.mutate()
            child2.mutate()
            newRoutes.append(child1)
            newRoutes.append(child2)
        population.solutions = newRoutes
        #for i in range(2, len(population.solutions)): population.solutions[i].insertUnmatched()
        numOfIt+=1
    return valueOfFunc, bestSolutions, numOfMatched, distance, time, riderTime
        