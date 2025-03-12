#TO-DO LIST:
#[]FIX CHANGING BACKGROUND COLOUR
#[]FIND SHORTEST PATH
#[]COMPARE NEW COLLISION WITH SHORTEST PATH
#[]SAVE AGENT POSITIONS

import pygame, random, sys, math, databasecontrol, userinterface
pygame.init()

GREEN = 50,255,0
WHITE = 255,255,255
BLACK = 0,0,0
RED = 255,0,0
LIGHTBLUE = 5,125,245
      
class agent():
    def __init__(self,screen,sw,sh,taillength,colour,gameid,positionsneeded,angleRetrieved):
        self.gameid = gameid
        self.colour = colour
        self.agentSize = 3
        self.screen = screen
        self.sw = sw
        self.sh = sh
        self.started = False
        self.agentArray = []
        self.interval = round(self.agentSize/3)
        self.spawnradius = 50
        self.angle = 0
        self.xmultiplier=1
        self.ymultiplier=1
        self.deflected = False
        self.fpx = self.sw/2
        self.fpy = self.sh/2
        self.anglecalculated = angleRetrieved
        self.nodefound = False
        self.taillength = taillength
        self.wallbuffer = 10
        self.minangle = 10
        self.startgenerationneeded = positionsneeded

        self.agentpath = []

        if self.started == False and self.startgenerationneeded == True:
            self.generateStartPositions()

        if self.started == True:
            self.updatePositions()

    def generateStartPositions(self):

        self.xpos = random.randint(round(self.sw/2)-self.spawnradius,round(self.sw/2)+self.spawnradius)
        self.ypos = random.randint(round(self.sh/2)-self.spawnradius,round(self.sh/2)+self.spawnradius) 
        while self.xpos>(self.sw/2)-10 and self.xpos<(self.sw/2)+10 and self.ypos>(self.sh/2)-10 and self.ypos<(self.sh/2)+10:
            self.xpos = random.randint(round(self.sw/2)-self.spawnradius,round(self.sw/2)+self.spawnradius)
            self.ypos = random.randint(round(self.sh/2)-self.spawnradius,round(self.sh/2)+self.spawnradius)

        
        self.agentArray.append(self.xpos)
        self.agentArray.append(self.ypos)

        self.agentpath.append(self.xpos)
        self.agentpath.append(self.ypos)

        self.redrawAgents()
        self.started = True

    def updatePositions(self):
        if len(self.agentArray)>self.taillength*2:
            self.agent=pygame.Rect(self.agentArray[0],self.agentArray[1],self.agentSize,self.agentSize)
            pygame.draw.rect(self.screen,(0,0,0),self.agent)

            for i in range(0,2):
                del self.agentArray[0]

        #calculate incentive 
        if self.nodefound == False:
            if self.anglecalculated == False:
                self.xincentive = self.interval

                self.fpx = self.sw/2
                self.fpy = self.sh/2

                #calculate current angle from center
                xdif = self.xpos - (self.fpx)
                ydif = self.ypos - (self.fpy)

                if xdif!=0 and ydif!=0:
                    self.angle = math.atan(xdif/ydif)
                    self.yincentive = self.xincentive/(math.tan(self.angle))
                    self.anglecalculated = True

                    if self.xpos<self.sw/2:
                        self.xincentive *=-1
                        self.yincentive *=-1

                else:
                    self.xincentive = 0
                    self.yincentive = 0

        #deflect off of walls
        #upper wall
        if self.ypos<=self.wallbuffer:
            #deflection from heading right-up to right-down
            if self.angle<0 and self.yincentive<=0 and self.xincentive>=0:
                self.angle*=-1
                self.yincentive*=-1
            
            #deflection from heading left-up to left-down
            if self.angle>0 and self.yincentive<=0 and self.xincentive<=0:
                self.angle*=-1
                self.yincentive*=-1

        #lower wall
        if self.ypos>=self.sh-self.wallbuffer:
            #deflection from heading right-down to right-up
            if self.angle>0 and self.yincentive>=0 and self.xincentive>=0:
                self.angle*=-1
                self.yincentive*=-1

            #deflection from heading left-down to left-up
            if self.angle<0 and self.yincentive>=0 and self.xincentive<=0:
                self.angle*=-1
                self.yincentive*=-1
        
        #left wall
        if self.xpos<=self.wallbuffer:
            #deflection from heading left-up to right-up
            if self.angle>0 and self.yincentive<=0 and self.xincentive<=0:
                self.angle*=-1
                self.xincentive*=-1

            #deflection heading from left-down to right-down
            if self.angle<0 and self.yincentive>=0 and self.xincentive<=0:
                self.angle*=-1
                self.xincentive*=-1

        #right wall
        if self.xpos>=self.sw-self.wallbuffer:
            #deflection from heading right-up to left-up
            if self.angle<0 and self.yincentive<=0 and self.xincentive>=0:
                self.angle*=-1
                self.xincentive*=-1
            
            #deflection from heading right-down to left-down
            if self.angle>0 and self.yincentive>=0 and self.xincentive>=0:
                self.angle*=-1
                self.xincentive*=-1

        if self.deflected == False:
            if math.degrees(self.angle)>-self.minangle and math.degrees(self.angle)<self.minangle:
                self.yincentive = 0

        #deflect off of center
        
        self.xincentive*=self.xmultiplier
        self.yincentive*=self.ymultiplier
        
        movx = random.randint(self.interval*-1,self.interval)
        while self.xpos+movx<0 or self.xpos+movx>self.sw:
            movx = random.randint(self.interval*-1,self.interval)

        movy = random.randint(self.interval*-1,self.interval)
        while self.ypos+movy<0 or self.ypos+movy>self.sh:
            movy = random.randint(self.interval*-1,self.interval)

        self.xpos+=(movx+self.xincentive)
        self.ypos+=(movy+self.yincentive)
        self.agentArray.append(self.xpos)
        self.agentArray.append(self.ypos)
        self.agentpath.append(self.xpos)
        self.agentpath.append(self.ypos)

        self.redrawAgents()

    def redrawAgents(self):
        #agent head colour
        for i in range(0,len(self.agentArray),2):
            agentRect = pygame.Surface((self.agentSize,self.agentSize))
            agentRect.fill(self.colour)
            agentRect.set_alpha(150)
            self.screen.blit(agentRect,(self.agentArray[i],self.agentArray[i+1]))

        #change the colour down the agent tail
        """ for i in range(0,len(self.agentArray),2):
            agentRect = pygame.Surface((self.agentSize,self.agentSize))
            alphaval = 255-(255/(len(self.agentArray)/(i+1)))
            agentRect.set_alpha(alphaval)
            agentRect.fill((0,0,0))
            self.screen.blit(agentRect,(self.agentArray[i],self.agentArray[i+1])) """
        
    def checknodecollision(self,nodearray,nodesize):
        pathlength=0
        for i in range(0,len(nodearray)):
            if self.agentArray[-2]>=nodearray[i][0] and self.agentArray[-2]<=nodearray[i][0]+(nodesize) and self.agentArray[-1]>=nodearray[i][1] and self.agentArray[-1]<=nodearray[i][1]+(nodesize):
                #get current shortest path from data base
                #print(f'collided with nodeID {i+1} at position {nodearray[i][0]},{nodearray[i][1]}')
                checkIfShortest(self.agentpath,self.gameid,i+1)
                print('collided')
       
def placeNode(nodeArray,nodesize):
    center = pygame.mouse.get_pos()
    coords = []
    centerx = center[0]-(nodesize/2)
    centery = center[1] - (nodesize/2)
    coords.append(centerx)
    coords.append(centery)
    nodeArray.append(coords)

    return nodeArray

def checkIfShortest(agentpath,gameid,nodeid):
    totaldist = 0
    for i in range(0,len(agentpath)-2,2):
        xdif = agentpath[i]-agentpath[i+2]
        ydif = agentpath[i+1]-agentpath[i+3]
        distancebetween = math.sqrt((xdif**2)+(ydif**2))
        totaldist+=distancebetween

    shortestpath = databasecontrol.getShortestValues(gameid,nodeid)
    totaldist = round(totaldist,2)
    if totaldist<shortestpath:
        databasecontrol.updateshortestpath(totaldist,gameid,nodeid)

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
        blankrect = pygame.Surface((100,self.fontsize))
        blankrect.fill((BLACK))
        self.screen.blit(blankrect,(self.x,self.y))
        fpstext = self.font.render(str(self.fps),1,GREEN)
        self.screen.blit(fpstext,(self.x,self.y))

def startsimulation():
    start = False
    spacecount = 1
    nodeid = 0

    classArray = []
    nodeArray = []

    nodesize = 10

    DBexists = databasecontrol.DoesDBExist()
    if DBexists:
        choice = input('Do You Want to Create a New Simulation?(Y/N) ')
        if choice.upper() == 'N':
            gameid = int(input('Enter The Game ID: '))
            nodeArray = databasecontrol.GetPastGame(gameid)
            nagents,taillen,unlimitfpsoption,fpslimit,displayfpsoption = databasecontrol.getparamaters(gameid)
        else:
            gameid = databasecontrol.creategameID()
            print(f'Your GameID is: {gameid}')
            userinterface.interface(gameid)
            nagents,taillen,unlimitfpsoption,fpslimit,displayfpsoption = databasecontrol.getparamaters(gameid)
        
    else:
        databasecontrol.createtable()
        gameid = databasecontrol.creategameID()
        print(f'Your GameID is: {gameid}')
        userinterface.interface(gameid)
        nagents,taillen,unlimitfpsoption,fpslimit,displayfpsoption = databasecontrol.getparamaters(gameid)
        choice = 'Y'

    screen_width = 1600
    screen_height = 900
    screen = pygame.display.set_mode((screen_width,screen_height))

    nodeHex = databasecontrol.getDBcolour(1)
    BGhex = databasecontrol.getDBcolour(2)
    agenthex = databasecontrol.getDBcolour(3)

    

    pygame.display.set_caption('Slime Mold Simulation')
    clock = pygame.time.Clock()
    print('simulation starting')


    if choice.upper() == 'Y':
        startposNeeded = True
        angleRetrieved = False
        
    elif choice.upper() == 'N':
        startposNeeded = False
        angleRetrieved = True

    for i in range(0,nagents):
        classArray.append(agent(screen,screen_width,screen_height,taillen,agenthex,gameid,startposNeeded,angleRetrieved))

    if choice.upper() == 'N':
        coordinates = databasecontrol.getagentpositions(gameid)
        print(len(coordinates))
        for i in range(0,len(classArray)-1):
            classArray[i].xpos = coordinates[i][0]
            classArray[i].ypos = coordinates[i][1]
            print(classArray[i].xpos,classArray[i].ypos)        

    center_spot = pygame.Rect(screen_width/2,screen_height/2,5,5)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                databasecontrol.insertNodePositions(classArray,gameid)
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONUP and start == False:
                nodeArray = placeNode(nodeArray,nodesize)

                #update the database with node id
                nodeid=len(nodeArray)
                center = pygame.mouse.get_pos()
                centerx = center[0]-(nodesize/2)
                centery = center[1] - (nodesize/2)
                databasecontrol.updatenoderegisters(nodeid,100000,'[]',gameid,centerx,centery)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    databasecontrol.insertNodePositions(classArray,gameid)
                    pygame.quit()
                    sys.exit()

                if event.key == pygame.K_SPACE:
                    spacecount+=1
                    if spacecount%2 == 0:
                        start=True

                    else:
                        start=False
        pygame.draw.ellipse(screen,(databasecontrol.getDBcolour(1)),center_spot)
        if start == True:
            for i in range(0,len(classArray)):
                classArray[i].updatePositions()
                shortestpath = classArray[i].checknodecollision(nodeArray,nodesize)  

        for i in range(0,len(nodeArray)):
            node = pygame.Rect(nodeArray[i][0],nodeArray[i][1],nodesize,nodesize)
            
            pygame.draw.rect(screen,(nodeHex),node)

        pygame.display.flip()
        if unlimitfpsoption == 1:
            clock.tick()
        else:
            clock.tick(fpslimit)

        #display fps
        if displayfpsoption == 1:
            fps(screen,round(clock.get_fps()),10,10)

if __name__ == '__main__':
    startsimulation()