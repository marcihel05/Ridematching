import random
from driver import *
from settings import *
from math import ceil

class Solution:
    def __init__(self, distMatrix = [],timeMatrix = [], riders = [], drivers = []):
        self.routes = drivers #lista Drivera
        self.riders = riders #lista svih Ridera
        self.fitness = 0
        self.unmatched = [] #lista Ridera koji se ne voze
        self.numOfRoutes = 0 #len(self.routes)
        self.distance = 0
        self.time = 0
        self.riderTime = 0
        self.D = distMatrix
        self.T = timeMatrix
    
    def initialize(self): #inicijaliziraj početno rješenje - posloži driver.stops i unmatched stops
       #ridersCopy = [rider.copy() for rider in self.riders]
       ridersCopy = self.riders.copy()
       #print("Next solution")
       driversCopy = [i for i in range(len(self.routes))]
       while len(driversCopy):
           rnd = random.randrange(len(driversCopy))
           ind = driversCopy[rnd]
           driversCopy.remove(ind)
           driver = self.routes[ind]
           random.shuffle(ridersCopy)
       #for driver in self.routes:
           #print("ja sam novi vozac")
        #   print("Start")
          # driver.printDriver()
           #for l in range(len(ridersCopy)):
           for rider in ridersCopy:
               #r = random.randrange(len(ridersCopy))
               #rider = ridersCopy[r]
               inserted = False
               if driver.depTime[0] < rider.depTime[1] and driver.arrivalTime[1] > rider.arrivalTime[0]: #vremenski okvir je okej
                   if len(driver.stops) == 0:
                       if rider.numOfPassengers <= driver.capacity and driver.checkDistance(rider, 0, 1) and driver.checkTime(rider, 0, 1):
                           time1 = driver.startTime + self.T[driver.start][rider.start]
                           if time1 > rider.depTime[1]: 
                               print("krivo radi")
                               continue
                           w1 = max(0, rider.depTime[0] - driver.depTime[0] - self.T[driver.start][rider.start])
                           time2 = time1 + self.T[rider.start][rider.end] +w1
                           driver.stops.insert(0, [rider, rider.start, 0, time1, w1])
                           driver.stops.insert(1, [rider, rider.end, 1, time2, 0])
                           ridersCopy.remove(rider)
                           #ridersCopy.pop(r)
                           driver.adjustTimes()
                           inserted = True
                   else:
                        for i in range(-1, len(driver.stops)): #di buš ga pokupil
                            if driver.compareTime(rider, i, 0): #može vremenski na index i
                                k = i+1 #ubaci na k
                                for j in range(k, len(driver.stops)): #di buš ga ostavil
                                    if driver.compareTime(rider, j, 1):
                                        #cap = driver.checkCapacity(rider.numOfPassengers, i)
                                        #dist = driver.checkDistance(rider, k, j+1)
                                        #time = driver.checkTime(rider, k, j+1)
                                    #print("cap " + str(cap))
                                    #print("dist " + str(dist))
                                    #print("time " + str(time))
                                        if driver.checkCapacity(rider.numOfPassengers, i) and driver.checkDistance(rider, k, j+1) and driver.checkTime(rider, k, j+1):
                                        #if cap and dist and time:
                                            time1 = max(rider.depTime[0], driver.stops[k-1][3] + driver.stops[k-1][4] + self.T[driver.stops[k-1][1]][rider.start])
                                            if time1 > rider.depTime[1]: continue
                                            w1 = max(0, rider.depTime[0] - time1)
                                            time2 = driver.stops[j][3] + driver.stops[j][4] + self.T[driver.stops[j][1]][rider.end]
                                            if time2 > rider.arrivalTime[1]: continue
                                            driver.stops.insert(k, [rider, rider.start, 0, time1, w1])
                                            driver.stops.insert(j+1, [rider, rider.end, 1, time2, 0])
                                            inserted = True
                                            #ridersCopy.pop(r)
                                            ridersCopy.remove(rider)
                                            driver.adjustTimes()
                                            break # prekida for j
                                if inserted: break #prekida for i
          # print("End")
           #driver.printDriver()
       self.unmatched = ridersCopy
       self.numOfRoutes = len(self.routes)
       #self.calcTaken() 
    
       #sort drivera po dep time - za insertUnmatched2
       self.routes.sort(key = lambda x: x.depTime[0])
            
        
    def mutate(self, rate):
        self.pushBackward(rate) #popraviti 
        self.pushForward(rate) #popraviti
        self.removeInsert(rate)
        self.transfer(rate)
        self.swap(rate) #postaviti provjere
    
    def pushBackward(self, rate): #first mutation operator #dodaj vozača
        #for route in self.routes:
        l = random.sample(range(0,len(self.routes)),50)
        for i in l:
            route = self.routes[i]
            r = random.random()
            if r < rate and len(route.stops) < 0: #mutiraj
                i = random.randrange(-1, len(route.stops))
                if i == -1:
                    if route.startTime - route.depTime[0] > 0: pb = ceil(random.uniform(0, route.startTime - route.depTime[0]))
                    else: continue
                    route.startTime = route.startTime - pb
                else:
                    stop = route.stops[i]
                    if stop[2] == 1:
                        ind = self.findIndex2(route.stops,stop[0].id)
                        stop = route.stops[ind]
                    if stop[3] - stop[0].depTime[0] > 0: pb = ceil(random.uniform(0, ceil(stop[3] - stop[0].depTime[0])))
                    else: continue
                    if route.startTime - pb < route.depTime[0]: continue
                    stop[3] = stop[3] - pb 
                    stop[4] = max(0, stop[0].depTime[0] - stop[3])
                route.pushBackwardAll(i+1, pb)
                #route.calculateTakenSeats()
            elif r < rate and not len(route.stops):
                 if route.startTime - route.depTime[0] > 0: pb = ceil(random.uniform(0, route.startTime - route.depTime[0]))
                 else: continue
                 if route.endTime - pb < route.arrivalTime[0]: continue
                 route.startTime -= pb
                 route.endTime -= pb
    
    def pushForward(self, rate): #second mutation operator 
        #for route in self.routes:
        l = random.sample(range(0,len(self.routes)),50)
        for i in l:
            route = self.routes[i]
            r = random.random()
            if r < rate and len(route.stops) < 0: #mutiraj
                nope = False
                i = random.randrange(-1, len(route.stops))
                if i == -1:
                    #print("pomicem drivera napred")
                    #print("start prije pf " + str(route.startTime) + " id " + str(route.id))
                    if route.depTime[1] - route.startTime > 0: 
                        pf = ceil(random.uniform(0, route.depTime[1] - route.startTime))
                        if pf + route.endTime > route.arrivalTime[1]: continue
                        for stop in route.stops:
                            if stop[2] == 0:
                                if stop[2] + pf > stop[0].depTime[1]:
                                    nope = True
                                    break
                            else:
                                if stop[2] + pf > stop[0].arrivalTime[1]:
                                    nope = True
                                    break
                        if nope: continue
                    else: continue
                    route.startTime = route.startTime + pf
                    #print("start nakon pf " + str(route.startTime) + " id " + str(route.id) )
                else:
                    stop = route.stops[i]
                    if stop[2] == 1:
                        ind = self.findIndex2(route.stops,stop[0].id)
                        stop = route.stops[ind]
                    #if stop[2] == 1: return
                    if stop[0].depTime[1] - stop[3] > 0: 
                        pf = ceil(random.uniform(0, stop[0].depTime[1] - stop[3]))
                        if pf + route.endTime > route.arrivalTime[1]: continue
                        for i in range(route.stops.index(stop), len(route.stops)):
                            stop = route.stops[i]
                            if stop[2] == 0:
                                if stop[2] + pf > stop[0].depTime[1]:
                                    nope = True
                                    break
                                else:
                                    if stop[2] + pf > stop[0].arrivalTime[1]:
                                        nope = True
                                        break
                        if nope: continue
                    else: continue
                    #if stop[3] + stop[4] > stop[0].depTime[1]: print("prekasno prije pb") 
                    #if stop[3] + stop[4] < stop[0].depTime[0]: print("prerano prije pb") 
                    stop[3] = stop[3] + pf
                    stop[4] = max(0, stop[0].depTime[0] - stop[3])
                    #if stop[3] + stop[4] < stop[0].depTime[0]: print("prerano")
                    #if stop[3] +stop[4] > stop[0].depTime[1]: print("prekasno")
                    
                route.pushForwardAll(i+1, pf)
                #route.calculateTakenSeats()
            elif r < rate and not len(route.stops):
                if route.depTime[1] - route.startTime > 0: 
                    pf = ceil(random.uniform(0, route.depTime[1] - route.startTime))
                    if pf + route.endTime > route.arrivalTime[1]: continue
                    else:
                        route.startTime += pf
                        route.endTime += pf


            
    
    def removeInsert(self, rate): #third mutation operator
        #for route in self.routes:
        l = random.sample(range(0,len(self.routes)),50)
        for i in l:
            route = self.routes[i]
            r = random.random()
            if r < rate and len(route.stops) > 0:  #mutiraj
                i = random.randrange(len(route.stops))
                stop = route.stops[i]
                #if stop[2] == 1: ind = self.findIndex2(route.stops, stop[0].id)
                #else: ind = self.findIndex(route.stops, stop[0].id)
                    #stop = route.stops[ind]
                self.unmatched.append(stop[0])
                route.stops.remove(stop)
                if stop[2] == 1: ind = self.findIndex2(route.stops, stop[0].id)
                else: ind = self.findIndex(route.stops, stop[0].id)
                if ind > -1: route.stops.pop(ind)
                else: print("something's wrong in remove insert " +str(self.routes.index(route)))
                route.adjustTimes()
                random.shuffle(self.unmatched)
                for rider in self.unmatched:
                    #provjera vremenskih okvira prije insert
                    if route.depTime[0] < rider.depTime[1] and route.arrivalTime[1] > rider.arrivalTime[0] and self.tryToInsert2(rider, route): self.unmatched.remove(rider)
                        #route.adjustTimes()
            elif r < rate and not len(route.stops):
                random.shuffle(self.unmatched)
                for rider in self.unmatched:
                #provjera vremenskih okvira prije insert
                    if route.depTime[0] < rider.depTime[1] and route.arrivalTime[1] > rider.arrivalTime[0] and self.tryToInsert2(rider, route): self.unmatched.remove(rider)
                        
                        #route.adjustTimes()
                #route.calculateTakenSeats()
                #self.modifyUnmatched()

                
    
    def transfer(self, rate): #fourth mutation operator
        #for route in self.routes:
        l = random.sample(range(0,len(self.routes)),50)
        for i in l:
            route = self.routes[i]
            r = random.random()
            if r < rate and len(route.stops) > 0: #mutiraj
                i = random.randrange(len(route.stops))
                stop = route.stops[i]
                #if stop[2] == 1: ind = self.findIndex2(route.stops, stop[0].id)
                #else: ind = self.findIndex(route.stops, stop[0].id)
                    #stop = route.stops[ind]
                if self.tryToInsert(stop[0], route.id):
                    route.stops.remove(stop)
                    if stop[2] == 1: ind = self.findIndex2(route.stops, stop[0].id)
                    else: ind = self.findIndex(route.stops, stop[0].id)
                    if ind > -1: route.stops.pop(ind)
                    else: print("something's wrong in transfer " + str(self.routes.index(route)))
                    route.adjustTimes()
                    #route.calculateTakenSeats()
    
    def swap(self, rate): #fifth mutation operator
        #for route in self.routes:
        l = random.sample(range(0,len(self.routes)),50)
        for i in l:
            route = self.routes[i]
            r = random.random()
            if r < rate and len(route.stops) > 0: #mutiraj
                i = random.randrange(len(route.stops))
                if i == len(route.stops) -1 : i -= 1
                if route.stops[i][0].id != route.stops[i+1][0].id:
                    #print("swap: " + str(route.id))
                    #route.stops[i], route.stops[i+1] = route.stops[i+1].copy(), route.stops[i].copy()
                    s1 = route.stops[i].copy()
                    s2 = route.stops[i+1].copy()
                    route.stops[i] = s2
                    route.stops[i+1] = s1
                    route.adjustTimes()

    def crossover(self, otherSolution):
        newSolution1 = self.copy()
        newSolution2 = otherSolution.copy()
        routeIndex = random.randrange(self.numOfRoutes)
        match1 = set()
        match2 = set()
        for i in range(routeIndex):
            for s in newSolution1.routes[i].stops:
                match1.add(s[0])
            for s in newSolution2.routes[i].stops:
                match2.add(s[0])
        for i in range(routeIndex, len(self.routes)):
            r1 = newSolution1.routes[i].copy()
            r2 = newSolution2.routes[i].copy()
            newSolution1.routes[i] = r2
            newSolution2.routes[i] = r1
            for s in newSolution1.routes[i].stops:
                match1.add(s[0])
            for s in newSolution2.routes[i].stops:
                match2.add(s[0])
        newSolution1.checkIfFeasibleAfterCrossAndFix(routeIndex)
        newSolution2.checkIfFeasibleAfterCrossAndFix(routeIndex)
        #newSolution1.modifyUnmatched()
        #newSolution2.modifyUnmatched()
        newSolution1.unmatched = list(set(self.riders)-match1)
        newSolution2.unmatched = list(set(self.riders)-match2)
        #newSolution1.insertUnmatched()
        #newSolution2.insertUnmatched()
        newSolution1.insertUnmatched2()         #iteracija po unmacthed umjesto po routes
        newSolution2.insertUnmatched2()
        return newSolution1, newSolution2
    
    def crossover2(self, otherSolution):
        newSolution = self.copy()
        routeIndex =  random.randrange(self.numOfRoutes)
        for i in range(routeIndex, len(self.routes)):
            newSolution.routes[i] = otherSolution.routes[i].copy()
        newSolution.checkIfFeasibleAfterCrossAndFix(routeIndex)
        newSolution.modifyUnmatched()
        newSolution.insertUnmatched()
        return newSolution
    
    def calculateFitness(self, vals): #racunaj funkciju dobrote (po onoj formuli) #DOVRŠITI
        val = 0
        dist = 0
        maxDist = 0
        time = 0
        maxTime = 0
        riderTime = 0
        maxRiderTime = 0
        alpha = vals[0]
        beta = vals[1]
        gamma = vals[2]
        delta = vals[3]
        unservedReq = delta*len(self.unmatched)/len(self.riders)
        for driver in self.routes:
            d = driver.calcDistance()
            dist += d
            maxDist += driver.maxDist
            t = (driver.endTime - driver.startTime)
            time += t
            #if t < 0: print("prefletno driver " + str(driver.id))
            maxTime += driver.maxTime
            if len(driver.stops) == 0: continue
            for stop in driver.stops:
                if stop[2] == 0:
                    ind = self.findIndex(driver.stops, stop[0].id)
                    #for i in range(driver.stops.index(stop) + 1, len(driver.stops)):
                        #if driver.stops[i][0].id == stop[0].id and driver.stops[i][2] == 1:
                    riderTime += (driver.stops[ind][3] - stop[3] - stop[4])
                    maxRiderTime += stop[0].maxTime
                    #break #prekida for i
        self.distance = dist
        self.time = time
        self.riderTime = riderTime
        if(time < 0): print("time: " + str(time))
        if(riderTime < 0): print("riderTime: " + str(riderTime))
        dist /= maxDist
        time /= maxTime
        riderTime /= maxRiderTime
        dist*=alpha
        time*=beta
        riderTime*=gamma
        val+=dist
        val+=time
        val += riderTime
        val+=unservedReq
        self.fitness = val
        #print(val)

    def checkIfFeasibleAfterCrossAndFix(self, routeIndex): #pogledaj dal više vozača ne vozi istog putnika i makni ako ima toga
        for i in range(routeIndex):
            for stop1 in self.routes[i].stops:
                if stop1[2] == 0:
                    rider = stop1[0]
                    for j in range(routeIndex,len(self.routes)):
                        for stop2 in self.routes[j].stops:
                            if stop2[0].id == rider.id and stop2[2] == 0:
                                #print("micemo ga")
                                ind0 =self.findIndex2(self.routes[j].stops, rider.id)
                                #self.routes[j].stops.remove(rider)
                                self.routes[j].stops.pop(ind0)
                                ind = self.findIndex(self.routes[j].stops, rider.id)
                                if ind > -1: self.routes[j].stops.pop(ind)
                                #else: print("smoething's wrong")
                                self.routes[j].adjustTimes()
    
    def modifyUnmatched(self):
        unmatchedNew = []
        for rider in self.riders:
            exists = False
            for route in self.routes:
                if route.exists(rider.id):
                    exists = True
                    break #prekini for stop
            if not exists:
                unmatchedNew.append(rider)
        self.unmatched = unmatchedNew.copy()
    
    def insertUnmatched(self):
        #l = [i for i in range(len(self.unmatched))]
        #while len(l):
         #   rnd = random.randrange(len(l))
          #  rider = self.unmatched[l[rnd]]
           # for i in range(rnd+1, len(l)): l[i] -=1
            #l.remove(l[rnd])
        #random.shuffle(self.unmatched)
        self.unmatched.sort(key = lambda x: x.depTime[0])
        for driver in self.routes:
        for rider in self.unmatched:
            #if self.tryToInsert(rider): self.unmatched.remove(rider)
            if rider.arrivalTime[0] > driver.arrivalTime[1]:
                break
            if rider.depTime[1] < driver.depTime[0]:
                continue
            if self.tryToInsert2(rider,driver): self.unmatched.remove(rider)
            #self.tryToInsert(rider)
        #self.modifyUnmatched()
    
    def insertUnmatched2(self):
        for rider in self.unmatched:
            drivers_sublist = []
            for driver in self.routes:
                if rider.arrivalTime[0] > driver.arrivalTime[1]:
                    break
                if rider.depTime[1] < driver.depTime[0]:
                    continue
                drivers_sublist.append(driver)
            if len(drivers_sublist) == 0: continue 
                
            #random broj drivera (od onih koji odgovaraju) u koje ćemo pokusati ubaciti
            r = random.randint(len(drivers_sublist)//4, len(drivers_sublist)//2)
            #random sample indeksa duljine r
            sample = random.sample(range(0,len(drivers_sublist)), r)
            for k in sample:
                if self.tryToInsert2(rider, drivers_sublist[k]):
                    self.unmatched.remove(rider)
                    break
            
            if rider not in self.unmatched: continue
            #ako ridera nismo ubacili, pokusavamo u ostatku liste
            new_try = set(range(len(drivers_sublist))) - set(sample)
            for k in new_try:
                if self.tryToInsert2(rider, drivers_sublist[k]):
                    self.unmatched.remove(rider)
                    break

        #varijanta samo sa random dijelom liste - otprilike ista brzina i rezultat
        #r = random.randint(len(drivers_sublist)//4, 3*len(drivers_sublist)//4)
        #sample = random.sample(range(0,len(drivers_sublist)), r)
        #for k in sample:
            #if self.tryToInsert2(rider, drivers_sublist[k]):
                #self.unmatched.remove(rider)
                #break

    def tryToInsert(self, rider, routeId = -1): #probaj ga negde staviti - POPRAVITI
        driversCopy = [i for i in range(len(self.routes))]
        while len(driversCopy):
        #for driver in self.routes:
            rnd = random.randrange(len(driversCopy))
            ind = driversCopy[rnd]
            driversCopy.remove(ind)
            driver = self.routes[ind]
            #if driver.id == routeId: print(" driver id je " + str(driver.id) + " a routeId je " + str(routeId))
            if driver.id != routeId:
                if driver.depTime[0] < rider.depTime[1] and driver.arrivalTime[1] > rider.arrivalTime[0]: #vremenski okvir je okej
                   if len(driver.stops) == 0:
                       if rider.numOfPassengers <= driver.capacity and driver.checkDistance(rider, 0, 1) and driver.checkTime(rider, 0, 1):
                           time1 = driver.startTime + self.T[driver.start][rider.start]
                           w1 = max(0, rider.depTime[0] - driver.startTime - self.T[driver.start][rider.start])
                           time2 = time1 + self.T[rider.start][rider.end] +w1
                           driver.stops.insert(0, [rider, rider.start, 0, time1, w1])
                           driver.stops.insert(1, [rider, rider.end, 1, time2, 0])
                           driver.adjustTimes()
                           #print("inserted new")
                           return True
                   else:
                        for i in range(-1, len(driver.stops)): #di buš ga pokupil
                            if driver.exists(rider.id): 
                                print("ovo se nesmi desiti try1")
                                print(" driver id je " + str(driver.id) + " a routeId je " + str(routeId))
                                return True
                            if driver.compareTime(rider, i, 0): #može vremenski na index i
                                k = i+1 #ubaci na k
                                for j in range(k, len(driver.stops)): #di buš ga ostavil
                                    if driver.compareTime(rider, j, 1):
                                        #dist = driver.checkDistance(rider, k, j+1)
                                        #time = driver.checkTime(rider, k, j+1)
                                    #if not dist: print("kilometri su problem")
                                    #if not time: print("vrijeme je problem")
                                        if driver.checkCapacity(rider.numOfPassengers, i) and driver.checkDistance(rider, k, j+1) and driver.checkTime(rider, k, j+1):
                                            time1 = driver.stops[k-1][3] + self.T[driver.stops[k-1][1]][rider.start]
                                            w1 = max(0, rider.depTime[0] - driver.stops[k-1][3] - self.T[driver.stops[k-1][1]][rider.start])
                                            time2 = driver.stops[j][3] + self.T[driver.stops[j][1]][rider.end]
                                            driver.stops.insert(k, [rider, rider.start, 0, time1, w1])
                                            driver.stops.insert(j+1, [rider, rider.end, 1, time2, 0])
                                            driver.adjustTimes()
                                            #print("inserted new")
                                            return True
        return False

    def tryToInsert2(self, rider, driver):
        #provjera maxdist
        if self.D[driver.start][rider.start] + self.D[rider.start][rider.end] + self.D[rider.end][driver.end] <= driver.maxDist:
            #provjera maxtime
            if self.T[driver.start][rider.start] + self.T[rider.start][rider.end] + self.T[rider.end][driver.end] <= driver.maxTime:
                if len(driver.stops) == 0:
                    if rider.numOfPassengers <= driver.capacity and driver.checkTime(rider, 0, 1): #dist za prazno vec provjereno u prvom ifu
                        time1 = driver.depTime[0] + self.T[driver.start][rider.start]
                        w1 = max(0, rider.depTime[0] - driver.depTime[0] - self.T[driver.start][rider.start])
                        time2 = time1 + self.T[rider.start][rider.end]
                        driver.stops.insert(0, [rider, rider.start, 0, time1, w1])
                        driver.stops.insert(1, [rider, rider.end, 1, time2, 0])
                        driver.adjustTimes()
                        #print("inserted new 2")
                        return True
                    return False
                for i in range(-1, len(driver.stops)): #di buš ga pokupil
                    if driver.exists(rider.id): 
                        print("ovo se nesmi desiti try2")
                        return True
                    if driver.compareTime(rider, i, 0): #može vremenski na index i
                        k = i+1 #ubaci na k
                        for j in range(k, len(driver.stops)): #di buš ga ostavil
                            if driver.compareTime(rider, j, 1):
                                if driver.checkCapacity(rider.numOfPassengers, i) and driver.checkDistance(rider, k, j+1) and driver.checkTime(rider, k, j+1):
                                    time1 = driver.stops[k-1][3] + self.T[driver.stops[k-1][1]][rider.start]
                                    w1 = max(0, rider.depTime[0] - driver.stops[k-1][3] - self.T[driver.stops[k-1][1]][rider.start])
                                    time2 = driver.stops[j][3] + self.T[driver.stops[j][1]][rider.end]
                                    driver.stops.insert(k, [rider, rider.start, 0, time1, w1])
                                    driver.stops.insert(j+1, [rider, rider.end, 1, time2, 0])
                                    driver.adjustTimes()
                                    #print("inserted new 2")
                                    return True
        return False    
    
    def calcTaken(self):
        for driver in self.routes:
            driver.calculateTakenSeats()
    
    def findIndex(self, stops, id):
        for stop in stops:
            if stop[0].id == id and stop[2] == 1:
                return stops.index(stop)
        return -1
    
    def findIndex2(self, stops, id):
        for stop in stops:
            if stop[0].id == id and stop[2] == 0:
                return stops.index(stop)
        return -1
    

    

    def copy(self):
        new = Solution()
        new.unmatched = self.unmatched.copy()
        new.riders = self.riders
        new.routes = [driver.copy() for driver in self.routes]
        new.fitness = self.fitness
        new.numOfRoutes = self.numOfRoutes
        new.distance = self.distance
        new.time = self.time
        new.riderTime = self.riderTime
        new.D = self.D
        new.T = self.T
        return new


