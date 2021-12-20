
import matplotlib.pyplot as plt     #potrebno instalirati
import pylab

#x - lista listi x koord., y - lista listi y koord., z - lista koord. i labela
#i - broj generacije
def plot_solution(x,y,z,i):

    plot1 = plt.figure(i)
    
    pylab.xlim(-89, -87)
    pylab.ylim(41, 43)
    
    pylab.xlabel('X')
    pylab.ylabel('Y')
    pylab.title('GEN ' + str(i))
    
    for i in range(len(x)):
        plt.scatter(x[i], y[i])
        plt.plot(x[i], y[i])
    for t in z:
        plt.annotate(t[1], t[0])

    return plt

def main(p):
    for x in p:
        plt = plot_solution(x[0], x[1], x[2], x[3])
    plt.show()
    return
