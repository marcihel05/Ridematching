class Rider:
    def __init__(self, data):
        self.id = data[0]
        self.start = data[1]
        self.end = data[2]
        self.depTime = data[3]
        self.arrivalTime = data[4]
        self.numOfPassengers = data[5]
    