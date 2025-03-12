import numpy as np
import pygame,sys,random,time

pygame.init()

BLACK = 0,0,0
GREEN = 0,255,0

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
        blankrect = pygame.Surface((35,self.fontsize))
        blankrect.fill((BLACK))
        self.screen.blit(blankrect,(self.x,self.y))
        fpstext = self.font.render(str(self.fps),1,GREEN)
        self.screen.blit(fpstext,(self.x,self.y))

class agent():
    def __init__(self,screen,sw,sh):
        self.screen = screen
        self.sw = sw
        self.sh = sh
        self.bufferSize = 300
        self.agentSize = 3
        self.incentiveControl = 3
        self.path = []
        self.random = round(self.agentSize/2)
        self.xincentive=0
        self.yincentive=0
        self.maxPheremoneStrength = 20
        self.pheremoneReach = 10
        self.clump = True
        self.viewDistance = 10
        self.taillength = 2

        self.generatestartPositions()
        
    def generatestartPositions(self):
        self.x = random.randint(self.bufferSize,self.sw-self.bufferSize)
        self.y = random.randint(self.bufferSize,self.sh-self.bufferSize)
        self.redrawAgents()

    def redrawAgents(self):
        agentRect = pygame.Surface((self.agentSize,self.agentSize))
        agentRect.fill((255,255,255))
        agentRect.set_alpha(200)
        self.screen.blit(agentRect,(self.x,self.y))

    def updatePosition(self,pheremoneArray):
        self.path.append(self.x)
        self.path.append(self.y)

        movx = random.randint(self.random*-1,self.random)
        while self.x+movx<0 or self.x+movx>self.sw:
            movx = random.randint(self.random*-1,self.random)

        movy = random.randint(self.random*-1,self.random)
        while self.y+movy<0 or self.y+movy>self.sh:
            movy = random.randint(self.random*-1,self.random)

        if len(self.path)>self.taillength*2:
            self.agent=pygame.Rect(self.path[0],self.path[1],self.agentSize,self.agentSize)
            pygame.draw.rect(self.screen,(0,0,0),self.agent)
            for i in range(0,2):
                del self.path[0]

        #get strongest nearby pheremone
        if self.clump == True:
            nearbyPhValues = np.zeros((self.viewDistance*2+1)**2)
            nearbyPhValues.shape = (self.viewDistance*2+1,self.viewDistance*2+1)

            for y in range(self.viewDistance*-1,self.viewDistance+1):
                for x in range(self.viewDistance*-1,self.viewDistance+1):
                    nearbyPhValues[y+self.viewDistance,x+self.viewDistance] = round(pheremoneArray[self.y+y,self.x+x],3)
            
            MaxList = np.where(nearbyPhValues == nearbyPhValues.max())
            if len(MaxList[0])>1:
                self.xincentive = 0
                self.yincentive = 0

            elif len(MaxList[0]) == 1:
                maxXcoord = MaxList[0][0]
                maxYcoord = MaxList[1][0]
                #CALCULATE INCENTIVES

                if maxXcoord>self.x:
                    self.xincentive = self.incentiveControl

                elif maxXcoord<self.x:
                    self.xincentive = self.incentiveControl*-1

                else:
                    self.xincentive = 0

                if maxYcoord>self.y:
                    self.yincentive = self.incentiveControl

                elif maxYcoord<self.y:
                    self.yincentive = self.incentiveControl*-1

                else:
                    self.xincentive = 0

        self.x+=movx+self.xincentive
        self.y+=movy+self.yincentive

        self.redrawAgents()                      

def deletepheremones(pheremoneArray,obj):
    pheremoneStrength = obj.maxPheremoneStrength
    phReach = obj.pheremoneReach
    path = obj.path

    phValues = np.zeros(phReach)
    phValues.fill(pheremoneStrength)
    #setup Pheremone Values Array
    tempcounter = len(phValues)
    for i in range(0,len(phValues)):
        phValues[i] = round(pheremoneStrength/tempcounter,1)
        tempcounter-=1

    #Delete Old Values
    for i in range(0,len(path),2):
        pos = int(i/2)
        pheremoneArray[path[i+1]-1,path[i]-1] -= phValues[pos]#Y,X
        

    return pheremoneArray
    
def addpheremones(pheremoneArray,obj):
    #setup Pheremone Values Array
    pheremoneStrength = obj.maxPheremoneStrength
    phReach = obj.pheremoneReach
    path = obj.path

    phValues = np.zeros(phReach)
    phValues.fill(pheremoneStrength)
    tempcounter = len(phValues)
    for i in range(0,len(phValues)):
        phValues[i] = round(pheremoneStrength/tempcounter,1)
        tempcounter-=1

    for i in range(0,len(path),2):
        pos=int(i/2)
        pheremoneArray[path[i+1]-1,path[i]-1] += phValues[pos]#Y,X
    return pheremoneArray

def startsimulation():
    print('Sim Starting')

    nagents = 100
    agentArray = []
    start = False
    spacecount = 1

    screen_width = 1000
    screen_height = 1000
    screen = pygame.display.set_mode((screen_width,screen_height))
    clock = pygame.time.Clock()
    
    pheremoneArray = np.zeros(screen_width*screen_height)
    pheremoneArray.shape = (screen_height,screen_width)
    for i in range(0,nagents):
        agentArray.append(agent(screen,screen_width,screen_height))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    spacecount+=1
                    if spacecount%2 == 0:
                        start=True

                    else:
                        start=False

        fps(screen,round(clock.get_fps()),10,10)

        if start == True:
            for i in range(0,len(agentArray)):
                obj = agentArray[i]
                obj.updatePosition(pheremoneArray)
                pheremoneArray=deletepheremones(pheremoneArray,obj)
                pheremoneArray=addpheremones(pheremoneArray,obj)
        
        pygame.display.flip()
        clock.tick()
if __name__ == '__main__':
    startsimulation()