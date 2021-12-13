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
    
   """ def calcTime(self): #trajanje puta
        time = 0
        for i in range(len(self.stops)-1):
            time += T[self.stops[i][1]][self.stops[i+1][1]] # T - matrica takva da T[i][j] == vrijeme vožnje između stanica i i j
        return time"""
    

    
        
