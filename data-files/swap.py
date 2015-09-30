from sys import argv
import re

# 1st argument file name
# hard coded 232 buildings, won't work other wise
# 2nd argument: None-> use swap.cfg to turn on specific building. 
#               1->turn on everything 
#               0(actually anything)->turn off everything

if len(argv) < 2:
    print("Input file name")
    exit()

switch = [0 for i in range(0,232)]
if len(argv) < 3:
    print("Using swap.cfg by default, input 0 to turn all off and 1 to turn all on")
    f = open('swap.cfg','r')
    n = 0
    for line in f.readlines():
        switch[n] = int(line.split()[1])
        n+=1
else:
    if int(argv[2]) == 1:
        switch = [1 for i in range(0,232)]

print switch


f = open(argv[1],'r')
lines = f.readlines()
f.close()

#repl = { "testVoronoi/finalBuilding" : "testVoronoi/building", "testVoronoi/building" : "testVoronoi/finalBuilding" }
result = ""

for line in lines:
    a = re.findall('\d+.obj',line)
    if len(a) > 0:
        d = int(a[0][0:-4])
        if switch[d] == 1:
            line = line.replace('building','finalBuilding')
        else:
            line = line.replace('finalBuilding', 'building')
    result += line

#print result
f = open(argv[1],'w')
f.write(result)

#f = open('swap.cfg','w')
#for i in range(0,232):
#    f.write(str(i) + " " + '0\n')
#f.close()

