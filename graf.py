
import matplotlib.pyplot as plt     #potrebno instalirati
import pylab

#x - lista listi x koord., y - lista listi y koord., z - lista koord. i labela
#i - broj generacije
def main(x,y,z,i):
    
    pylab.xlim(-89, -87)
    pylab.ylim(41, 43)
    
    pylab.xlabel('X')
    pylab.ylabel('Y')
    pylab.title('GRAPH ' + str(i))
    print(x[0])
    
    for i in range(len(x)):
        plt.scatter(x[i],y[i])
        plt.plot(x[i],y[i])
    
    for t in z:
        plt.annotate(t[1], t[0])

    plt.show()
    return
