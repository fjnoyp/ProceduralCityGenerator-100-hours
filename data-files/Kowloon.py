from buildingType import *

class Kowloon(Building):
    
    def __init__(self, length, width, max_height, seed):
        Building.__init__(self, length=length, width=width, max_height=max_height, seed=seed)
        
        # Create a rectangle of random dims in random loc on floorplan
        base_width = width - 2
        base_length = length - 2
        
        buff = 1
        
        # Establish build bounds
        base_start_x = random.randint(buff, width - buff - base_width )
        base_start_z = random.randint(buff, length - buff - base_length )
        
        # Establish where it can build
        for r in range( base_start_x, base_start_x + base_width ):
            for c in range( base_start_z, base_start_z + base_length ):
                if random.randint(0,4) == 0:
                    self.floorplan[r][c] = True
                    self.terminated[r][c] = False
        
        # Ways that this building can begin
        self.axioms = [tex_cube_obj.copy()]
        
        # Story type
        self.nonterminals = [tex_cube_obj.copy()]
        
        # True terminals (vertical)
        self.terminals = [tex_cube_obj.copy(), 
                          small_cyl_obj.copy(),
                          full_rad_cyl_obj.copy(),
                          half_rad_cyl_obj.copy(),
                          empty_obj.copy()
        ]
        
        # Outward terminals
        self.decorators = [ kitkat_obj.translate(0.6, 0, 0),
                            vent_obj.translate(1,0,0)
        ]
        
        
        self.rules = {tex_cube_obj : [ self.terminate,
                                   self.foundation,
                                   self.repeatUp, 
                                   self.repeatUpAll,
                                   self.repeatUpGroup,
                                   self.decorate],
                      full_rad_cyl_obj : [ self.repeatUp ] 
        }
        
        self.rules[empty_obj] = [ self.terminate,
                                  self.repeatUp,
                                  self.repeatUpAll,
                                  self.repeatUpGroup,
                                  self.terminate
        ]
        
        
        if not __name__ == "__main__":
            self.expand()
            for i in range(3):
                self.clean()
            # separated for demo
            #return
            for r in range(len(self.grid)):
                for c in range(len(self.grid[r])):
                    self.decorate(self.grid[r][c], r, c)
        else:
            for r in range(len(self.grid)):
                for c in range(len(self.grid[r])):
                    self.foundation(self.grid[r][c], r, c)
            print("Skipping expand")


    def decorate(self, stack, r, c):
        """This should push something outwards from face, ie a terminal, and terminate that out-facing
        stack"""
        try:
            upto = len(stack) 
            for i in range(min(len(stack), 2), upto):
                # push everything at same height into top
                # only cubes are reguar enough to have things plastered on them
                if stack[i] != tex_cube_obj:
                    continue
                for a in range(0, 361, 90):
                    #lim = (len(self.decorators) - 1, -1)[i == len(stack) - 2]
                    x = random.randint(0, len(self.decorators)-2)
                    x = (x,0)[random.randint(0,4)>0]
                    x = (x, -1)[ i == len(stack) - 3 ]
                    stack.append( self.decorators[x] )
                    stack[-1] = stack[-1].rotate(yaw=a,pitch=0,roll=0).translate(r, i, c)

        except:
            pass

        
    def clean(self):
        for r in range( len(self.grid) ):
            for c in range( len(self.grid[r]) ):
                stack = self.grid[r][c]
                if len(stack) < 3:
                    del stack[:]
                    continue
                if len(stack) >= 2 and stack[1].objType == 3:
                    stack[0] = delete_obj
                for i in range(len(stack)):
                    try:
                        all_block = stack[i+1].objType != 3 and stack[i-1].objType != 3
                        if not all_block:
                            continue
                        for dr in range(-1, 2):
                            for dc in range(-1, 2):
                                if dr == dc == 0:
                                    continue
                                s2 = self.grid[r + dr][c + dc]
                                if len(s2) > i and (s2[i].objType == 3):
                                    all_block = False
                                    break
                                elif len(s2) < i:
                                    all_block = False
                                    break
                        if all_block:
                            stack[i] = delete_obj
                    except:
                        pass
                    
        
    def expand(self):
        while not all([done for sublist in self.terminated for done in sublist]):
            for r in range( len(self.grid) ):
                for c in range( len(self.grid[0]) ):
                    if self.floorplan[r][c] and not self.terminated[r][c]:

                        stack = self.grid[r][c]
                        
                        if self.MAX_HEIGHT == 1: 
                            self.terminate(stack, r, c)
                            continue
                        if not stack:
                            # Initialize with axioms
                            self.foundation(stack, r, c)
                            # for demoing
                            #print(stack[0])
                            #self.terminated[r][c] = True
                            continue
                        top_obj = stack[-1]
                        rules = self.rules[ top_obj ]

                        func_i = None
                        if len(stack) >= self.MAX_HEIGHT - 1:
                            func_i = 0 # Terminate
                        else:
                            rand = random.randint(0,7)
                            if rand == 0:
                                func_i = rules.index(self.repeatUpAll)
                                func_i = 0
                            else:
                                func_i = rules.index(self.repeatUpGroup)
                                
                        f = rules[func_i]
                        f(stack, r, c)


    def foundation(self, stack, r, c):
        if not stack and self.floorplan[r][c] and not self.terminated[r][c]:
            stack.append( self.axioms[0].translate(r, 0, c) )

    def terminate(self, stack, r, c):
        self.terminated[r][c] = True
        if len(stack) < 2:
            return
        #stack.append( self.terminals[0].translate(r, len(stack), c) )
        #rnd = random.randint(0, len(self.terminals)-2)
        rnd = -random.randint(1, 3)
        rnd = (rnd, -1)[random.randint(0,1)]
        term = self.terminals[rnd]#.translate(r, len(stack), c)
        #stack.append( self.terminals[rnd].translate(r, len(stack), c) )
        for i in range(1 + random.randint(0,5) * (term == full_rad_cyl_obj or term == half_rad_cyl_obj)):
            stack.append( term.translate(r, len(stack)-1, c) )
        #stack.append( full_rad_cyl_obj.translate(r, len(stack) + .1, c) )

    def repeatUp(self, stack, r, c):
        stack.append( stack[-1].translate(0, 1, 0) )

    def repeatUpGroup(self, stack, r, c):
        """Isolate some rectangle and repeat them up"""
        for_bound = back_bound = c
        up_bound = down_bound = r
        
        level = len(self.grid[r][c]) # want everything to be up at the height of this stack

        # If there isn't a cube in the expansion area, put one there at the right height
        # If there is a cube higher than it in the expansion area, don't put anything there
        #buffer_max = (1, 0)[len(stack) > 1]
        buffer_max = random.randint(0, 4)

        up_bound = max(r - random.randint(3, 7), buffer_max)
        down_bound = min(r + random.randint(3, 7), len(self.grid) - buffer_max)

        for_bound = min(c + random.randint(3, 7), len(self.grid[0]) - buffer_max)
        back_bound = max(c - random.randint(3, 7), buffer_max)

        upto = random.randint(3,7) # Repeat each up to some height
        for ri in range(up_bound, down_bound ):
            for ci in range(back_bound, for_bound ):
                if len(self.grid[ri][ci]) > level:
                    return #return # pass for skyscraper thing
                    # RETURN IS GOOD. MANY LARGE BLOCKS
                    
        for ri in range(up_bound, down_bound):
            for ci in range(back_bound, for_bound ):
                if len(self.grid[ri][ci]) > level:
                    #return
                    continue
                while len(self.grid[ri][ci]) < level - 1:
                    self.grid[ri][ci].append( empty_obj.translate(ri, len(self.grid[ri][ci]), ci) )
                self.grid[ri][ci].append( self.nonterminals[0].translate(ri, len(self.grid[ri][ci]), ci) )
                # Things at the same height (or higher, in which case ignoring) as the main stack
                for u in range(upto):
                    self.repeatUp(self.grid[ri][ci], r, c)

    def repeatUpAll(self, stack, r, c):
        """Expand area around this square as much as possible into a larger rect
        which is then all repeated upwards by 1"""
        pass

    def growOut(self, stack, r, c):
        pass


if __name__ == "__main__":
    k = Kowloon(length=10, width=10, max_height = 10)
    k.repeatUpGroup(k.grid[1][1], 1, 1)
    k.to_obj().write("test.obj")
