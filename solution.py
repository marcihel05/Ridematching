import random
from driver import *
from settings import *
from math import ceil, floor
import time
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

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
       ridersCopy = self.riders.copy()
       driversCopy = [i for i in range(len(self.routes))]
       while len(driversCopy):
           rnd = random.randrange(len(driversCopy))
           ind = driversCopy[rnd]
           driversCopy.remove(ind)
           driver = self.routes[ind]
           random.shuffle(ridersCopy)
           for rider in ridersCopy:
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
                           driver.adjustTimes()
                           inserted = True
                   else:
                        for i in range(-1, len(driver.stops)): #di buš ga pokupil
                            if driver.compareTime(rider, i, 0): #može vremenski na index i
                                k = i+1 #ubaci na k
                                for j in range(k, len(driver.stops)): #di buš ga ostavil
                                    if driver.compareTime(rider, j, 1):
                                        if driver.checkCapacity(rider.numOfPassengers, i) and driver.checkDistance(rider, k, j+1) and driver.checkTime(rider, k, j+1):
                                            time1 = max(rider.depTime[0], driver.stops[k-1][3] + driver.stops[k-1][4] + self.T[driver.stops[k-1][1]][rider.start])
                                            if time1 > rider.depTime[1]: continue
                                            w1 = max(0, rider.depTime[0] - time1)
                                            time2 = driver.stops[j][3] + driver.stops[j][4] + self.T[driver.stops[j][1]][rider.end]
                                            if time2 > rider.arrivalTime[1]: continue
                                            driver.stops.insert(k, [rider, rider.start, 0, time1, w1])
                                            driver.stops.insert(j+1, [rider, rider.end, 1, time2, 0])
                                            inserted = True
                                            ridersCopy.remove(rider)
                                            driver.adjustTimes()
                                            break # prekida for j
                                if inserted: break #prekida for i
       self.unmatched = ridersCopy
       self.numOfRoutes = len(self.routes)
            
        
    def mutate(self, rate):
        self.pushBackward(rate)
        self.pushForward2(rate)
        self.removeInsert2(rate)
        self.transfer2(rate)
        self.swap2(rate)
    
    def pushBackward(self, rate): #first mutation operator #dodaj vozača
        randList = random.sample(range(0, self.numOfRoutes), int(floor(rate*self.numOfRoutes)))
        for i in randList:
            route = self.routes[i]
            if len(route.stops) < 0: #mutiraj
                i = random.randrange(-1, len(route.stops))
                if i == -1:
                    if route.startTime - route.depTime[0] > 0: pb = ceil(random.uniform(0, route.startTime - route.depTime[0]))
                    else: continue
                    route.startTime = route.startTime - pb
                route.pushBackwardAll(i+1, pb)
            elif not len(route.stops):
                 if route.startTime - route.depTime[0] > 0: pb = ceil(random.uniform(0, route.startTime - route.depTime[0]))
                 else: continue
                 if route.endTime - pb < route.arrivalTime[0]: continue
                 route.startTime -= pb
                 route.endTime -= pb

    def pushForward2(self,rate): #second mutation operator 
        randList = random.sample(range(0, self.numOfRoutes), int(floor(rate*self.numOfRoutes)))
        for j in randList:
            route = self.routes[j]
            if len(route.stops) < 0:  #mutiraj
                nope = False
                i = random.randrange(-1, len(route.stops))
                if i == -1:
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
                route.pushForwardAll(i+1, pf)
            elif not len(route.stops):
                if route.depTime[1] - route.startTime > 0: 
                    pf = ceil(random.uniform(0, route.depTime[1] - route.startTime))
                    if pf + route.endTime > route.arrivalTime[1]: continue
                    else:
                        route.startTime += pf
                        route.endTime += pf

    def removeInsert2(self, rate): #third mutation operator
        randList = random.sample(range(0, self.numOfRoutes), int(floor(rate*self.numOfRoutes)))
        for j in randList:
            route = self.routes[j]
            if len(route.stops) > 0:  #mutiraj
                i = random.randrange(len(route.stops))
                stop = route.stops[i]
                self.unmatched.append(stop[0])
                route.stops.remove(stop)
                if stop[2] == 1: ind = self.findIndex2(route.stops, stop[0].id)
                else: ind = self.findIndex(route.stops, stop[0].id)
                if ind > -1: route.stops.pop(ind)
                else: print("something's wrong in remove insert " +str(self.routes.index(route)))
                route.adjustTimes()
                random.shuffle(self.unmatched)
                for rider in self.unmatched:
                    if route.depTime[0] <= rider.depTime[1] and route.arrivalTime[1] >= rider.arrivalTime[0] and self.tryToInsert2(rider, route): self.unmatched.remove(rider)
            elif not len(route.stops):
                random.shuffle(self.unmatched)
                for rider in self.unmatched:
                    if route.depTime[0] <= rider.depTime[1] and route.arrivalTime[1] >= rider.arrivalTime[0] and self.tryToInsert2(rider, route): self.unmatched.remove(rider)
    
    def transfer2(self, rate): #fourth mutation operator
        randList = random.sample(range(0, self.numOfRoutes), int(floor(rate*self.numOfRoutes)))
        for j in randList:
            route = self.routes[j]
            if len(route.stops) > 0: #mutiraj
                i = random.randrange(len(route.stops))
                stop = route.stops[i]
                if self.tryToInsert(stop[0], route.id):
                    route.stops.remove(stop)
                    if stop[2] == 1: ind = self.findIndex2(route.stops, stop[0].id)
                    else: ind = self.findIndex(route.stops, stop[0].id)
                    if ind > -1: route.stops.pop(ind)
                    else: print("something's wrong in transfer " + str(self.routes.index(route)))
                    route.adjustTimes()

    def swap2(self, rate): #fifth mutation operator
        randList = random.sample(range(0, self.numOfRoutes), int(floor(rate*self.numOfRoutes)))
        for j in randList:
            route = self.routes[j]
            if len(route.stops) > 0: #mutiraj
                i = random.randrange(len(route.stops))
                if i == len(route.stops) -1 : i -= 1
                if route.stops[i][0].id != route.stops[i+1][0].id:
                    s1 = route.stops[i].copy()
                    s2 = route.stops[i+1].copy()
                    route.stops[i] = s2
                    route.stops[i+1] = s1
                    route.adjustTimes()


    def crossover(self, otherSolution, rate):
        start = time.time()
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
        newSolution1.unmatched = list(set(self.riders)-match1)
        newSolution2.unmatched = list(set(self.riders)-match2)
        newSolution1.insertUnmatched2()         #iteracija po unmacthed umjesto po routes
        newSolution2.insertUnmatched2()
        return newSolution1, newSolution2
    
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
        unservedReq = delta*len(self.unmatched)/(len(self.riders))
        for driver in self.routes:
            d = driver.calcDistance()
            dist += d
            maxDist += driver.maxDist
            t = (driver.endTime - driver.startTime)
            time += t
            maxTime += driver.maxTime
            if len(driver.stops) == 0: continue
            for stop in driver.stops:
                if stop[2] == 0:
                    ind = self.findIndex(driver.stops, stop[0].id)
                    riderTime += (driver.stops[ind][3] - stop[3] - stop[4])
                    maxRiderTime += stop[0].maxTime
        self.distance = dist
        self.time = time
        self.riderTime = riderTime
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

    def checkIfFeasibleAfterCrossAndFix(self, routeIndex): #pogledaj dal više vozača ne vozi istog putnika i makni ako ima toga
        for i in range(routeIndex):
            for stop1 in self.routes[i].stops:
                if stop1[2] == 0:
                    rider = stop1[0]
                    for j in range(routeIndex,len(self.routes)):
                        for stop2 in self.routes[j].stops:
                            if stop2[0].id == rider.id and stop2[2] == 0:
                                ind0 =self.findIndex2(self.routes[j].stops, rider.id)
                                self.routes[j].stops.pop(ind0)
                                ind = self.findIndex(self.routes[j].stops, rider.id)
                                if ind > -1: self.routes[j].stops.pop(ind)
                                self.routes[j].adjustTimes()
    
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
            # random broj drivera (od onih koji odgovaraju) u koje cemo pokusati ubaciti
            r = random.randint(len(drivers_sublist)//4, len(drivers_sublist)//2)
            # random sample indeksa duljine r
            sample = random.sample(range(0,len(drivers_sublist)), r)
            for k in sample:
                if self.tryToInsert2(rider, drivers_sublist[k]):
                    self.unmatched.remove(rider)
                    break
            
            if rider not in self.unmatched: continue
            # ako ridera nismo ubacili, pokusavamo u ostatku liste
            new_try = set(range(len(drivers_sublist))) - set(sample)
            for k in new_try:
                if self.tryToInsert2(rider, drivers_sublist[k]):
                    self.unmatched.remove(rider)
                    break

    def tryToInsert(self, rider, routeId = -1): #probaj ga negde staviti 
        driversCopy = [i for i in range(len(self.routes))]
        while len(driversCopy):
            rnd = random.randrange(len(driversCopy))
            ind = driversCopy[rnd]
            driversCopy.remove(ind)
            driver = self.routes[ind]
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
                                        if driver.checkCapacity(rider.numOfPassengers, i) and driver.checkDistance(rider, k, j+1) and driver.checkTime(rider, k, j+1):
                                            time1 = driver.stops[k-1][3] + self.T[driver.stops[k-1][1]][rider.start]
                                            w1 = max(0, rider.depTime[0] - driver.stops[k-1][3] - self.T[driver.stops[k-1][1]][rider.start])
                                            time2 = driver.stops[j][3] + self.T[driver.stops[j][1]][rider.end]
                                            driver.stops.insert(k, [rider, rider.start, 0, time1, w1])
                                            driver.stops.insert(j+1, [rider, rider.end, 1, time2, 0])
                                            driver.adjustTimes()
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
                                    return True
        return False


    def returnFitness(self, vals): #racunaj funkciju dobrote (po onoj formuli)
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
        unservedReq = delta*len(self.unmatched)/(len(self.riders))
        for driver in self.routes:
            d = driver.calcDistance()
            dist += d
            maxDist += driver.maxDist
            t = (driver.endTime - driver.startTime)
            time += t
            maxTime += driver.maxTime
            if len(driver.stops) == 0: continue
            for stop in driver.stops:
                if stop[2] == 0:
                    ind = self.findIndex(driver.stops, stop[0].id)
                    riderTime += (driver.stops[ind][3] - stop[3] - stop[4])
                    maxRiderTime += stop[0].maxTime
        self.distance = dist
        self.time = time
        self.riderTime = riderTime
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
        return val
    
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
    
    def draw(self, win, upperLeft, h,w, coords, toShow):
        r = 3 #radius
        xmultiply = w/1.1
        ymultiply = h/1.3
        for rider in self.unmatched: #nespareni putnici su bijele točke
            point = [coords[rider.start][0], coords[rider.start][1]]
            point[0] = (point[0] + upperLeft[0] + 88.5) * xmultiply
            point[1] = (upperLeft[1] + h) - ((point[1] - 41.2)) * ymultiply
            pygame.draw.circle(win, WHITE, point,r)
        i = 0
        for driver in self.routes:
            if i == 25 and not toShow: break
            color = driver.color
            start = [coords[driver.start][0], coords[driver.start][1]]
            start[0] = (start[0] + upperLeft[0] + 88.5) * xmultiply
            start[1] = (upperLeft[1] + h) - ((start[1] - 41.2)) * ymultiply
            for rider in driver.stops[0:len(driver.stops)-1]:
                end = [coords[rider[1]][0], coords[rider[1]][1]]
                end[0] = (end[0] + upperLeft[0] + 88.5) * xmultiply
                end[1] = (upperLeft[1] + h) - ((end[1] - 41.2)) * ymultiply
                pygame.draw.circle(win, color, start, r)
                pygame.draw.circle(win, color, end, r)
                pygame.draw.line(win,color, start, end, 2)
                start = [coords[driver.stops.index(rider)+1][0], coords[driver.stops.index(rider)+1][1]]
                start[0] = (start[0] + upperLeft[0] + 88.5) * xmultiply
                start[1] = (upperLeft[1] + h) - ((start[1] - 41.2)) * ymultiply
            end = [coords[driver.end][0], coords[driver.end][1]]
            end[0] = (end[0] + upperLeft[0] + 88.5) * xmultiply
            end[1] = (upperLeft[1] + h) - ((end[1] - 41.2)) * ymultiply
            pygame.draw.circle(win, color, start, r)
            pygame.draw.circle(win, color, end, r)
            pygame.draw.line(win,color, start, end, 2)
            i+=1


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


