import copy
from math import *
import random 
import datetime
globalScale = 0.2

class RAND_OBJ:
    def __init__(self, possibleObjects):
        self.possibleObjects = possibleObjects 

        #self.ourIndex = random.randint(0, len(self.possibleObjects)-1)
        #self.ourIndex = 0
        #print( "our index: " + str(self.ourIndex))

    #GLITCH WITH PYTHON: CANNOT DO THE COMMENTED OUT LINE 
    def translate(self, x, y, z):
        #return self.possibleObjects[ random.randint(0, len(possibleObjects))-1 ].translate(x,y,z)
        #random.seed( datetime.time().microsecond*2 )

        randomInt = random.randint(0, len(self.possibleObjects)-1)
        return self.possibleObjects[ randomInt ].translate(x,y,z)
    def rotate(self, roll, yaw, pitch):
        #return self.possibleObjects[ random.randint(0, len(possibleObjects))-1 ].rotate(roll,yaw,pitch)
        #print( str(random.seed( datetime.time().microsecond )))
        #random.seed( datetime.time().microsecond*2 )

        randomInt = random.randint(0, len(self.possibleObjects)-1)
        return self.possibleObjects[ randomInt ].rotate(roll,yaw,pitch)


class OBJ:

# Changed the name to obj. object breaks things

# Changed so that mutator methods return copies. This makes
# it easier on our end to add new objects without worrying about
# whether we've just mutated the same one

# append still appends to the same object

# changed: rotate, scale, translate, transform

    # objType is to index our function dicts by the "types" of the primitives
    def __init__(self, objType=0, filename=None, mtlname=None):
        # want to init with load here
        self.name = ""
        self.vertices = []
        self.textureCoordinates = []
        self.normals = []
        self.faces = []
        self.mtl = []
        self.objType = objType
        if mtlname:
            self.mtlname = mtlname
        #else:
            #self.mtlname = None
        if filename:
            self.load(filename, str(mtlname))
            self.filename = filename
        else:
            self.filename = None

    def __hash__(self):
        if self.filename:
            return hash(self.filename)
        else:
            return hash(self.objType)

    def __eq__(self, other):
        return self.filename == other.filename or self.objType == other.objType

    def __ne__(self, other):
        return self.filename != other.filename or self.objType != other.objType

    def load(self, filename,mtlname="None"):
        #self.__init__()
        self.name = filename[filename.rfind("/")+1:-4]
        if mtlname != "None":
            tmpArray = []
            for line in open(mtlname,"r"):
                if line[0:6] == "newmtl":
                    line = line[0:7] + self.name + line[7:]
                tmpArray.append(line)
            self.mtl.append([mtlname,tmpArray])

        for line in open(filename, "r"):
            data = line.split()
            if len(data) > 0:   
                if data[0] == "v":
                    self.vertices.append([float(i) for i in data[1:4]])
                if data[0] == "vt":
                    self.textureCoordinates.append([float(i) for i in data[1:4]])
                if data[0] == "vn":
                    self.normals.append([float(i) for i in data[1:4]])
                if data[0] == "f":
                    tmpFace = []
                    for f in data[1:]:
                        tmpFace.append([int(i) for i in f.split("/")])
                    self.faces.append(tmpFace)

                if (data[0] == "usemtl"):
                    line = line[0:7] + self.name + line[7:]
                    self.faces.append(line)
        self.scale_self(0.5)

    def copy(self):
        return copy.deepcopy(self)

    def transform(self, x, y, z, roll, yaw, pitch,  s):
        cp = self.copy()
        cp.rotate(roll,yaw,pitch)
        cp.scale(s)
        cp.translate(x,y,z)
        return cp
        """
        self.rotate(roll,yaw,pitch)
        self.scale(s)
        self.translate(x,y,z)
        """

    def translate(self, x, y, z):
        cp = self.copy()
        #for vertex in self.vertices:
        for vertex in cp.vertices:
            vertex[0] += x
            vertex[1] += y
            vertex[2] += z
        return cp

    def scale_self(self, s):
        for vertex in self.vertices:
            vertex[0] *= s
            vertex[1] *= s
            vertex[2] *= s

    def scaleAxis(self, sx, sy, sz):
        cp = self.copy()
        for vertex in cp.vertices:
            vertex[0] *= sx
            vertex[1] *= sy
            vertex[2] *= sz
        return cp
    def scale(self, s):
        cp = self.copy()
        #for vertex in self.vertices:
        for vertex in cp.vertices:
            vertex[0] *= s
            vertex[1] *= s
            vertex[2] *= s
        return cp

    def scale3(self, x,y,z):
        cp = self.copy()
        #for vertex in self.vertices:
        for vertex in cp.vertices:
            vertex[0] *= x
            vertex[1] *= y
            vertex[2] *= z
        return cp

    def rotate(self, roll, yaw, pitch):
        roll = radians(roll)
        yaw = radians(yaw)
        pitch = radians(pitch)
        #for vertex in self.vertices:
        cp = self.copy()
        for vertex in cp.vertices:
            x = vertex[0]
            y = vertex[1]
            z = vertex[2]
            if (roll != 0):
                tmp = cos(roll) * x - sin(roll) * y
                y = sin(roll) * x + cos(roll) * y
                x = tmp
            if (yaw != 0):
                tmp = cos(yaw) * x + sin(yaw) * z
                z = -sin(yaw) * x + cos(yaw) * z
                x = tmp
            if (pitch != 0):
                tmp = cos(pitch) * y - sin(pitch) * z
                z = sin(pitch) * y + cos(pitch) * z
                y = tmp
            vertex[0] = x
            vertex[1] = y
            vertex[2] = z
        return cp


    def append(self, other):
        #The other is going to have a material file saved.
        #Append this into our dataset.

        for data in other.mtl:
            add = True
            for dataIncluded in self.mtl:
                if dataIncluded[0] == data[0]:
                    add = False
                    break
            if add:
                self.mtl.append(data)

        for face in other.faces:
            tmpFace = copy.deepcopy(face)

            try:
                #Quick and easy check if we have a usemtl line (I love python)
                if tmpFace[0:6] == "usemtl":
                    
                    self.faces.append(tmpFace)
                else:
                    raise Exception
            except:
                for f in tmpFace:
                    f[0] += len(self.vertices)
                    if len(f) > 1:  
                        f[1] += len(self.textureCoordinates)
                    if len(f) > 2:  
                        f[2] += len(self.normals)
                self.faces.append(tmpFace)

        for vertex in other.vertices:
            self.vertices.append(vertex)

        for textureCoordinate in other.textureCoordinates:
            self.textureCoordinates.append(textureCoordinate)
        
        for normal in other.normals:
            self.normals.append(normal)

    def compress(self):
        uniq = {}
        orig = {}
        new_index = 1
        actual_index = 1
        for vertex in self.vertices:
            key = tuple(vertex)
            if key not in uniq:
                uniq[key] = new_index
                orig[actual_index] = new_index
                new_index += 1
            
            #uniq[tuple(vertex)] = 
            

    def write(self, objname):
        #self.compress()
        self.scale_self(globalScale)
        mtlname = objname[:-4] + ".mtl"
        with open(objname, 'w') as f:
            f.write("mtllib " + mtlname.split("/")[-1] + '\n')

            for vertex in self.vertices:
                f.write('v '+ ' '.join([str(round(i,3)) for i in vertex]) + '\n')
            f.write('\n')

            for textureCoordinate in self.textureCoordinates:
                f.write('vt '+ ' '.join([str(round(i,3)) for i in textureCoordinate]) + '\n')
            f.write('\n')

            for normal in self.normals:
                f.write('vn '+ ' '.join([str(round(i,3)) for i in normal]) + '\n')
            f.write('\n')

            for face in self.faces:
                #Include logic to deal with usemtl lines.
                if face[0] == "u":
                    f.write(face + "\n");
                else:
                    f.write('f')
                    for w in face:
                        f.write(' ' + '/'.join([str(i) for i in w]))          
                    f.write('\n')

            f.close()


        with open(mtlname, 'w') as f:
            for data in self.mtl:
                for line in data[1]:
                    f.write(line)
            f.close()

def main():
    obj = OBJ()
    obj2 = OBJ()
    obj.load("models/cube/Cube.obj","models/cube/Cube.mtl")
    obj2.load("models/kitkat/kitkat_emissive_type4.obj","models/kitkat/kitkat_emissive_type4.mtl")
    obj2.transform(1,4,5,45,45,77,2)
    
    obj.append(obj2)
    obj.write("test.obj")
    print(len(obj.vertices))
    print(obj.faces)
    

if __name__ == "__main__": main()

