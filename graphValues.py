import matplotlib.pyplot as plt     #potrebno instalirati
import pylab


def graphValues(values):
    pylab.xlim(0, len(values))
    pylab.ylim(min(values) - max(values) + min(values), max(values) + max(values) - min(values))
    
    pylab.xlabel('Generation')
    pylab.ylabel('Value of multiobj function')
    pylab.title('VALUES')
    
    x = [i for i in range(len(values))]
    #figure, ax = plt.subplots()
    #ax.plot(x, values)
    plt.plot(x, values)
    plt.show()
    return

def graphUnmatched(unmatched):
    pylab.xlim(0, len(unmatched))
    pylab.ylim(min(unmatched) - max(unmatched) + min(unmatched), max(unmatched) + max(unmatched) - min(unmatched))
    
    pylab.xlabel('Generation')
    pylab.ylabel('Num of matched')
    pylab.title('VALUES')
    
    x = [i for i in range(len(unmatched))]
    #figure, ax = plt.subplots()
    #ax.plot(x, values)
    plt.plot(x, unmatched)
    plt.show()
    return

def graphDistance(distance):
    pylab.xlim(0, len(distance))
    pylab.ylim(min(distance) - max(distance) + min(distance), max(distance) + max(distance) - min(distance))
    
    pylab.xlabel('Generation')
    pylab.ylabel('Distance')
    pylab.title('VALUES')
    
    x = [i for i in range(len(distance))]
    #figure, ax = plt.subplots()
    #ax.plot(x, values)
    plt.plot(x, distance)
    plt.show()
    return
