class Rider:
    def __init__(self, data=[]):
        self.id = 0
        self.start = () 
        self.end = ()
        self.depTime = ()
        self.arrivalTime = ()
        self.numOfPassengers = 1
        if len(data):
            self.initialize(data)
    def initialize(self, data):
        self.id = data[0]
        self.start = data[1]
        self.end = data[2]
        self.depTime = data[3]
        self.arrivalTime = data[4]
    
    def copy(self):
        new = Rider()
        new.id = self.id
        new.start = self.start
        new.end = self.end
        new.depTime = self.depTime
        new.arrivalTime = self.arrivalTime
        new.numOfPassengers = self.numOfPassengers
        return new
    
    def printRider(self):
        listRider = [self.id, self.start, self.end, self.depTime, self.arrivalTime, self.numOfPassengers]
        print(listRider)
    
    def toString(self):
        ret = str(self.id) + " " + "(" + str(self.start[0]) + ", " + str(self.start[1]) + ") (" 
        ret += str(self.end[0]) + ", " + str(self.end[1]) + ") (" 
        ret += str(self.depTime[0]) + ", " + str(self.depTime[1]) + ") ("
        ret += str(self.arrivalTime[0]) + ", " +str(self.arrivalTime[1]) + ") " + str(self.numOfPassengers)
        return ret
    