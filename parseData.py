def parseData(data): # data - txt file
    riderData = []
    driverData = []
    numOfRiders = int(data.readline())
    for i in range(numOfRiders):
        riderSplit = data.readline().split()
        rider = []
        for str in riderSplit:
            rider.append(int(str))
        riderData.append(rider)
    numOfDrivers = int(data.readline())
    for i in range(numOfDrivers):
        driverSplit = data.readline().split()
        driver = []
        for str in driverSplit:
            driver.append(int(str))
        driverData.append(driver)
    return riderData, driverData