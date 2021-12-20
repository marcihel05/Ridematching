import random
from driver import *
from settings import *

class Solution:
    def __init__(self, distMatrix = [],timeMatrix = [], riders = [], drivers = []):
        self.routes = drivers.copy() #lista Drivera
        self.riders = riders.copy() #lista svih Ridera
        self.fitness = 0
        self.unmatched = [] #lista Ridera koji se ne voze
        self.numOfRoutes = 0 #len(self.routes)
        self.D = distMatrix
        self.T = timeMatrix
    
    def initialize(self): #inicijaliziraj početno rješenje - posloži driver.stops i unmatched stops
       ridersCopy = self.riders.copy()
       random.shuffle(self.routes)
       #print("Next solution")
       for driver in self.routes:
           print("ja sam novi vozac")
        #   print("Start")
          # driver.printDriver()
           for l in range(len(ridersCopy)):
               r = random.randrange(len(ridersCopy))
               rider = ridersCopy[r]
               inserted = False
               if driver.depTime[0] < rider.depTime[1] and driver.arrivalTime[1] > rider.arrivalTime[0]: #vremenski okvir je okej
                   if len(driver.stops) == 0:
                       if rider.numOfPassengers <= driver.capacity and driver.checkDistance(rider, 0, 1) and driver.checkTime(rider, 0, 1):
                           time1 = driver.depTime[0] + self.T[driver.start][rider.start]
                           time2 = time1 + self.T[rider.start][rider.end]
                           driver.stops.insert(0, [rider, rider.start, 0, time1, "w"])
                           driver.stops.insert(1, [rider, rider.end, 1, time2, "w"])
                           ridersCopy.pop(r)
                           driver.adjustTimes()
                           inserted = True
                       continue
                   for i in range(-1, len(driver.stops)): #di buš ga pokupil
                        if driver.compareTime(rider, i, 0): #može vremenski na index i
                            k = i+1 #ubaci na k
                            for j in range(k, len(driver.stops)): #di buš ga ostavil
                                if driver.compareTime(rider, j, 1):
                                    if driver.checkCapacity(rider.numOfPassengers, i) and driver.checkDistance(rider, k, j+1) and driver.checkTime(rider, k, j+1):
                                        time1 = driver.stops[k-1][3] + self.T[driver.stops[k-1][1]][rider.start]
                                        time2 = driver.stops[j][3] + self.T[driver.stops[j][1]][rider.end]
                                        driver.stops.insert(k, [rider, rider.start, 0, time1, "w"])
                                        driver.stops.insert(j+1, [rider, rider.end, 1, time2, "w"])
                                        inserted = True
                                        ridersCopy.pop(r)
                                        driver.adjustTimes()
                                        break # prekida for j
                            if inserted: break #prekida for i
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
                ind = self.findIndex(route.stops, stop[0].id)
                if ind > -1:
                    route.stops.pop(ind)
                for rider in self.unmatched:
                    self.tryToInsert2(rider)
                route.calculateTakenSeats()
                
    
    def transfer(self): #fourth mutation operator
        for route in self.routes:
            r = random.random()
            if r < MUTATION_RATE and len(route.stops) > 0: #mutiraj
                i = random.randrange(len(route.stops))
                if self.tryToInsert(route.stops[i][0], self.routes.index(route)):
                    stop = route.stops[i]
                    route.stops.remove(stop)
                    ind = self.findIndex(route.stops, stop[0].id)
                    if ind > -1: route.stops.pop(ind)
                route.calculateTakenSeats()
    
    def swap(self): #fifth mutation operator
        for route in self.routes:
            r = random.random()
            if r < MUTATION_RATE and len(route.stops) > 0: #mutiraj
                i = random.randrange(len(route.stops))
                if i == len(route.stops) -1 : continue
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
        servedReq = delta*len(self.unmatched)
        for driver in self.routes:
            dist += driver.calcDistance()
            if len(driver.stops) == 0: continue
            time += abs(driver.stops[len(driver.stops)-1][3] + self.T[driver.stops[len(driver.stops)-1][1]][driver.end])
            for stop in driver.stops:
                if stop[2] == 0:
                    for i in range(driver.stops.index(stop) + 1, len(driver.stops)):
                        if driver.stops[i][0].id == stop[0].id:
                            riderTime += driver.stops[i][3] - stop[3]
                            break #prekida for i
        dist*=alpha
        time*=beta
        riderTime*=delta
        val+=dist
        val+=time
        val += riderTime
        val+=servedReq
        self.fitness = val
        print(val)

    def checkIfFeasibleAfterCrossAndFix(self, routeIndex): #pogledaj dal više vozača ne vozi istog putnika i makni ako ima toga
        for i in range(routeIndex):
            for stop1 in self.routes[i].stops:
                if stop1[2] == 0:
                    rider = stop1
                    for j in range(routeIndex,len(self.routes)):
                        for stop2 in self.routes[j].stops:
                            if stop2 == rider:
                                self.routes[j].stops.remove(rider)
                                ind = self.findIndex(self.routes[j].stops, rider[0].id)
                                if ind > -1: self.routes[j].stops.pop(ind)
    
    def modifyUnmatched(self):
        unmatchedNew = []
        for rider in self.riders:
            exists = False
            for route in self.routes:
                if route.stops.count([rider, rider.start,0]) > 0:
                    exists = True
            if not exists:
                unmatchedNew.append(rider)
        self.unmatched = unmatchedNew
    
    def insertUnmatched(self):
        for rider in self.unmatched:
            self.tryToInsert(rider)

    def tryToInsert(self, rider, routeIndex = -1): #probaj ga negde staviti - POPRAVITI
        inserted = False
        for driver in self.routes:
            if self.routes.index(driver) != routeIndex:
                for i in range(len(driver.stops)-1):
                    if driver.compareTime(rider, i, 0) and driver.checkCapacity(rider.numOfPassengers, i):      #PROVJERITI
                        if i == 0:
                            time = driver.depTime[0] + self.T[driver.start][rider.start]
                        else:
                            time = driver.stops[i][3] + self.T[driver.stops[i][1]][rider.start]
                        driver.stops.insert(i+1, [rider,rider.start,0,time,"w"]) #na pravi indeks između i i i+1
                        driver.adjustTimes()
                        k = i+1
                        inserted = True
                        break
                    if not inserted:
                        if driver.calculateTakenSeats() + rider.numOfPassengers <= driver.capacity:
                            time = driver.stops[len(driver.stops)-1][3] + self.T[driver.stops[len(driver.stops)-1][1]][rider.start]
                            driver.stops.append([rider,rider.start,0,time,"w"])
                            time = driver.stops[len(driver.stops)-1][3] + self.T[driver.stops[len(driver.stops)-1][1]][rider.end]
                            driver.stops.append([rider,rider.end,1,time,"w"])
                            driver.adjustTimes()
                            return True
                    else:
                        inserted = False
                        for j in range(k, len(driver.stops) - 1): #di buš ga ostavil
                            if driver.compareTime(rider, j, 1):
                                time = driver.stops[j][3] + self.T[driver.stops[j][1]][rider.end]
                                driver.stops.insert(j+1, [rider,rider.end,1,time,"w"]) #na pravi indeks
                                inserted = True
                                driver.adjustTimes()
                                return True
                        if not inserted:
                            time = driver.stops[len(driver.stops)-1][3] + self.T[driver.stops[len(driver.stops)-1][1]][rider.end]
                            driver.stops.append([rider,rider.end,1,time,"w"])
                            driver.adjustTimes()
                            return True
        return False

    def tryToInsert2(self, rider, driver, routeIndex = -1): #probaj ga negde staviti - POPRAVITI
        inserted = False
        if self.routes.index(driver) != routeIndex:
            for i in range(len(driver.stops)-1):
                if driver.compareTime(rider, i, 0) and driver.checkCapacity(rider.numOfPassengers, i):      #PROVJERITI
                    if i == 0:
                        time = driver.depTime[0] + self.T[driver.start][rider.start]
                    else:
                        time = driver.stops[i][3] + self.T[driver.stops[i][1]][rider.start]
                    driver.stops.insert(i+1, [rider,rider.start,0,time,"w"]) #na pravi indeks između i i i+1
                    driver.adjustTimes()
                    k = i+1
                    inserted = True
                    break
                if not inserted:
                    if driver.calculateTakenSeats() + rider.numOfPassengers <= driver.capacity:
                        time = driver.stops[len(driver.stops)-1][3] + self.T[driver.stops[len(driver.stops)-1][1]][rider.start]
                        driver.stops.append([rider,rider.start,0,time,"w"])
                        time = driver.stops[len(driver.stops)-1][3] + self.T[driver.stops[len(driver.stops)-1][1]][rider.end]
                        driver.stops.append([rider,rider.end,1,time,"w"])
                        driver.adjustTimes()
                        return True
                else:
                    inserted = False
                    for j in range(k, len(driver.stops) - 1): #di buš ga ostavil
                        if driver.compareTime(rider, j, 1):
                            time = driver.stops[j][3] + self.T[driver.stops[j][1]][rider.end]
                            driver.stops.insert(j+1, [rider,rider.end,1,time,"w"]) #na pravi indeks
                            inserted = True
                            driver.adjustTimes()
                            return True
                    if not inserted:
                        time = driver.stops[len(driver.stops)-1][3] + self.T[driver.stops[len(driver.stops)-1][1]][rider.end]
                        driver.stops.append([rider,rider.end,1,time,"w"])
                        driver.adjustTimes()
                        return True
        return False
    
    def calcTaken(self):
        for driver in self.routes:
            driver.calculateTakenSeats()
    
    def findIndex(self, stops, id):
        for stop in stops:
            if stop[0].id == id:
                return stops.index(stop)
        return -1
    

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


