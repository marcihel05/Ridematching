from settings import *

class Driver:
    def __init__(self, distMatrix = [], timeMatrix = [], data = []):
        self.id = 0
        self.start = 0
        self.end = 0
        self.depTime = 0
        self.arrivalTime = 0
        self.capacity = 0
        self.taken = 0
        self.stops = [] #stanice po putu - lista uređenih petorki (rider, point, c \in {0,1}, vrijeme dolaska na point, vrijeme čekanja) (0 - tu ga pokupim, 1 - tu ga ostavim)
        self.D = distMatrix
        self.T = timeMatrix
        self.maxDist = 0
        self.maxTime = 0
        self.endTime = 0 #ukomponiraj
        self.startTime = 0 #ukomponiraj
        if len(data):self.initialize(data)
    
    def initialize(self, data):
        self.id = data[0]
        self.start = data[1]
        self.end = data[2]
        self.depTime = data[3]
        self.arrivalTime = data[4]
        self.capacity = data[5]
        self.maxDist = self.D[self.start][self.end] * BD + AD
        self.maxTime = AT + BT * self.T[self.start][self.end]

    
    def copy(self):
        new = Driver()
        new.id = self.id
        new.start = self.start
        new.end = self.end
        new.depTime = self.depTime
        new.arrivalTime = self.arrivalTime
        new.capacity = self.capacity
        new.taken = self.taken
        new.stops = self.stops.copy()
        new.D = self.D
        new.T = self.T
        new.maxDist = self.maxDist
        new.maxTime = self.maxTime
        new.startTime = self.startTime
        new.endTime = self.endTime
        return new
        
    
    def calcDistance(self): #duljina puta
        if len(self.stops) == 0: return self.D[self.start][self.end]
        dist = self.D[self.start][self.stops[0][1]]
        for i in range(len(self.stops)-1):
            dist += self.D[self.stops[i][1]][self.stops[i+1][1]] # D - matrica takva da D[i][j] == udaljenost između stanica i i j
        dist += self.D[self.stops[len(self.stops)-1][1]][self.end]
        return dist
    

    def checkDistance(self, rider, indIn, indOut):
        route = self.stops.copy()
        route.insert(indIn,[rider, rider.start, 0, 0 , "w"] )
        route.insert(indOut,[rider, rider.end, 1, 0, "w"] )
        dist = self.D[self.start][route[0][1]]
        #print(self.start)
        #print(route[0][1])
        #print(dist)
        for i in range(len(route)-1):
            dist += self.D[route[i][1]][route[i+1][1]]
        dist += self.D[route[len(route)-1][1]][self.end]
        return dist <= self.maxDist
    
    def checkTime(self, rider, indIn, indOut):
        route = self.stops.copy()
        if indIn == 0: time1 = self.depTime[0] + self.T[self.start][rider.start]
        else: time1 = route[indIn -1][3] + self.T[route[indIn -1][1]][rider.start]
        route.insert(indIn, [rider, rider.start, 0, time1, "w"] )
        time2 = route[indOut-1][3] + self.T[route[indOut-1][1]][rider.end]
        route.insert(indOut, [rider, rider.end, 1, time2, "w"] )
        route = self.adjustTimesCopy(route)
        if route[len(route) -1][3] + self.T[route[len(route) -1][1]][self.end] - self.depTime[0] > self.maxTime:
            #print(route[len(route) -1][3] + self.T[route[len(route) -1][1]][self.end] - self.depTime[0])
            #print(self.maxTime)
            return False
        for i in range(len(route)-1):
            if route[i][2] == 0: #tu kupimo putnik
                rider = route[i][0]
                for j in range(i+1, len(route)):
                    if rider.id == route[j][0].id: #tu ga ostavljamo
                       if route[j][3] - route[i][3] > rider.maxTime:
                           return False
            
        return True


    def compareTime(self, rider, index, inOrOut): #POPRAVITI da provjerava interval (pushforward)
        if inOrOut == 0:
            loc = rider.start
        else:
            loc = rider.end
        if index == -1: #želimo ridera ubaciti kao prvu stanicu
            time = self.depTime[0] + self.T[self.start][loc] #vrijeme polaska vozača + vrijeme potrebno za doći od mjesta polaska vozača do loc
            stop = self.stops[0]
            time3 = stop[3] #vrijeme u koje se dođe na lokaciju od stop
            return time + self.T[loc][stop[1]] <= time3 # time + vrijeme potrenbno za doći od loc do lokacije od stop mora biti manje od vremena kad dolazimo na lokaciju od stop
        if index == len(self.stops) - 1: # želimo ridera ubaciti kao zadnju stanicu
            stop = self.stops[len(self.stops) - 1] 
            time3 = stop[3] #vrijeme kad smo došli na stop
            return time3 + self.T[stop[1]][loc] + self.T[loc][self.end] <= self.depTime[1] # time3 + vrijeme potrebno od stop do loc + vrijeme potrebno zs od loc do cilja vozača mora bit manji od planiranog dolaska vozača
        if index == len(self.stops):#jedino kad vozača želimo ubaciti na kraj liste (to je onda stanica di ga ostavljamo jer smo ga pokupili na indexu len(self.stops) (tak bi trebalo biti))
             stop = self.stops[len(self.stops) - 1] 
             time3 = stop[3] + self.T[stop[1]][rider.start] #vrijeme kad smo došli na rider.start
             return time3 + self.T[rider.start][loc] + self.T[loc][self.end] <= self.depTime[1]
        stop1 = self.stops[index]
        stop2 = self.stops[index+1]
        time1 = stop1[3] #vrijeme kad smo došli na stop1
        time2 = stop2[3] #vrijeme kad smo došli na stop2
        return time1 + self.T[stop1[1]][loc] + self.T[loc][stop2[1]] <= time2
    
    def adjustTimes(self): #adjust waiting time
        self.stops[0][3] = self.depTime[0] + self.T[self.start][self.stops[0][1]]
        for i in range(len(self.stops)-1):
            self.stops[i+1][3] = self.stops[i][3] + self.T[self.stops[i+1][1]][self.stops[i][1]]
    
    def pushForwardAll(self, indOfStop, pf): #dodaj posebni slučaj ako se pomiče sve nakon driver.start
        for i in range(indOfStop, len(self.stops)):
            if not pf: return
            stop = self.stops[i]
            pf = max(0, pf - stop[4])
            stop[3] = pf + stop[3]
            if indOfStop == 0 and i == 0: stop[4] = stop[4] - max(0, stop[0].depTime[0] - stop[3] - self.T[stop[1]][self.start])
            else: stop[4] = stop[4] - max(0, stop[0].depTime[0] - stop[3] - self.T[stop[1]][self.stops[i-1][1]])
        pf = max(0, pf)
        self.endTime = pf + self.endTime
    
    def adjustTimesCopy(self, route):
        copy = route.copy()
        copy[0][3] = self.depTime[0] + self.T[self.start][copy[0][1]]
        for i in range(len(copy)-1):
            copy[i+1][3] = copy[i][3] + self.T[copy[i+1][1]][copy[i][1]]
        return copy

    def checkCapacity(self, numOfPass, index):
        cap = 0
        for i in range(index+1):
            if self.stops[i][2] == 0: cap += self.stops[i][0].numOfPassengers
            else: cap -= self.stops[i][0].numOfPassengers
        cap += numOfPass
        if cap >= self.capacity: return False

        for i in range(index+1, len(self.stops)):
            if self.stops[i][2] == 0: cap += self.stops[i][0].numOfPassengers
            else: cap -= self.stops[i][0].numOfPassengers
            if cap >= self.capacity: return False
        return True

    
    def calculateTakenSeats(self):
        tkn = 0
        for stop in self.stops:
            if stop[2] == 0: tkn += stop[0].numOfPassengers
            else: tkn -= stop[0].numOfPassengers
        self.taken = tkn
        return tkn
    
    def printDriver(self):
        listDriver = [self.id, self.start, self.end, self.depTime, self.arrivalTime, self.capacity, self.taken]
        print(listDriver)
        for stop in self.stops:
            strr = stop[0].toString() + ", " + str(stop[1]) + ", " + str(stop[2])
            print(strr)


    
        
