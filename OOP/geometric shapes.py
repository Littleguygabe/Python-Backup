import pygame, sys, random, math
pygame.init()

WHITE = (255,255,255)
GRAY = (75,75,75)

class point():
    def __init__(self,sw,sh,screen):
        self.sw = sw
        self.sh = sh
        self.x = random.randint(0,sw)
        self.y = random.randint(0,sh)
        self.screen = screen
        self.size = 10
        
        self.colour = GRAY
        
        self.movementInterval=4
        
        self.xstep = random.randint(1,self.movementInterval)
        self.ystep = random.randint(1,self.movementInterval)
        
        arr = [-1,1]
        self.xmult = arr[random.randint(0,1)]
        self.ymult = arr[random.randint(0,1)]
        
        self.nConnections = 5
        
    def drawPoint(self):
        dot = pygame.Rect(self.x-(self.size/2),self.y-(self.size/2),self.size,self.size)
        pygame.draw.ellipse(self.screen,self.colour,dot)
        
    def move(self):
        if self.y-self.size/2<=0:
            self.ymult = 1
            
        elif self.y+self.size/2>=self.sh:
            self.ymult=-1
            
        if self.x-self.size/2<=0:
            self.xmult=1
            
        elif self.x+self.size/2>=self.sw:
            self.xmult=-1
        
        self.x+=self.xmult*self.xstep
        self.y+=self.ymult*self.ystep
        
    def createConnections(self,posArr):
        positions = {}
        for i in range(0,len(posArr)):
            xdif = self.x-posArr[i][0]
            ydif = self.y - posArr[i][1]
            if xdif != 0 and ydif != 0:
                totaldif = round(math.sqrt((xdif**2)+(ydif**2)),0)
                positions[totaldif] = (posArr[i][0],posArr[i][1])
                
        sortedPositions = sorted(positions)
        self.closest = []
        for i in range(0,self.nConnections):
            self.closest.append(positions[sortedPositions[i]])
            
            
    def drawConnections(self):
        for i in range(len(self.closest)):
            pygame.draw.line(self.screen,self.colour,(self.x,self.y),(self.closest[i][0],self.closest[i][1]))

def startprogram():
    sw=1800
    sh=900
    screen=pygame.display.set_mode((sw,sh))
    clock = pygame.time.Clock()
    
    nPoints = 100
    
    pointArray = []
    for i in range(nPoints):
        pointArray.append(point(sw,sh,screen))
    
    while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            screen.fill(WHITE)
            
            posArr = []
            for i in range(len(pointArray)):
                temparr = []
                temparr.append(pointArray[i].x)
                temparr.append(pointArray[i].y)
                posArr.append(temparr)
            
            for i in range(len(pointArray)):
                pointArray[i].move()
                pointArray[i].drawPoint()
                pointArray[i].createConnections(posArr)
                pointArray[i].drawConnections()
            
            pygame.display.flip()
            clock.tick(30)
        
if __name__ == '__main__':
    startprogram()