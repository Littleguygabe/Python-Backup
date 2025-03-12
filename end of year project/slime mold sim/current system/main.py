import pygame, sys, random, math, time, ctypes,gui,dbfunctions,os,numpy
pygame.init()

#USE A STACK TO MOVE AGENTS FROM NODE TO NODE
#[]use zones to decide which node to target
class agent():
    def __init__(self,sw,sh,screen,nodeattributes,generation,allNodesFound,agentID,squaresize,settings):
        self.__ID = agentID
        self.nodecollided = False
        self.visitedStack = []
        self.allNodesReached = False
        
        self.collisionDist = squaresize
        self.agentsize = 2
        self.sw = sw
        self.sh = sh

        self.x = random.randint(self.agentsize,sw-self.agentsize)
        self.y = random.randint(self.agentsize,sh-self.agentsize)
        self.screen = screen

        self.opacity = 40#as a percentage
        self.nodeAttributes = nodeattributes
        
        self.visibleNodes = []        
        self.setVisibleNodes()
        self.generation = generation
        self.gen2xtarget = None
        self.gen2ytarget = None
        
        #attributes that need to come from gui.agentConfig
        self.curiosityVal = settings[1]
        self.tailLen = settings[2]
        self.movementInterval = settings[3]
        self.viewDistance = settings[4]
        self.spawnRadius = settings[5]
        self.dispertionMethod = settings[6] #standard,x,spiral\\        

        #point to deincentivise from
        self.deincentiveTargetx = self.sw/2
        self.deincentiveTargety = self.sh/2
        
        self.__buffersize = 5 #percentage of screen
        self.__wallbuffer = ((self.sw*(self.__buffersize/100))+(self.sh*(self.__buffersize/100)))/4
        
        self.shortestPath = []
        self.generationReset = False
        self.nPoints2Follow = 0
        self.followedPoints = 0
        self.path2follow = None

        self.allNodesFound = allNodesFound
        self.R = 255
        self.G = 255
        self.B = 255

        self.movementArray = []

    def setVisibleNodes(self):
        for i in range(0,len(self.nodeAttributes),6):
            if self.nodeAttributes[i+3] == 'V':
                self.visibleNodes.append(self.nodeAttributes[i])
        

    def redrawagent(self):
        self.movementArray.append(self.x)
        self.movementArray.append(self.y)

        if len(self.movementArray)>(2*self.tailLen):
            deleteRect = pygame.Surface((self.agentsize,self.agentsize))
            deleteRect.fill((0,0,0))
            self.screen.blit(deleteRect,(self.movementArray[0],self.movementArray[1]))

            for i in range(0,2):
                del self.movementArray[0]

        for i in range(0,len(self.movementArray),2):
            agentRect = pygame.Surface((self.agentsize,self.agentsize))
            agentRect.fill((self.R,self.G,self.B))
            agentRect.set_alpha((self.opacity/100)*255)
            self.screen.blit(agentRect,(self.movementArray[i],self.movementArray[i+1]))
    
    def calculateIncentives(self,xtarget,ytarget):
        if xtarget == 0 and ytarget == 0:
            return 0,0
            
        xdif = xtarget-self.x
        ydif = ytarget-self.y
        
        #CAST DIAGRAM
        if abs(xdif)>=abs(ydif):

            xincentive = random.randint(1,self.movementInterval)
            try:
                yincentive = (xincentive/xdif)*ydif
            except:
                yincentive = 0
            if xdif<0:
                xincentive*=-1
                yincentive*=-1
        
        else:
            yincentive = random.randint(1,self.movementInterval)
            try:
                xincentive = (yincentive/ydif)*xdif
                
            except:
                xincentive = 0
            if ydif<0:
                yincentive*=-1
                xincentive*=-1
            
        #print(f'{self.__IDf} incentives x: {xincentive}, y: {yincentive} & targetting ({self.gen2xtarget}, {self.gen2ytarget})')

        return(xincentive,yincentive)

    def calculateDeincentives(self,xtarget,ytarget):

        xdif = self.x - xtarget
        ydif = self.y - ytarget
        
        if self.dispertionMethod == 'standard':
            
            if xdif == 0:
                xdif+=1e-10
                
            if ydif == 0:
                ydif += 1e-10
            
            self.angle = math.atan(xdif/ydif)
            xdeincentive = self.movementInterval
            ydeincentive = xdeincentive/(math.tan(self.angle)) #standard ball dispersion
        
        elif self.dispertionMethod == 'x':
            self.angle = math.atan(ydif/xdif)
            xdeincentive = self.movementInterval
            ydeincentive = xdeincentive/(math.tan(self.angle)) #X dispersion
        
        elif self.dispertionMethod == 'spiral':
            self.angle = math.atan(xdif/ydif)
            if self.angle<=5/(180*math.pi):
                xdeincentive = self.movementInterval
                ydeincentive = xdeincentive/(math.tan(self.angle))
            else:
                ydeincentive=self.movementInterval
                xdeincentive = ydeincentive*(math.tan(self.angle)) #spiral dispersion
        

        if self.x<self.sw/2:
            xdeincentive*=-1
            ydeincentive*=-1

        if self.y<=self.__wallbuffer:
            #deflection from heading right-up to right-down
            if self.angle<0 and ydeincentive<=0 and xdeincentive>=0:
                self.angle*=-1
                ydeincentive*=-1
            
            #deflection from heading left-up to left-down
            if self.angle>0 and ydeincentive<=0 and xdeincentive<=0:
                self.angle*=-1
                ydeincentive*=-1

        #lower wall
        if self.y+self.agentsize>=self.sh-self.__wallbuffer:
            #deflection from heading right-down to right-up
            if self.angle>0 and ydeincentive>=0 and xdeincentive>=0:
                self.angle*=-1
                ydeincentive*=-1
                

            #deflection from heading left-down to left-up
            if self.angle<0 and ydeincentive>=0 and xdeincentive<=0:
                self.angle*=-1
                ydeincentive*=-1
        
        #left wall
        if self.x<=self.__wallbuffer:
            #deflection from heading left-up to right-up
            if self.angle>0 and ydeincentive<=0 and xdeincentive<=0:
                self.angle*=-1
                xdeincentive*=-1

            #deflection heading from left-down to right-down
            if self.angle<0 and ydeincentive>=0 and xdeincentive<=0:
                self.angle*=-1
                xdeincentive*=-1

        #right wall
        if self.x+self.agentsize>=self.sw-self.__wallbuffer:
            #deflection from heading right-up to left-up
            if self.angle<0 and ydeincentive<=0 and xdeincentive>=0:
                self.angle*=-1
                xdeincentive*=-1
            
            #deflection from heading right-down to left-down
            if self.angle>0 and ydeincentive>=0 and xdeincentive>=0:
                self.angle*=-1
                xdeincentive*=-1

        return(xdeincentive,ydeincentive)

    def findRandomNode(self):
        if len(self.visibleNodes) == 0:
            self.allNodesReached = True
            return 0,0
        index = random.randint(0,len(self.visibleNodes)-1)
        node = self.visibleNodes[index]                   
        return self.nodeAttributes[((node-1)*6)+1], self.nodeAttributes[((node-1)*6)+2]

    def checkNodeCollision(self):
        for i in range(0,len(self.nodeAttributes),6):
            #+0>NID +1>X +2>Y +3>V/N +4>Colour +5>F/N
            #calculate distance to center of the node
            xdist = self.x-self.nodeAttributes[i+1]
            ydist = self.y-self.nodeAttributes[i+2]
            if math.sqrt((xdist**2)+(ydist**2))<=self.collisionDist:
                if self.search(self.nodeAttributes[i+1]) == False:    
                    self.visitedStack.append((self.nodeAttributes[i+1],self.nodeAttributes[i+2]))
                    self.nodecollided = True
                    self.nodeAttributes[i+5] = 'F'
                    self.updateVisibleNodes(self.nodeAttributes[i])
                    
                    if self.generation>=3:
                        self.followedPoints+=1
                    
    def updateVisibleNodes(self,nodeID):
        #print(f'nodeID: {nodeID}, Angle: {math.degrees(self.angle)}')
        self.visibleNodes.remove(nodeID)
        
    def search(self,target):
        for i in range(0,len(self.visitedStack)):
            if self.visitedStack[i][0] == target:
                return True
        
        return False
        
    def move(self):
        if self.generation>=3:
            self.checkNodeCollision()
            self.nPoints2Follow = self.generation - 2
            if self.followedPoints<=self.nPoints2Follow:
                #print(self.visitedStack)
                if self.path2follow == None:
                    self.path2follow = []
                    nearestx,nearesty = self.findNearestNode()
                    
                    #search for the position of the closest in the path
                    for i in range(len(self.shortestPath)):
                        if self.shortestPath[i][0] == nearestx and self.shortestPath[i][1] == nearesty:
                            currentIndexPos = i
                            
                    for i in range(1,self.nPoints2Follow+1):
                        if i+currentIndexPos<len(self.shortestPath):
                            nextPosition = self.shortestPath[i+currentIndexPos]
                            
                        else:
                            nextPosition = self.shortestPath[(i+currentIndexPos)-len(self.shortestPath)]
                            
                        self.path2follow.append(nextPosition)
                        
                xtarget = self.path2follow[self.followedPoints-1][0]
                ytarget = self.path2follow[self.followedPoints-1][1]
                
                xincentive,yincentive = self.calculateIncentives(xtarget,ytarget)
                self.x+=xincentive
                self.y+=yincentive

            else:
                #if the agent has collided then find a new target
                if self.nodecollided == True:
                    xtarget,ytarget = self.findRandomNode()
                    self.nodecollided = False
                    self.gen2xtarget,self.gen2ytarget = xtarget,ytarget
                    xincentive,yincentive = self.calculateIncentives(self.gen2xtarget,self.gen2ytarget)
                    self.x+=xincentive
                    self.y+=yincentive
                #otherwise keep moving towards current target
                else:
                    xincentive,yincentive = self.calculateIncentives(self.gen2xtarget,self.gen2ytarget)
                    self.x+=xincentive
                    self.y+=yincentive
                    
                

        if self.generation==2:
            self.checkNodeCollision()
            if self.nodecollided == True:
                xtarget,ytarget = self.findRandomNode()
                self.gen2xtarget,self.gen2ytarget = xtarget,ytarget
                self.nodecollided = False
            
            if self.gen2xtarget == None and self.gen2ytarget == None:
                xtarget,ytarget = self.findRandomNode()
                self.gen2xtarget = xtarget
                self.gen2ytarget = ytarget
                
            else:
                xincentive,yincentive = self.calculateIncentives(self.gen2xtarget,self.gen2ytarget)
                self.x+=xincentive
                self.y+=yincentive              

        if self.generation == 1:
            if not self.allNodesFound:
                xdeincentive, ydeincentive = self.calculateDeincentives(self.deincentiveTargetx,self.deincentiveTargety)

                self.x+=xdeincentive
                self.y+=ydeincentive

            else:
                self.deincentive = False
                xincentive, yincentive = self.calculateIncentives(xtarget,ytarget)
                self.x+=xincentive
                self.y+=(yincentive)
                
        

        #Calculate Random Factor
        xcuriosity = random.randint(0,self.curiosityVal)
        ycuriosity = random.randint(0,self.curiosityVal)

        xRandMultiplier = random.randint(-1,1)
        xcuriosity*=xRandMultiplier

        yRandMultiplier = random.randint(-1,1)
        ycuriosity*=yRandMultiplier

        self.x+=xcuriosity
        self.y+=ycuriosity

    def updatenodeAttributes(self,nodeattributes):
        self.nodeAttributes = nodeattributes

    def updateAllNodesFound(self,allNodesFound):
        self.allNodesFound = allNodesFound

    def generateStartPos(self):
        # center of the circle (x, y)
        centerx = self.sw/2
        centery = self.sh/2
        alpha = 2 * math.pi * random.random()
        randRadius = self.spawnRadius * math.sqrt(random.random())
        # calculating coordinates
        self.x = randRadius * math.cos(alpha) + centerx
        self.y = randRadius * math.sin(alpha) + centery
        
    def checkwallCollision(self):
        if self.x>=self.sw-((self.__wallbuffer*2)+(self.agentsize*(1.2))) or self.x+self.agentsize<=(self.__wallbuffer*2)+(self.agentsize*(1.2)):
            return True
        else: 
            return False
    
    def findNearestNode(self):
        distance = None
        xtarget = None
        ytarget = None
        for i in range(0,len(self.nodeAttributes),6):
            #+0>NID +1>X +2>Y +3>V/N +4>Colour +5>F/N
            xdif = self.x-self.nodeAttributes[i+1]
            ydif = self.y-self.nodeAttributes[i+2]
            tempDistance = math.sqrt((xdif**2)+(ydif**2))
            if distance == None:
                distance = tempDistance
                xtarget = self.nodeAttributes[i+1]
                ytarget = self.nodeAttributes[i+2]
                                
            elif tempDistance<distance:
                distance = tempDistance
                xtarget = self.nodeAttributes[i+1]
                ytarget = self.nodeAttributes[i+2]
                
        return xtarget,ytarget
    
    def reset4NewGeneration(self):
        self.setVisibleNodes()
        self.nPoints2Follow = self.generation-2
        self.followedPoints = 0
        xtarget,ytarget = self.findNearestNode()
        self.path2follow = None
        self.generationReset = True
        for i in range(0,50):
            xincentive, yincentive = self.calculateIncentives(xtarget,ytarget)
            
            self.x+=xincentive
            self.y+=yincentive
            
            xcuriosity = random.randint(0,self.curiosityVal)
            ycuriosity = random.randint(0,self.curiosityVal)

            xRandMultiplier = random.randint(-1,1)
            xcuriosity*=xRandMultiplier

            yRandMultiplier = random.randint(-1,1)
            ycuriosity*=yRandMultiplier

            self.x+=xcuriosity
            self.y+=ycuriosity
        self.generationReset = False
        self.visitedStack = []
        self.redrawagent()
        

class fps():
    def __init__(self,screen,fps,x,y):
        self.screen = screen
        self.fps = fps
        self.fontsize = 20
        self.font = pygame.font.SysFont('Arial', self.fontsize)
        self.x = x
        self.y = y
        self.displayfps()
    
    def displayfps(self):
        blankrect = pygame.Surface((40,self.fontsize))
        blankrect.fill((0,0,0))
        self.screen.blit(blankrect,(self.x,self.y))
        fpstext = self.font.render(str(self.fps),1,(0,255,0))
        self.screen.blit(fpstext,(self.x,self.y))

def checkNodeFound(nodeAttributeArr,allNodesFound,agentArray,nodesize):
    for i in range(0,len(agentArray)):
        foundCount = 0
        x,y = agentArray[i].x,agentArray[i].y
        agentsize = agentArray[i].agentsize

        #check if collided with a node

        for k in range(0,len(nodeAttributeArr),6):
            #+0>NID +1>X +2>Y +3>V/N +4>Colour +5>F/N
            if x+agentsize/2>=nodeAttributeArr[k+1]-nodesize/2 and x-agentsize/2<=nodeAttributeArr[k+1]+nodesize/2 and y+agentsize/2>=nodeAttributeArr[k+2]-nodesize/2 and y-agentsize/2<=nodeAttributeArr[k+2]+nodesize/2:
                #Find which node has been hit
                nodeAttributeArr[k+5] = 'F'
            if nodeAttributeArr[k+5] == 'F':
                foundCount+=1
                nodeAttributeArr[k+4] = (0,255,0) #Active agent colour

                
            if foundCount==len(nodeAttributeArr)/6:
                return nodeAttributeArr,True
                

    return(nodeAttributeArr,allNodesFound)


def progressBar(count,finished):
    progressBarChar = '▊'
    lengthOfBar = 25
    #os.system('cls')
    percent = ((count/finished))
    
    index = round(lengthOfBar*percent,0)
    print('▊',end='')
        
    for i in range(int(index)):
        print(progressBarChar,end='')
        
    for i in range(lengthOfBar-int(index)):
        print(' ',end='')
        
    print(' ',end='')
    print(f'{count}/{finished}',end='\r')

def checkPathLength(path,shortestPathLength,currentShortestPath):
    totalPathLength = 0
    for i in range(len(path)-1):
        xdif = path[i][0]-path[i+1][0]
        ydif = path[i][1]-path[i+1][1]
        totalPathLength+=round(math.sqrt((xdif**2)+(ydif**2)),3)
        
    #update the shortestPathLength
    try:
        if totalPathLength<shortestPathLength:
            return path,totalPathLength
        
    #for when the shortestPathLength is still None
    except:
        return currentShortestPath,totalPathLength
    
    #if the new path isn't shorter then return the original values
    return path, shortestPathLength

def dijkstras(givenPath):
    dijkstrasPath = []
    temparray = []
    for i in range(0,len(givenPath)):
        temparray.append(givenPath[i][0])
        temparray.append(givenPath[i][1])
    basex = temparray[0]
    basey = temparray[1]

    temparray.remove(basex)
    temparray.remove(basey)

    temparray2 = []
    temparray2.append(basex)
    temparray2.append(basey)
    dijkstrasPath.append(temparray2)

    while len(temparray)>0:
        shortestdist = 10000

        for i in range(0,len(temparray),2):
            xdif = basex-temparray[i]
            ydif = basey - temparray[i+1]
            totaldif = math.sqrt((xdif**2)+(ydif**2))
            if totaldif<shortestdist:
                shortestdist=totaldif
                closestx = temparray[i]
                closesty=temparray[i+1]
        temparray.remove(closestx)
        temparray.remove(closesty)
        temparray2 = []
        temparray2.append(closestx)
        temparray2.append(closesty)
        dijkstrasPath.append(temparray2)
        
        basex = closestx
        basey = closesty
        
    return dijkstrasPath

def draw_dashed_line(surf, color, start_pos, end_pos, width=1, dash_length=10):
    x1, y1 = start_pos
    x2, y2 = end_pos
    dl = dash_length

    if (x1 == x2):
        ycoords = [y for y in range(y1, y2, dl if y1 < y2 else -dl)]
        xcoords = [x1] * len(ycoords)
    elif (y1 == y2):
        xcoords = [x for x in range(x1, x2, dl if x1 < x2 else -dl)]
        ycoords = [y1] * len(xcoords)
    else:
        a = abs(x2 - x1)
        b = abs(y2 - y1)
        c = round(math.sqrt(a**2 + b**2))
        dx = dl * a / c
        dy = dl * b / c

        xcoords = [x for x in numpy.arange(x1, x2, dx if x1 < x2 else -dx)]
        ycoords = [y for y in numpy.arange(y1, y2, dy if y1 < y2 else -dy)]

    next_coords = list(zip(xcoords[1::2], ycoords[1::2]))
    last_coords = list(zip(xcoords[0::2], ycoords[0::2]))
    for (x1, y1), (x2, y2) in zip(next_coords, last_coords):
        start = (round(x1), round(y1))
        end = (round(x2), round(y2))
        pygame.draw.line(surf, color, start, end, width)

def startprogram(key,guest=False,fromPrev=False):    
    user32 = ctypes.windll.user32
    screen_width,screen_height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

    screenScale = 85 #size of the window as a percentage of the screen resolution
    screenScale = screenScale/100
    screen_width = round(screen_width*screenScale)
    screen_height = round(screen_height*screenScale)

    screen = pygame.display.set_mode((screen_width,screen_height))
    clock = pygame.time.Clock()
    nodesize = 20
    nodePos = []
    agentarray = []
    
    if fromPrev:
        nodePos = dbfunctions.retrieveSimSettings(key)
        
    nagents=2000

    

    started = False
    spacecount = 0
    generation = 1
    
    FoundAllThreshold = 30 #PERCENTAGE OF AGENTS THAT NEED TO HIT WALL BEFORE GEN2 BEGINS
    FoundAllThreshold = FoundAllThreshold/100

    RED = (255,0,0)
    DARKGREY = (97,97,97)
    BLACK = (0,0,0)
    WHITE = (255,255,255)

    nodeColour = RED
    initialNodeDraw = True

    nodeAttributesCreated = False
    nodeAtrributeArr = []
    agentsCreated = False
    allNodesCollided = False

    loaded = False
    allNodesFound = False
    
    iterateGeneration = False
    agentFinishedCount = 0
    
    shortestPath = []
    shortestPathLength = None
    generationResetting = False
    
    iterateGenerationThreshold = 1
    
    finishedSim = False
    
    os.system('cls')
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                if guest:
                    dbfunctions.deleteUser('guest')
                    
                else:
                    dbfunctions.saveSimSettings(key,nodePos)
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONUP:
                center = pygame.mouse.get_pos()
                centerx = center[0]
                centery = center[1]          
                #so long as the game isn't running then nodes can be placed
                if started == False:
                    nodePos.append(centerx)
                    nodePos.append(centery)

                    nodeAttributesCreated = False
                    
            if event.type == pygame.KEYDOWN:
                #Allow to delete nodes if the sim hasn't started
                if event.key == pygame.K_DELETE and started == False:
                    for i in range(0,len(nodePos),2):
                        node = pygame.Rect(nodePos[i]-(nodesize/2),nodePos[i+1]-(nodesize/2),nodesize,nodesize)
                        pygame.draw.rect(screen,(0,0,0),node)
                    nodePos=[]

                #start the sim once space is pressed
                if event.key == pygame.K_SPACE:
                    if spacecount%2 == 0:
                        started = True
                        spacecount+=1

                    else:
                        started = False
                        spacecount+=1

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    if guest:
                        dbfunctions.deleteSettings('guest')
                    
                    else:
                        dbfunctions.saveSimSettings(key,nodePos)
                    
                    sys.exit()

                #set all nodes to be visible
                if event.key == pygame.K_v:
                    for i in range(0,len(nodeAtrributeArr),6):
                        #+0>NID +1>X +2>Y +3>V/N +4>Colour +5>F/N
                        nodeAtrributeArr[i+3] = 'V'
                        nodeAtrributeArr[i+4] = RED
                    
                    print('Nodes Visible')

                #set all nodes to be invisible
                if event.key == pygame.K_n:
                    for i in range(0,len(nodeAtrributeArr),6):
                        nodeAtrributeArr[i+3] = 'N'
                        nodeAtrributeArr[i+4] = DARKGREY

                    print('Nodes Not Visible')
                    
        if nodeAttributesCreated == False and started == True:
            #Assign attributes to nodes
            nodeAtrributeArr = []
            for i in range(1,int(len(nodePos)/2)+1):
                nodeAtrributeArr.append(i) #NODE ID
                nodeAtrributeArr.append(nodePos[(i-1)*2]) #X COORD
                nodeAtrributeArr.append(nodePos[((i-1)*2)+1]) #Y COORD
                nodeAtrributeArr.append('V') #VISIBLE/NOT VISIBLE
                nodeAtrributeArr.append(RED) #COLOUR
                nodeAtrributeArr.append('N') #FOUND/NOT FOUND

            nodeAttributesCreated = True


        if agentsCreated == False:
            keydata = dbfunctions.getKeydata(key)
            settings = dbfunctions.getSettings(keydata[0][0],keydata[0][1])
            for i in range(0,nagents):
                agentarray.append(agent(screen_width,screen_height,screen,nodeAtrributeArr,generation,allNodesFound,i,nodesize,settings[0]))
            agentsCreated = True
        #Draw the Nodes on screen
        
        #Stats for loading time and creating start agent positions
        if not loaded:
            start = time.time()
            for i in range(0,len(agentarray)):
                agentarray[i].generateStartPos()
                agentarray[i].redrawagent()
                print(f'Gen {generation} Populating... ',end='')
                progressBar(i,len(agentarray))
                pygame.display.flip()
                
            loaded = True
            finish = time.time()
            time2Load = round(finish-start,3)
            os.system('cls')
            print(f'Loaded {nagents} agents in {time2Load}s')

            if generation!=1:
                started=True
                spacecount+=1

        if loaded:
            for i in range(0,len(agentarray)):
                agentarray[i].redrawagent()
        
        if initialNodeDraw:
            for i in range(0,len(nodePos),2):
                nodeRect = pygame.Surface((nodesize,nodesize))
                nodeColour = RED
                    
                nodeRect.fill(nodeColour)
                screen.blit(nodeRect,(nodePos[i]-(nodesize/2),nodePos[i+1]-(nodesize/2)))
                pygame.display.flip()
                time.sleep(0.1)
            initialNodeDraw = False
        
        elif not initialNodeDraw:
            for i in range(0,len(nodePos),2):
                nodeRect = pygame.Surface((nodesize,nodesize))
                if nodeAttributesCreated == True:
                    for k in range(0,len(nodeAtrributeArr),6):
                        #+0>NID +1>X +2>Y +3>V/N +4>Colour +5>F/N
                        if nodePos[i] == nodeAtrributeArr[k+1] and nodePos[i+1] == nodeAtrributeArr[k+2]:
                            nodeColour = nodeAtrributeArr[k+4]
                else:
                    nodeColour = RED
                    
                nodeRect.fill(nodeColour)
                screen.blit(nodeRect,(nodePos[i]-(nodesize/2),nodePos[i+1]-(nodesize/2)))



        if started == True:
            if generationResetting == False:
                for i in range(0,len(agentarray)):
                    agentarray[i].updatenodeAttributes(nodeAtrributeArr)
                    agentarray[i].move()
                    if agentarray[i].allNodesReached == True:
                        agentFinishedCount+=1
                        #print(f'ID: {agentarray[i].ID}, Path: {agentarray[i].visitedStack}')
                        agentarray[i].allNodesReached = False
                        progressBar(agentFinishedCount,nagents)
        
            nodeAtrributeArr,allNodesFound = checkNodeFound(nodeAtrributeArr,allNodesFound,agentarray,nodesize)
            
            collisionCount = 0
            for i in range(0,len(agentarray)):
                if agentarray[i].checkwallCollision() == True:
                    collisionCount+=1

            if collisionCount >= nagents*FoundAllThreshold:
                allNodesCollided=True
            
            if allNodesFound and allNodesCollided:
                if generation == 1:
                    generation+=1
                    started = False
                    spacecount+=1
                    agentarray=[]
                    screen.fill(BLACK)
                    for i in range(0,len(nodeAtrributeArr),6):
                        nodeAtrributeArr[i+5] = 'N'
                    for i in range(0,len(nodePos),2):   
                        nodeRect = pygame.Surface((nodesize,nodesize))
                        nodeRect.fill(nodeColour)
                        screen.blit(nodeRect,(nodePos[i]-(nodesize/2),nodePos[i+1]-(nodesize/2)))
                        agentsCreated = False
                        loaded = False

            if agentFinishedCount>=nagents*iterateGenerationThreshold:
                iterateGeneration = True
                
            if iterateGeneration == True:
                if finishedSim == False:
                    generation+=1
                    print(f'\ngeneration: {generation}')
                if generation>=len(nodeAtrributeArr)/6:
                    finishedSim = True
                    for i in range(len(shortestPath)):
                        if i==len(shortestPath)-1:
                           #pygame.draw.line(screen,WHITE,(shortestPath[-1][0],shortestPath[-1][1]),(shortestPath[0][0],shortestPath[0][1]))
                            draw_dashed_line(screen,WHITE,(shortestPath[-1][0],shortestPath[-1][1]),(shortestPath[0][0],shortestPath[0][1]),3,5)
                            
                        else:
                            #pygame.draw.line(screen,WHITE,(shortestPath[i][0],shortestPath[i][1]),(shortestPath[0][0],shortestPath[0][1]))
                            draw_dashed_line(screen,WHITE,(shortestPath[i][0],shortestPath[i][1]),(shortestPath[i+1][0],shortestPath[i+1][1]),3,3)
                    
                    dijkstrasPath = dijkstras(shortestPath)
                    for i in range(len(shortestPath)):
                        if i==len(shortestPath)-1:
                            #pygame.draw.line(screen,RED,(dijkstrasPath[-1][0],dijkstrasPath[-1][1]),(dijkstrasPath[0][0],dijkstrasPath[0][1]))
                            draw_dashed_line(screen,RED,(dijkstrasPath[-1][0],dijkstrasPath[-1][1]),(dijkstrasPath[0][0],dijkstrasPath[0][1]),3)
                            
                        else:
                            #pygame.draw.line(screen,RED,(dijkstrasPath[i][0],dijkstrasPath[i][1]),(dijkstrasPath[i+1][0],dijkstrasPath[i+1][1]))
                            draw_dashed_line(screen,RED,(dijkstrasPath[i][0],dijkstrasPath[i][1]),(dijkstrasPath[i+1][0],dijkstrasPath[i+1][1]),3)
                else:           
                    iterateGeneration = False
                    agentFinishedCount = 0
                    for i in range(len(agentarray)):
                        agentarray[i].generation += 1
                        shortestPath,shortestPathLength = checkPathLength(agentarray[i].visitedStack,shortestPathLength,shortestPath)
                    generationResetting = True
                    for i in range(len(agentarray)):
                        agentarray[i].shortestPath = shortestPath
                        agentarray[i].reset4NewGeneration()
                        progressBar(i+1,len(agentarray))
                        pygame.display.flip()
                        generationResetting = False

        fps(screen,round(clock.get_fps()),10,10)
        pygame.display.flip()
        clock.tick()

if __name__ == '__main__':
    gui.access()