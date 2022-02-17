
import matplotlib.pyplot as plt     #potrebno instalirati
import pylab

#x - lista listi x koord., y - lista listi y koord., z - lista koord. i labela
#i - broj generacije
def plot_solution(x,y,z,i):

    plot1 = plt.figure(i)
    pylab.xlabel('X')
    pylab.ylabel('Y')
    pylab.title('GEN ' + str(i))
    
    for i in range(len(x)):
        plt.scatter(x[i], y[i])
        plt.plot(x[i], y[i])

    return plt

def main(p):
    for x in p:
        plt = plot_solution(x[0], x[1], x[2], x[3])
    plt.show()
    return

def mainMap(p):
    for x in p:
        plt = plotSolutionOnMap(x[0], x[1], x[2], x[3])
    plt.show()
    return

def plotSolutionOnMap(coords):
    map = plt.imread('map.png')
    BBox = (-88.75, -87.0, 41.0, 42.6)
    fig, ax = plt.subplots(figsize = (8,7))
    ax.set_title('map')
    ax.set_xlim(BBox[0],BBox[1])
    ax.set_ylim(BBox[2],BBox[3])
    ax.imshow(map, zorder=0, extent = BBox, aspect= 'auto')
    for c in coords:
        x = c[0]
        y = c[1]
        for i in range(len(x)):
            ax.scatter(x[i], y[i], zorder=1)
            ax.plot(x[i], y[i], zorder=1)
    plt.show()
