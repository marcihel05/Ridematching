class Driver:
    def __init__(self, data):
        self.id = data[0]
        self.start = data[1]
        self.end = data[2]
        self.depTime = data[3]
        self.arivalTime = data[4]
        self.capacity = data[5]
        self.stops = [] #stanice po putu
        
    
    def calcDistance(self): #duljina puta
        ...
    
    def calcTime(self): #trajanje puta
        ...
    

    
        
