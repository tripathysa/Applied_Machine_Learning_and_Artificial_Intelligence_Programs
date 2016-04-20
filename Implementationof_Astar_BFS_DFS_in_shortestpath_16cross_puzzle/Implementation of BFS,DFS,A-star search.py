#For BFS and DFS ,we took input from road-segments.txt
#1.Store all the nodes of road-segments.txt in list
#2.Store start city in queue/stack for bfs/dfs respectively.
#3.Search all the nodes in list where the first element is start city and add to queue its connecting city.
#4.Repeat process and check for the goal node.
#In bfs/dfs case ,Routing Option was not considered, since it returns goal path as soon as it gets the goal.
#For A*, g(n) was taken as the distance given between two cities in road-segments.txt 
#h(n) is taken as haversian distance formula.(http://www.movable-type.co.uk/scripts/latlong.html) which calculates distance between two GPS coordinates,
#For A*, 
#We are keeping an open list with start city to begin, then we expand only those node which has the least f value.
import sys
import math
from decimal import Decimal
City_Start=sys.argv[1]
City_End=sys.argv[2]
Routing_Algo=sys.argv[3]
file_road_segments = 'road-segments.txt'
file_city_gps='city-gps.txt'
with open(file_road_segments) as f:
    List_Road_Segments = f.readlines()
for i, _ in enumerate(List_Road_Segments):
    List_Road_Segments[i] = List_Road_Segments[i].split()
with open(file_city_gps) as f:
    List_city_gps = f.readlines()
for i, _ in enumerate(List_city_gps):
    List_city_gps[i] = List_city_gps[i].split()
def bfs(city_start1, city_destination1):
    queue = []
    queue.append([city_start1])
    while queue:
        path = queue.pop(0)
        node=path[-1]
        if node == city_destination1:
            return path
        for i, _ in enumerate(List_Road_Segments):
            if List_Road_Segments[i][0] == node:
                new_path = list(path)
                distance = float(List_Road_Segments[i][2])
                new_path.append(distance)
                new_path.append(float(distance/float(List_Road_Segments[i][3])))
                new_path.append(List_Road_Segments[i][1])
                if List_Road_Segments[i][1] == city_destination1:
                    sumdistance=0
                    sumtime = 0
                    outputpath=[]
                    for i in xrange(1, len(new_path)-2, 3):
                        sumdistance+=new_path[i]
                    for j in xrange(2, len(new_path)-1, 3):
                        sumtime+=new_path[j]
                    for k in xrange(0, len(new_path), 3):
                        outputpath.append(new_path[k])
                    return round(sumdistance,2), round(sumtime,2), outputpath
                else:
                    queue.append(new_path)
def dfs(city_start1, city_destination1):
    stack = []
    stack.append([city_start1])
    while stack:
        path = stack.pop()
        node = path[-1]
        if node == city_destination1:
            return path
        for i, _ in enumerate(List_Road_Segments):
            if List_Road_Segments[i][0] == node:
                new_path = list(path)
                distance = float(List_Road_Segments[i][2])
                new_path.append(distance)
                new_path.append(float(distance/float(List_Road_Segments[i][3])))
                new_path.append(List_Road_Segments[i][1])
                if List_Road_Segments[i][1] == city_destination1:
                    sumdistance=0
                    sumtime = 0
                    outputpath=[]
                    for i in xrange(1, len(new_path)-2, 3):
                        sumdistance+=new_path[i]
                    for j in xrange(2, len(new_path)-1, 3):
                        sumtime+=new_path[j]
                    for k in xrange(0, len(new_path), 3):
                        outputpath.append(new_path[k])
                    return round(sumdistance,2), round(sumtime,2), outputpath
                else:
                    stack.append(new_path)

def Astar(city_start1, city_destination1):
    ListOpen = []
    itemTopop=[]
    itemFvalueList=[]
    ListOpen.append([city_start1,0])
    while ListOpen:

        if len(ListOpen)>1:
            for m, _ in enumerate(ListOpen):
                itemFvalueList.append(ListOpen[m][1])
            path = ListOpen.pop(itemFvalueList.index(min(itemFvalueList)))
            del itemFvalueList[:]
            node=path[-1]
        else:
            path=ListOpen.pop(0)
            node=path[0]
        if node == city_destination1:
            return path
        for i, _ in enumerate(List_Road_Segments):
            if List_Road_Segments[i][0] == node:
                new_path = list(path)
                LatitudeSource=0
                LongitudeSource=0
                LatitudeGoal=0
                LongitudeGoal=0
                for m, _ in enumerate(List_city_gps):
                    if List_city_gps[m][0]==node:
                        LatitudeSource=float(List_city_gps[m][1])
                        LongitudeSource=float(List_city_gps[m][2])
                    if List_city_gps[m][0]==city_destination1:
                        LatitudeGoal=float(List_city_gps[m][1])
                        LongitudeGoal=float(List_city_gps[m][2])
                gValue=0
                hValue=0
                fvalue=0
                new_path[1]=fvalue
                distance = float(List_Road_Segments[i][2])
                new_path.append(distance)
                new_path.append(float(distance/float(List_Road_Segments[i][3])))
                new_path.append(List_Road_Segments[i][1])
                for n in xrange(2, len(new_path)-2, 3):
                    gValue+=new_path[n]
                hValue=CalculateHeuristicsDistance(LatitudeSource,LongitudeSource,LatitudeGoal,LongitudeGoal)
                fvalue=gValue+hValue
                new_path[1]=fvalue
                if List_Road_Segments[i][1] == city_destination1:
                    sumdistance=0
                    sumtime = 0
                    outputpath=[]
                    for p in xrange(2, len(new_path)-2, 3):
                        sumdistance+=new_path[p]
                    for q in xrange(3, len(new_path)-2, 3):
                        sumtime+=new_path[q]
                    for r in xrange(4, len(new_path), 3):
                        outputpath.append(new_path[r])
                    return round(sumdistance,2), round(sumtime,2), new_path[0],outputpath
                else:
                    ListOpen.append(new_path)

def CalculateHeuristicsDistance(lat1, long1, lat2, long2):

    degrees_to_radians = math.pi/180.0

    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians

    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians

    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) +
           math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )
    return arc*3961
if Routing_Algo=='bfs':
    print bfs(City_Start,City_End)
if Routing_Algo=='dfs':
    print dfs(City_Start,City_End)
if Routing_Algo=='astar':
    print Astar(City_Start,City_End)
#References:
#http://www.movable-type.co.uk/scripts/latlong.html
#http://www.redblobgames.com/pathfinding/a-star/implementation.html

