import math
from random import *
from collections import OrderedDict
from png import *
import copy

#TEST FOR KYLE PURPOSES SEE THIS ===================
# ===========================================================
# ===========================================================
# ===========================================================
# ===========================================================
seed(171717)

class voronoi:

    def __init__(self, cityL, cityW, s, factorD, name, roadScale, cubeDemo):

        self.cityName = name
        self.buildings = []

        self.cityL = cityL
        self.cityW = cityW
        self.s = s
        self.factorD = factorD
        self.roadScale = roadScale
        self.cubeDemo = bool(cubeDemo)




    #Read from a cty file and construct a list of objects (currently just building)
    def read(self, filename):
        P = []
        with open(filename, 'r') as f:
            tmpList = f.readlines()
            infoDict = OrderedDict()
            for line in tmpList:
                data = line.split()
                #Skip empty line and comments
                if len(data)>0 and data[0][0] != '#':
                    #Type signifies the start of a new object
                    if data[0] == 'NewPoint':
                        #Append old object
                        if len(infoDict) > 0:
                            if len(subDict) > 0:
                                subPoints.append(subDict)
                            infoDict['subPoints'] = subPoints
                            P.append(infoDict)
                        infoDict = OrderedDict()
                        subDict = OrderedDict()
                        defaultDict = OrderedDict()
                        parsingSub = False
                        subPoints = []
                        infoDict['x'] = int(data[1])
                        infoDict['z'] = int(data[2])
                        #Set the current list to append, currently only building
                    elif data[0] == 'SubPoint':
                        if not parsingSub:
                            parsingSub = True
                            defaultDict = copy.deepcopy(infoDict)
                        if len(subDict) > 0:
                            subPoints.append(subDict)
                        subDict = copy.deepcopy(defaultDict)
                        subDict['x'] = int(data[1])
                        subDict['z'] = int(data[2])
                    else:
                        if parsingSub:
                            d = subDict
                        else:
                            d = infoDict
                        #Append the parameters
                        if data[0] == 'pVector':
                            d[data[0]] = (data[2],data[3],data[4],data[5])
                        else:
                            d[data[0]] = data[2]
        #Append the last object
        if len(infoDict) > 0:
            if len(subDict) > 0:
                subPoints.append(subDict)
            infoDict['subPoints'] = subPoints
            P.append(infoDict)
        #print P
        return P

    # Generate a list of information enocding each unique building
    def getBuildingList(self):
        P = self.read("cityPlan.vor")
        n = 0
        #cityL = 800
        cityL = self.cityL
        cityW = self.cityW
        #cityW = 600
        #Scale to the actual scene
        #s = 1
        s = self.s
        #Divide density by this: density/factorD = # buildings 
        #factorD = 1
        factorD = self.factorD
        #Scale road size by this. You want it to be larger with smaller s, not related to s for better customizability
        #roadScale = 1
        roadScale = self.roadScale
        #Using Cube or not
        #cubeDemo = False
        cubeDemo = self.cubeDemo

        districts = [[] for data in P]
        subDistricts = [[[] for j in range(0,len(P[i].get('subPoints')))] for i in range(0,len(P))]
        #print subDistricts
        gridMap = [[0 for i in range(0,cityL+1)] for j in range(0,cityW+1)]
        for i in range(0,cityL):
            for j in range(0,cityW):
                nearest = []
                k = 0
                for data in P:
                    nearest.append((abs(i-data.get('x'))+abs(j-data.get('z')),k))
                    k += 1
                nearest = sorted(nearest, key=lambda tup: tup[0])
                roadSize = (float(P[nearest[1][1]].get('roadSize')) + float(P[nearest[0][1]].get('roadSize'))) * roadScale
                if nearest[1][0] - nearest[0][0] > roadSize:
                    districts[nearest[0][1]].append((i,j,nearest[0][1],nearest[1][1]))
                else:
                    gridMap[j][i] = 1

        for i in range(0,len(subDistricts)):
            j = 0
            for item in districts[i]:
                subP = P[i].get('subPoints')
                x = item[0]
                z = item[1]
                nearest = []
                k = 0
                for data in subP:
                    nearest.append((abs(x-data.get('x'))+abs(z-data.get('z')),k))
                    k += 1
                nearest = sorted(nearest, key=lambda tup: tup[0])
                roadSize = (float(P[nearest[1][1]].get('roadSize')) + float(P[nearest[0][1]].get('roadSize'))) * roadScale
                if nearest[1][0] - nearest[0][0] > roadSize:
                    subDistricts[i][nearest[0][1]].append((x,z,nearest[0][1],nearest[1][1],item[2],item[3]))
                else:
                    gridMap[z][x] = 1
                j += 1

        def getP(a,b):
            return P[a].get('subPoints')[b]
    
        for i in range(0,len(subDistricts)):
            #for item in districts[i]:
            for j in range(0,len(subDistricts[i])):
                density = int(getP(i,j).get('density'))/factorD
                if len(subDistricts[i][j]) == 0:
                    density = -1
                tidyness = float(getP(i,j).get('tidyness'))
                gridSize = int(getP(i,j).get('gridSize'))
                pVector = [float(item) for item in getP(i,j).get('pVector')]
                height = getP(i,j).get('height')
                width = getP(i,j).get('width')
                length = getP(i,j).get('length')
                yaw = "90*a*a*a"

                #print height
                for k in range(0,density * 10):
                    if density == 0:
                        break
                    l = randint(0,len(subDistricts[i][j])-1)
                    item = subDistricts[i][j][l]
                    x = item[0]
                    z = item[1]   
                    roulette = random()
                    tidy = False
                    if roulette < tidyness:
                        tidy = True
                        x = int(round(float(x)/gridSize) * gridSize)
                        z = int(round(float(z)/gridSize) * gridSize)
                    roulette = random()
                    if roulette > gridMap[z][x]:
                        density -= 1

                        name = self.cityName + '/building' + str(n) + '.obj'
                        a = random()*1
                        H = int(eval(height))
                        #print( str(H))
                        W = int(eval(width))
                        L = int(eval(length))
                        Y = 0
                        if not tidy:
                            Y = int(eval(yaw))
                        #type
                        
                        #Total arbitrary collision avoidance
                        WW = (float(W)/s)
                        for o in range(0,int(WW)):
                            for p in range(0,o+1):
                                q = o-p
                                if q>0:
                                    try:    
                                        gridMap[z+p][x+q] = min(gridMap[z+p][x+q]+((WW-o)/WW)**2, 1)
                                    except:
                                        pass
                                if p>0:
                                    try:
                                        gridMap[z+p][x-q] = min(gridMap[z+p][x-q]+((WW-o)/WW)**2, 1)
                                    except:
                                        pass
                                if p>0:
                                    try:
                                        gridMap[z-p][x+q] = min(gridMap[z-p][x+q]+((WW-o)/WW)**2, 1)
                                    except:
                                        pass
                                if q>0:
                                    try:
                                        gridMap[z-p][x-q] = min(gridMap[z-p][x-q]+((WW-o)/WW)**2, 1)
                                    except:
                                        pass
                        gridMap[z][x] = 1

                        #Scale 
                        x *= s
                        z *= s

                        t = 0
                        roulette = random()
                        if roulette < pVector[0]:
                            t = 1
                        elif roulette < pVector[0] + pVector[1]:
                            t = 2
                        elif roulette < pVector[0] + pVector[1] + pVector[2]:
                            t = 3
                        else:
                            t = 4

                        if cubeDemo:
                            t = 0

                        #changed to OrderedDict to facilitate file storage
                        infoDict = OrderedDict([
                            ('name', name),
                            ('type', str(t)),
                            ('length', str(L)),
                            ('width', str(W)),
                            ('height', str(H)),
                            #('length', str(randint(10,15))),
                            #('width', str(randint(10,12))),
                            #('height', str(randint(20,30))),
                            ('x', str(x)),
                            ('y', str(0)),
                            ('z', str(z)),
                            # TODO: Apply random YPR?
                            ('yaw', str(Y)),
                            ('pitch', str(0.0)),
                            ('roll', str(0.0))
                        ])

                        #del(subDistricts[i][j][l])
                        self.buildings.append(infoDict)
                        n+=1
        #print self.buildings
        
        #CODE FOR DISTRICT, NOW USING SUBDISTRICTS
        #for i in range(0,len(districts)):
        #    #for item in districts[i]:
        #    for j in range(0,int(P[i].get('density'))/5):
        #        if len(districts[i]) == 0:
        #            break
        #        k = randint(0,len(districts[i])-1)
        #        item = districts[i][k]
        #        name = self.cityName + '/building' + str(n) + '.obj'
        #        x = item[0]*1
        #        z = item[1]*1
        #        H = i
        #        #changed to OrderedDict to facilitate file storage
        #        infoDict = OrderedDict([
        #            ('name', name),
        #            ('type', str(0)),
        #            ('length', str(1)),
        #            ('width', str(1)),
        #            ('height', str(5)),
        #            #('length', str(randint(12,20))),
        #            #('width', str(randint(10,13))),
        #            #('height', str(randint(10,15))),
        #            ('x', str(x)),
        #            ('y', str(0)),
        #            ('z', str(z)),
        #            # TODO: Apply random YPR?
        #            ('yaw', str(0.0)),
        #            ('pitch', str(0.0)),
        #            ('roll', str(0.0))
        #        ])

        #        del(districts[i][k])
        #        #gridMap[z][x] = 0.5
        #        #self.buildings.append(infoDict)
        #        n+=1
        ##print self.buildings

        imgArray=[[int(gridMap[i][j]*255) for j in range(0,cityL)] for i in range(0,cityW)]
        img = from_array(imgArray,'L')
        img.save("foo.png")
        return self.buildings

def main():
    img = from_array([[255,0,0],[255,0,0]],'L')
    img.save("foo.png")
    print "troll"
if __name__ == "__main__": main()
