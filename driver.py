class Driver:
    def __init__(self, data):
        self.id = data[0]
        self.start = data[1]
        self.end = data[2]
        self.depTime = data[3]
        self.arrivalTime = data[4]
        self.capacity = data[5]
        self.taken = 0
        self.stops = [] #stanice po putu - lista uređenih trojki (rider, point, c \in {0,1}) (0 - tu ga pokupim, 1 - tu ga ostavim)
        
    
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

        return time > time1 and time < time2
    
    def checkCapacity(self, numOfPass, index):
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
                tkn -= self.stop[0].numOfPassengers
        self.taken = tkn
        return tkn



         """ def calcTime(self): #trajanje puta
        time = 0
        for i in range(len(self.stops)-1):
            time += T[self.stops[i][1]][self.stops[i+1][1]] # T - matrica takva da T[i][j] == vrijeme vožnje između stanica i i j
        return time"""
    

    
        
