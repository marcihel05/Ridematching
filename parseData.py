def parseData(data): # data - txt file
    riderData = []
    driverData = []
    lokacije = []
    next(data)          #skip prvu liniju - uk. br. zahtjeva
    l = data.readline().split()
    numOfDrivers = int(l[4])
    l = data.readline().split()
    numOfRiders = int(l[4])
    next(data)          #prazna linija
    next(data)          #stupci

    for i in range(numOfDrivers):
        driverSplit = data.readline().split()
        driver = []
        driver.append(int(driverSplit[0]))
        #koordinate start i end
        #matrica
        t = (float(driverSplit[3]), float(driverSplit[4]))
        if lokacije.count(t):
            driver.append(lokacije.index(t))
        else:
            lokacije.append(t)
            driver.append(len(lokacije)-1)
        t = (float(driverSplit[8]), float(driverSplit[9]))
        if lokacije.count(t):
            driver.append(lokacije.index(t))
        else:
            lokacije.append(t)
            driver.append(len(lokacije)-1)
        #dep time window
        driver.append((int(driverSplit[5]), int(driverSplit[6])))
        #ar time window
        driver.append((float(driverSplit[10]), float(driverSplit[11])))
        driver.append(4)       #iz rada
        driverData.append(driver)

    for i in range(numOfRiders):
        riderSplit = data.readline().split()
        rider = []
        rider.append(int(riderSplit[0]))
        t = (float(riderSplit[3]), float(riderSplit[4]))
        if lokacije.count(t):
            rider.append(lokacije.index(t))
        else:
            lokacije.append(t)
            rider.append(len(lokacije)-1)
        t = (float(riderSplit[8]), float(riderSplit[9]))
        if lokacije.count(t):
            rider.append(lokacije.index(t))
        else:
            lokacije.append(t)
            rider.append(len(lokacije)-1)
        rider.append((int(riderSplit[5]), int(riderSplit[6])))
        rider.append((float(riderSplit[10]), float(riderSplit[11])))
        riderData.append(rider)

    return riderData, driverData, lokacije


def parseData2(data, rnd): # data - txt file
    import random
    import numpy as np
    from distAndTime import calcDistance
    riderData = []
    driverData = []
    allData = []
    lokacije = []
    allDist = []
    next(data)          #skip prvu liniju - uk. br. zahtjeva
    l = data.readline().split()
    numOfDrivers = int(l[4])
    l = data.readline().split()
    numOfRiders = int(l[4])
    next(data)          #prazna linija
    next(data)          #stupci

    for i in range(numOfDrivers + numOfRiders):
        driverSplit = data.readline().split()
        driver = []
        driver.append(int(driverSplit[0]))
        #koordinate start i end
        #matrica
        t1 = (float(driverSplit[3]), float(driverSplit[4]))
        if lokacije.count(t1):
            driver.append(lokacije.index(t1))
        else:
            lokacije.append(t1)
            driver.append(len(lokacije)-1)
        t2 = (float(driverSplit[8]), float(driverSplit[9]))
        if lokacije.count(t2):
            driver.append(lokacije.index(t2))
        else:
            lokacije.append(t2)
            driver.append(len(lokacije)-1)
        if not rnd: allDist.append(calcDistance(t1,t2))
        
        #dep time window
        driver.append((int(driverSplit[5]), int(driverSplit[6])))
        #ar time window
        driver.append((float(driverSplit[10]), float(driverSplit[11])))
        driver.append(5)       #iz rada
        allData.append(driver)
    if rnd:
        for i in range(numOfDrivers):
            ind = random.randrange(len(allData))
            driverData.append(allData[i])
            allData.remove(allData[i])
        riderData = allData
    else:
        npDist = np.array(allDist)
        npDistInd = npDist.argsort()[::-1]
        for i in range(numOfDrivers): driverData.append(allData[npDistInd[i]])
        for i in range(numOfDrivers, numOfRiders+numOfDrivers): riderData.append(allData[npDistInd[i]])
    return riderData, driverData, lokacije
