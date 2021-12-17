class Rider:
    def __init__(self, data=[]):
        self.id = 0
        self.start = 0 
        self.end = 0
        self.depTime = 0
        self.arrivalTime = 0
        self.numOfPassengers = 0
        if len(data):
            self.initialize(data)
    def initialize(self, data):
        self.id = data[0]
        self.start = data[1]
        self.end = data[2]
        self.depTime = data[3]
        self.arrivalTime = data[4]
        self.numOfPassengers = data[5]
    
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
        return str(self.id) + " " + str(self.start) + " " + str(self.end) + " " + self.depTime + " " + self.arrivalTime + " " + str(self.numOfPassengers)
    