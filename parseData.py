

def parseData(data): # data - txt file
    riderData = []
    driverData = []
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
        driver.append((float(driverSplit[3]), float(driverSplit[4])))
        driver.append((float(driverSplit[8]), float(driverSplit[9])))
        #earliest dep time
        driver.append((int(driverSplit[5]), int(driverSplit[6])))
        #latest ar time
        driver.append((float(driverSplit[10]), float(driverSplit[1])))
        driver.append(5)       #iz rada
        driverData.append(driver)

    for i in range(numOfRiders):
        riderSplit = data.readline().split()
        rider = []
        rider.append(int(riderSplit[0]))
        rider.append((float(riderSplit[3]), float(riderSplit[4])))
        rider.append((float(riderSplit[8]), float(riderSplit[9])))
        rider.append(int(riderSplit[5]))
        rider.append(float(riderSplit[11]))
        riderData.append(rider)

    return (riderData, driverData)
