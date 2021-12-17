class Driver:
    def __init__(self, data = []):
        self.id = 0
        self.start = 0
        self.end = 0
        self.depTime = 0
        self.arrivalTime = 0
        self.capacity = 0
        self.taken = 0
        self.stops = [] #stanice po putu - lista uređenih trojki (rider, point, c \in {0,1}) (0 - tu ga pokupim, 1 - tu ga ostavim)
        if len(data):
            self.initialize(data)
    
    def initialize(self, data):
        self.id = data[0]
        self.start = data[1]
        self.end = data[2]
        self.depTime = data[3]
        self.arrivalTime = data[4]
        self.capacity = data[5]

    
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
        return new
        
    
    def calcDistance(self): #duljina puta
        dist = D[self.start][self.stops[0][1]]
        for i in range(len(self.stops)-1):
            dist += D[self.stops[i][1]][self.stops[i+1][1]] # D - matrica takva da D[i][j] == udaljenost između stanica i i j
        dist += D[self.stops[len(self.stops)-1]][self.end]
        return dist
    
  

    def compareTime(self, rider,index, inOrOut):
        if inOrOut == 0:
            time = rider.depTime
        else:
            time = rider.arrivalTime
        if index == -1:
            stop = self.stops[0]
            if stop[2] == 0:
                time3 = stop[0].depTime
            else:
                time3 = stop[0].arrivalTime
            return time <= time3
        stop1 = self.stops[index]
        stop2 = self.stops[index+1]
        if stop1[2] == 0:
            time1 = stop1[0].depTime
        else:
            time1 = stop1[0].arrivalTime      
        if stop2[2] == 0:
             time2 = stop2[0].depTime
        else:
            time2 = stop2[0].arrivalTime

        return time >= time1 and time <= time2
    
    def checkCapacity(self, numOfPass, index):
        if index == -1:
            return True
        cap = 0
        for i in range(index+1):
            if self.stops[i][2] == 0:
                cap += self.stops[i][0].numOfPassengers
            else:
                cap -= self.stops[i][0].numOfPassengers
        return cap + numOfPass <= self.capacity
        
    
    def calculateTakenSeats(self):
        tkn = 0
        for stop in self.stops:
            if stop[2] == 0:
                tkn += stop[0].numOfPassengers
            else:
                tkn -= stop[0].numOfPassengers
        self.taken = tkn
        return tkn
    
    def printDriver(self):
        listDriver = [self.id, self.start, self.end, self.depTime, self.arrivalTime, self.capacity, self.taken]
        print(listDriver)
        for stop in self.stops:
            strr = stop[0].toString() + ", " + str(stop[1]) + ", " + str(stop[2])
            print(strr)



        # def calcTime(self): #trajanje puta
        #time = 0
        #for i in range(len(self.stops)-1):
         #   time += T[self.stops[i][1]][self.stops[i+1][1]] # T - matrica takva da T[i][j] == vrijeme vožnje između stanica i i j
        #return time"""
    

    
        
