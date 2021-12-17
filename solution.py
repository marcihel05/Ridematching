import random
from driver import *
from settings import *
from matrices import *

class Solution:
    def __init__(self, distMatrix = [],timeMatrix = [], riders = [], drivers = []):
        self.routes = drivers.copy() #lista Drivera
        self.riders = riders.copy() #lista svih Ridera
        self.fitness = 0
        self.unmatched = [] #lista Ridera koji se ne voze
        self.numOfRoutes = 0 #len(self.routes)
        self.D = distMatrix
        self.T = timeMatrix
    
    def initialize(self): #inicijaliziraj početno rješenje - posloži driver.stops i unmatched stops #DODATI PROVJERU JE LI FIZIČKI MOGUĆE DOĆI S JEDNE LOKACIJE NA SLJEDEĆU U ZADANOM VREMENU
       ridersCopy = self.riders.copy()
       random.shuffle(self.routes)
       #print("Next solution")
       for driver in self.routes:
        #   print("Start")
          # driver.printDriver()
           for i in range(len(ridersCopy)):
         #      print(i)
               r = random.randrange(len(ridersCopy))
               rider = ridersCopy[r]
               if driver.depTime < rider.depTime and driver.arrivalTime > rider.arrivalTime: #vremenski okvir je okej
                    inserted = False
                    for i in range(-1, len(driver.stops) - 1): #di buš ga pokupil
                        if driver.compareTime(rider, i, 0) and driver.checkCapacity(rider.numOfPassengers, i):
                            driver.stops.insert(i+1, [rider,rider.start,0]) #na pravi indeks između i i i+1
                            k = i+1
                            inserted = True
                            break
                    if not inserted:
                        if driver.calculateTakenSeats() + rider.numOfPassengers <= driver.capacity:
                            driver.stops.append([rider,rider.start,0])
                            driver.stops.append([rider,rider.end,1])
                            ridersCopy.pop(r)
                    else:
                        inserted = False
                        for j in range(k, len(driver.stops) - 1): #di buš ga ostavil
                            if driver.compareTime(rider, j, 1):
                                driver.stops.insert(j+1, [rider,rider.end,1]) #na pravi indeks
                                inserted = True
                                ridersCopy.pop(r)
                                break
                        if not inserted:
                            driver.stops.append([rider,rider.end,1])
                            ridersCopy.pop(r)
          # print("End")
           #driver.printDriver()
       self.unmatched = ridersCopy.copy()
       self.numOfRoutes = len(self.routes)
       #self.calcTaken()         
            
        
    def mutate(self):
        #self.pushBackward()
        #self.pushForward()
        self.removeInsert()
        self.transfer()
        self.swap()
    
    def pushBackward(self): #first mutation operator
        for route in self.routes:
            r = random.random()
            if r < MUTATION_RATE and len(route.stops) > 0: #mutiraj
                i = random.randrange(len(route.stops))

                route.calculateTakenSeats()
    
    def pushForward(self): #seconds mutation operator
        for route in self.routes:
            r = random.random()
            if r < MUTATION_RATE and len(route.stops) > 0: #mutiraj
                i = random.randrange(len(route.stops))
                
                route.calculateTakenSeats()
    
    def removeInsert(self): #third mutation operator
        for route in self.routes:
            r = random.random()
            if r < MUTATION_RATE and len(route.stops) > 0:  #mutiraj
                i = random.randrange(len(route.stops))
                stop = route.stops[i]
                self.unmatched.append(stop[0])
                route.stops.remove(stop)
                route.stops.remove([stop[0], stop[0].end, 1])
                for rider in self.unmatched:
                    self.tryToInsert(rider)
                route.calculateTakenSeats()
                
    
    def transfer(self): #fourth mutation operator
        for route in self.routes:
            r = random.random()
            if r < MUTATION_RATE and len(route.stops) > 0: #mutiraj
                i = random.randrange(len(route.stops))
                if self.tryToInsert(route.stops[i][0], self.routes.index(route)):
                    route.stops.remove(route.stops[i])
                    route.stops.remove([route.stops[i][0], route.stops[i][0].end, 1])
                route.calculateTakenSeats()
    
    def swap(self): #fifth mutation operator
        for route in self.routes:
            r = random.random()
            if r < MUTATION_RATE and len(route.stops) > 0: #mutiraj
                i = random.randrange(len(route.stops))
                if route.stops[i][0] != route.stops[i+1][0]:
                    route.stops[i], route.stops[i+1] = route.stops[i+1], route.stops[i]

    def crossover(self, otherSolution):
        newSolution1, newSolution2 = self.copy(), otherSolution.copy()
        routeIndex = random.randrange(self.numOfRoutes)
        for i in range(routeIndex, len(self.routes)):
            newSolution1.routes[i], newSolution2.routes[i] = newSolution2.routes[i], newSolution1.routes[i]
        newSolution1.checkIfFeasibleAfterCrossAndFix(routeIndex)
        newSolution2.checkIfFeasibleAfterCrossAndFix(routeIndex)
        newSolution1.modifyUnmatched()
        newSolution2.modifyUnmatched()
        newSolution1.insertUnmatched()
        newSolution2.insertUnmatched()
        return newSolution1, newSolution2
    
    def calculateFitness(self): #racunaj funkciju dobrote (po onoj formuli) #DOVRŠITI
        val = 0
        dist = 0
        time = 0
        riderTime = 0
        servedReq = delta*(len(self.riders) - len(self.unmatched))
        for driver in self.routes:
            dist += driver.calcDistance()
            time += abs(T[driver.id][driver.end] - T[driver.id][driver.start]) #T - matrica taka da T[i][j] = vrijeme u koje je vozač s id-em i došao na destinaciju j
            for stop in driver.stops:
                if stop[2] == 0:
                    riderTime += abs(T[driver.id][stop[0].end] - T[driver.id][stop[1]])
        dist*=alpha
        time*=beta
        riderTime*=delta
        val+=dist
        val+=time
        val += riderTime
        val+=servedReq
        self.fitness = val

    def checkIfFeasibleAfterCrossAndFix(self, routeIndex): #pogledaj dal više vozača ne vozi istog putnika i makni ako ima toga
        for i in range(routeIndex):
            for stop1 in self.routes[i].stops:
                if stop1[2] == 0:
                    rider = stop1
                    for j in range(routeIndex,len(self.routes)):
                        for stop2 in self.routes[j].stops:
                            if stop2 == rider:
                                self.routes[j].stops.remove(rider)
                                self.routes[j].stops.remove([rider[0], rider[1],1])

    
    def modifyUnmatched(self):
        unmatchedNew = []
        for rider in self.riders:
            exists = False
            for route in self.routes:
                if route.stops.count([rider, rider.start,0]) > 0:
                    exists = True
                    break
            if not exists:
                unmatchedNew.append(rider)
        self.unmatched = unmatchedNew
    
    def insertUnmatched(self):
        for rider in self.unmatched:
            self.tryToInsert(rider)

    def tryToInsert(self, rider, routeIndex = -1): #probaj ga negde staviti
        inserted = False
        for driver in self.routes:
            if self.routes.index(driver) != routeIndex:
                for i in range(len(driver.stops)-1):
                    if driver.compareTime(rider, i, 0) and driver.checkCapacity(rider.numOfPassengers, i):
                            driver.stops.insert(i+1, [rider,rider.start,0]) #na pravi indeks između i i i+1
                            k = i+1
                            inserted = True
                            break
                    if not inserted:
                        if driver.calculateTakenSeats() + rider.numOfPassengers <= driver.capacity:
                            driver.stops.append([rider,rider.start,0])
                            driver.stops.append([rider,rider.end,1])
                    else:
                        inserted = False
                        for j in range(k, len(driver.stops) - 1): #di buš ga ostavil
                            if driver.compareTime(rider, j, 1):
                                driver.stops.insert(j+1, [rider,rider.end,1]) #na pravi indeks
                                inserted = True
                                return True
                        if not inserted:
                            driver.stops.append([rider,rider.end,1])
                            return True
        return False
    
    def calcTaken(self):
        for driver in self.routes:
            driver.calculateTakenSeats()
    

    def copy(self):
        new = Solution()
        new.unmatched = self.unmatched.copy()
        new.riders = self.riders.copy()
        new.routes = [driver.copy() for driver in self.routes]
        new.fitness = self.fitness
        new.numOfRoutes = self.numOfRoutes
        new.D = self.D
        new.T = self.T
        return new


