
import matplotlib.pyplot as plt     #potrebno instalirati
import pylab
#import numpy as np

def main(x,y,z):
    
    pylab.ylim(-100, 100)
    pylab.xlim(-100, 100)
    
    pylab.xlabel('X')
    pylab.ylabel('Y')
    pylab.title('GRAPH')
    print(x[0])
    
    for i in range(len(x)):
        plt.scatter(x[i],y[i])
        plt.plot(x[i],y[i])
        for j in range(len(x[i])):
            plt.annotate(z[i][j], (x[i][j], y[i][j]))

    plt.show()
    return

##x = [80,81,90,95]
##y = [51,45,56,64]
##z = [1,2,3,4]
##x1 = [40,60,80,10]
##y1 = [20,30,40,50]
##z1 = ['a','b','c','d']
##x2 = [40,50,40,50]
##y2 = [10,20,30,50]
##z2 = [10,20,'e','f']
##l = [x,x1,x2]
##k = [y,y1,y2]
##m = [z,z1,z2]
##main(l,k,m)
