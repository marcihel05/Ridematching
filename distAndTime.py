from settings import *

def calcDistance(a, b):
    from math import sin, cos, sqrt, atan2, radians
    R = 6371 # approx radius of Earth in km
    lon1 = radians(a[0])
    lat1 = radians(a[1])
    lon2 = radians(b[0])
    lat2 = radians(b[1])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat/2)**2 + cos(lat1)*cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R*c

def distances(locations):
    from math import ceil
    #print(locations)
    distance_between_locations = list()
    for i in range(len(locations)):
        pom_list = []
        for j in range(len(locations)):
            pom_list.append(calcDistance(locations[i], locations[j]))
        distance_between_locations.append(pom_list)
    return distance_between_locations

def times(locations, distances):
    from math import ceil
    time_between_locations = []
    for i in range(len(locations)):
        pom_list = list()
        for j in range(len(locations)):
            a = ceil(distances[i][j]/V)
            #aa = int((a * 100) + 0.5) / 100.0 
            pom_list.append(a)
        time_between_locations.append(pom_list)
    return time_between_locations