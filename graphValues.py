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