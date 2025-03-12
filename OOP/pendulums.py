import pygame, sys, math
pygame.init()

RED = (255,0,0)
BLACK = (0,0,0)
GRAY = (75,75,75)
WHITE = (255,255,255)

class pendulum():
    def __init__(self,speedRatio,screen,sw,sh):
        self.rotationInt = 2
        self.rotation = 0
        baseSpeed = 0.1
        self.screen = screen
        
        self.ox = 0
        self.oy = 0
        
        self.cx = sw/2
        self.cy = sh/2
        
        self.drawTrail = False
        self.trail = []
        
        speedRatio = int(speedRatio)
        
        self.length = 100*(speedRatio/4)
        
        if speedRatio <= 0:
            self.speed = int(baseSpeed)
            
        else:
            self.speed = int(baseSpeed*speedRatio)
        
    def drawDot(self,x,y):
        dot = pygame.Rect(x-2,y-2,4,4)
        pygame.draw.ellipse(self.screen,RED,dot)
        
    def drawLine(self):
        pygame.draw.line(self.screen,GRAY,(self.cx,self.cy),(self.ox-2,self.oy-2))
        
        
        
    def rotate(self):
        for i in range(self.speed):
            self.rotation += self.rotationInt
            self.ox,self.oy = self.calculateCoords()
            self.drawDot(self.ox,self.oy)
            if self.drawTrail == True:
                temparr = []
                temparr.append(self.ox)
                temparr.append(self.oy)
                self.trail.append(temparr)
                
        
        self.drawLine()
        
        if self.drawTrail == True:            
            for points in self.trail:
                self.drawDot(points[0],points[1])
            
    def calculateCoords(self):
        x = self.length*math.cos(math.radians(self.rotation))+self.cx
        y = self.length*math.sin(math.radians(self.rotation))+self.cy
        
        return x,y
        
def getRatios():
    ratios = []
    ratioInp = str(input('Enter ratios: '))
    
    p1 = 0
    p2 = 0
    
    while p2<len(ratioInp):
        if ratioInp[p2] == ' ':
            ratios.append(ratioInp[p1:p2])
            p1 = p2+1
        p2+=1
        
    ratios.append(ratioInp[p1:])
    return ratios 

def startProgram():
    sw = 1800
    sh = 900    
    
    ratios = getRatios()
    
    screen = pygame.display.set_mode((sw,sh))
    clock = pygame.time.Clock()

    pendulumArr = []
    for ratio in ratios:
        pendulumArr.append(pendulum(ratio,screen,sw,sh))
        
    pendulumArr[-1].drawTrail = True
    
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
                    
        for i in range(len(pendulumArr)):
            if i>0:
                
                pendulumArr[i].cx = int(pendulumArr[i-1].ox)
                pendulumArr[i].cy = int(pendulumArr[i-1].oy)
                
            pendulumArr[i].rotate()
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    startProgram()