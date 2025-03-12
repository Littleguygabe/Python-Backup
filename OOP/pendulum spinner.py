import pygame,sys,math,random
pygame.init()

class pendulum():
    def __init__(self,screen,rotation,opacity,ID,maxID):
        self.screen = screen
        self.colour = (255,255,255)
        self.opacity = opacity
        self.x = 0
        self.y = 0
        self.ID = ID
        self.maxID = maxID

        self.centerX = 750
        self.centerY = 500

        self.PendRadius = 1500

        self.rotation = rotation


        self.calculateXY()
        self.drawLine()

    def drawCircle(self):
        circle_surface = pygame.Surface((80, 80), pygame.SRCALPHA)
        pygame.draw.circle(circle_surface, (255, 255, 255, self.opacity), (50, 50), 5)  # (R, G, B, Alpha) 
        self.screen.blit(circle_surface,(self.edgex-50,self.edgey-50))
    
    def calculateXY(self):
        #circle
        #self.edgex = self.PendRadius*math.cos(math.radians(self.rotation))+self.centerX
        #self.edgey = self.PendRadius*math.sin(math.radians(self.rotation))+self.centerY

        #figure 8 
        self.edgex = self.centerX-self.PendRadius/2+(self.PendRadius/self.maxID)*self.ID
        self.edgey=self.centerY+50*math.sin(math.radians(1*0.96*self.edgex))
    


    def drawLine(self):
        pygame.draw.line(self.screen,(255,255,255),(self.centerX,self.centerY),(self.edgex-2,self.edgey-2))

def startProgram():
    count=0
    sw=1500
    sh=1000
    screen=pygame.display.set_mode((sw,sh))
    clock = pygame.time.Clock()

    nPendulums = 1500
    penArr = []
    for i in range(nPendulums):
        penArr.append(pendulum(screen,(360/nPendulums)*i-1,(255/nPendulums)*i,i,nPendulums-1))


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.QUIT()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.QUIT
                    sys.exit()
        screen.fill((0,0,0))
        for i in range(len(penArr)):
            if count>=nPendulums:
                count=-1
            else:
                count+=1
            obj = penArr[i]
            obj.opacity = abs((count%nPendulums)*(255/nPendulums))
            obj.drawCircle()
            #obj.drawLine()
            

        pygame.display.flip()
        clock.tick(144)

if __name__ == '__main__':
    startProgram()