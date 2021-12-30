import matplotlib.pyplot as plt     #potrebno instalirati
import pylab


def graphValues(values):
    #pylab.xlim(0, len(values))
    #pylab.ylim(min(values) - max(values) + min(values), max(values) + max(values) - min(values))
    
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
    pylab.ylabel('Distance (km)')
    pylab.title('VALUES')
    
    x = [i for i in range(len(distance))]
    #figure, ax = plt.subplots()
    #ax.plot(x, values)
    plt.plot(x, distance)
    plt.show()
    return

def graphTime(time):
    pylab.xlim(0, len(time))
    pylab.ylim(min(time) - max(time) + min(time), max(time) + max(time) - min(time))
    
    pylab.xlabel('Generation')
    pylab.ylabel('Time (min)')
    pylab.title('VALUES')
    
    x = [i for i in range(len(time))]
    #figure, ax = plt.subplots()
    #ax.plot(x, values)
    plt.plot(x, time)
    plt.show()
    return


def graphRiderTime(riderTime):
    pylab.xlim(0, len(riderTime))
    pylab.ylim(min(riderTime) - max(riderTime) + min(riderTime), max(riderTime) + max(riderTime) - min(riderTime))
    
    pylab.xlabel('Generation')
    pylab.ylabel('Time (min)')
    pylab.title('VALUES')
    
    x = [i for i in range(len(riderTime))]
    #figure, ax = plt.subplots()
    #ax.plot(x, values)
    plt.plot(x, riderTime)
    plt.show()
    return

def graphAll(values, matched, distance, time, riderTime):
    #fig, axs = plt.subplots(2,2)
    mosaic = """
            AB
            DE
    """
    fig, axs = plt.subplot_mosaic(mosaic)
    x = [i for i in range(len(values))]
    #axs['C'].plot(x, values)
    #axs['C'].set(title='Values of obj func', xlabel = 'Generation', ylabel = 'Value')
    axs['A'].plot(x, matched)
    axs['A'].set(title='Number of matched riders', xlabel = 'Generation', ylabel = 'Num of matched')
    axs['B'].plot(x, distance)
    axs['B'].set(title='Distance', xlabel = 'Generation', ylabel = 'Distance(km)')
    axs['D'].plot(x, time)
    axs['D'].set(title='Driver time', xlabel = 'Generation', ylabel = 'Time(min)')
    axs['E'].plot(x, riderTime)
    axs['E'].set(title='Rider time', xlabel = 'Generation', ylabel = 'Time(min)')
    plt.show()
