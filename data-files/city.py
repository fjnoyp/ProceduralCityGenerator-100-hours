from buildingType import *
from building import *
from gridGenerator import *
from randomPlacement import *
from voronoi import *
from cityIO import *
import math
import random
import os
import sys
import shutil

SEED = random.randint(0,100000000)
print("SEEDED WITH " + str(SEED))

# TODO: CLEAN UP COMMENTED CODE AT FINISH
globalScale = 0.2

class cityLayout:
    
    def __init__(self, buildings, name, usingGrid = False):
        # Get generator settings and create buildings
        self.buildings = buildings
        self.numBuildings = len(buildings)
        self.name = name
        self.usingGrid = usingGrid

    def makeCity(self):
        if os.path.exists(self.name):
            shutil.rmtree(self.name)
        os.makedirs(self.name)

        with open(self.name+'.scn.any', 'w') as sceneFile:

            # write building types and models
            buildings= self.buildings
            sceneFile.write('{\n    models = {\n\n')

            # write street model
            #sceneFile.write('        streetModel = ArticulatedModel::Specification {\n')
            #sceneFile.write('            filename = "model/crate/crate.obj";\n')
            #sceneFile.write('            preprocess = {\n')
            #sceneFile.write('                setMaterial(all(), "streetBlock.jpg");\n')

            #sceneFile.write('                transformGeometry(all(), Matrix4::scale(' + str(buildings[0].get('blockSize') * globalScale) + ', 0.2, ' + str(buildings[0].get('blockSize') * globalScale) + '));\n')
            #sceneFile.write('            };\n')
            #sceneFile.write('        };\n\n')

            # write building models
            for i in range(self.numBuildings):
                building = self.buildings[i]

                # Generate Building
                name = building.get('name')
                print("Generating " + name)
                tipe = BuildingType(int(building.get('type'))) #BuildingType()
                generateBuilding(int(building.get('length')), int(building.get('height')), int(building.get('width')), tipe, name, SEED)

                #if self.usingGrid:
                #    sceneFile.write('        buildingModel' + str(i) + ' = ArticulatedModel::Specification {\n')
                #    sceneFile.write('            filename =  \"' + buildings[i].get('name') + '\"; \n')
                #    sceneFile.write('        };\n\n')

                sceneFile.write('        buildingModel' + str(i) + ' = ArticulatedModel::Specification {\n')
                sceneFile.write('            filename =  \"' + buildings[i].get('name') + '\"; \n')
                sceneFile.write('        };\n\n')

            # start writing entities
            sceneFile.write('   };\n\n     entities = {\n\n')
            sceneFile.write('        camera = Camera {\n\n')
            sceneFile.write('            frame = CFrame::fromXYZYPRDegrees(13.8, 17.2, -22.5, 176.7, -8.4 );\n')
            sceneFile.write('        };\n\n')


            # write building entities
            for i in range(self.numBuildings):
                building = self.buildings[i]

                # Build the string of parammeters for XYZYPR
                params = str(float(building.get('x')) * globalScale) + ', ' + str(float(building.get('y')) * globalScale) + ', ' + str(float(building.get('z')) * globalScale) + ', ' + building.get('yaw') + ', ' + building.get('pitch') + ', ' + building.get('roll')

                sceneFile.write('        building' + str(i) + ' = VisibleEntity {\n')
                sceneFile.write('            model = "buildingModel' + str(i) + '";\n')
                sceneFile.write('            frame = CFrame::fromXYZYPRDegrees(' + params + ' );\n')
                sceneFile.write('        };\n\n')

            #    if self.usingGrid:
            #        # Build the street for the block.
            #        sceneFile.write('        street' + str(i) + ' = VisibleEntity {\n')
            #        sceneFile.write('            model = "streetModel";\n')
            #        sceneFile.write('            frame = CFrame::fromXYZYPRDegrees(' + str((int(building.get('x')) + 0.16*building.get('blockSize')) * globalScale) + ',' + '0' + ', ' + str((int(building.get('z')) + 0.16*building.get('blockSize')) * globalScale) + ', ' + building.get('yaw') + ', ' + building.get('pitch') + ', ' + building.get('roll') + ' );\n')
            #        sceneFile.write('        };\n\n')
                
            # write skybox and lighting 

            sceneFile.write('       skybox = Skybox { \n')
            sceneFile.write('           texture ="cubemap/whiteroom/whiteroom-*.png"; \n')
            sceneFile.write('       }; \n')
            sceneFile.write('       sun = Light { \n')
            sceneFile.write('           attenuation = ( 0, 0, 1 ); \n')
            sceneFile.write('           bulbPower = Power3(4e+006 ); \n')
            sceneFile.write('           frame = CFrame::fromXYZYPRDegrees(-15, 207, -41, -164, -77, 77); \n')
            sceneFile.write('           nearPlaneZLimit = -100; \n')
            sceneFile.write('           shadowMapSize = Vector2int16(2048, 2048 ); \n')
            sceneFile.write('           spotHalfAngleDegrees = 20; \n')
            sceneFile.write('           spotSquare = true; \n')
            sceneFile.write('           type = "SPOT"; \n')
            sceneFile.write('       }; \n')

            sceneFile.write('    };\n')
            sceneFile.write('   name = "' + self.name + '"\n')
            sceneFile.write('};')
            sceneFile.close()
            return

def main():
    # read settings from cfg files to avoid having to modify vode.
    # set the directory to the path of the script to allow running it from any place
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    def toInt(l):
        for x in l:
            try:
                yield int(x)
            except ValueError:
                yield x

    with open(sys.argv[1], 'r') as f:
        tmpList = f.read().split()
        config = list(toInt([tmpList[3*i+2] for i in range(len(tmpList)/3)]))
        if config[0] == 'gridGenerator':
            print("Using Grid Generator")
            generator = gridGenerator(config[1], config[2], config[3], config[4], config[5], config[6], config[7])
            city = cityLayout(generator.getBuildingList(), config[5], True)
        elif config[0] == 'cityLoader':
            print("Loading data from " + config[1] + "...")
            cityLoader = cityIO()
            cityLoader.read(config[1])
            city = cityLayout(cityLoader.getBuildingList(), config[2])
        elif config[0] == 'randomPlacement':
            print("Using Random Generator")
            generator = randomPlacement(config[1], config[2], config[3], config[4], config[5], config[6], config[7])
            city = cityLayout(generator.getBuildingList(), config[5])
        elif config[0] == 'voronoi':
            print("Using Voronoi Generator")
            generator = voronoi(config[1], config[2], config[3], config[4], config[5], config[6], config[7])
            city = cityLayout(generator.getBuildingList(), config[5])
        else:
            print("Error: generator type " + config[0] + " is not defined")
        f.close()

    print("Generating...")
    city.makeCity()
    print("Done")

if __name__ == "__main__": main()
