import pygame,sys,math
pygame.init()

WHITE = (255,255,255)
BLACK = (0,0,0)

class objects():
    def __init__(self,screen) -> None:
        self.screen = screen
        
    def drawCircle(self,x,y,radius):
        pygame.draw.circle(self.screen,WHITE,(x,y),radius,width=1)
        
    def drawLine(self,startPos,endPos):
        pygame.draw.line(self.screen,WHITE,startPos,endPos)
        
class point():
    def __init__(self,screen,radius,angle,cx,cy,identity) -> None:
        self.Rangle = angle
        self.x = None
        self.y = None
        self.drawRadius = radius
        self.screen = screen
        self.cx = cx
        self.cy = cy
        
        self.id = identity
        
        self.calculatePosition()
        
    def draw(self):
        pygame.draw.circle(self.screen,WHITE,(self.x,self.y),3)
        
    def calculatePosition(self):
        self.x = self.drawRadius*math.cos(self.Rangle)+self.cx
        self.y = self.drawRadius*math.sin(self.Rangle)+self.cy            

def f(x):
    k = 1
    y = math.tan(x*k)-(k**math.pi)
    return round(y)

def getPosition(pointID,dots):
    print(pointID)
    return (dots[pointID].x,dots[pointID].y)

def startprogram():
    sw= 1800
    sh = 900
    screen=pygame.display.set_mode((sw,sh))
    clock = pygame.time.Clock()
    
    mainCircleRadius = 425
    cx=sw/2
    cy=sh/2
    
    shapes = objects(screen)
    
    
    nDivisions = 50
    
    while True:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
        
        screen.fill(BLACK)
        
        shapes.drawCircle(cx,cy,mainCircleRadius)
        
        dots = []
    
        for i in range(nDivisions):        
            dots.append(point(screen,mainCircleRadius,((int(360/nDivisions))*i)*(math.pi/180),cx,cy,i))
        
        for x in range(nDivisions):
            y = f(x)
            
            if y<0:
                y*=-1
                while y>=nDivisions:
                    y=y%nDivisions
            else:
                while y>=nDivisions:
                    y=y%nDivisions
            
            xpos = getPosition(x,dots)
            ypos = getPosition(y,dots)
            shapes.drawLine(xpos,ypos)

        if nDivisions<=300:
            nDivisions+=1
            
        print(nDivisions)
        pygame.display.flip()
        clock.tick(30)

if __name__ == '__main__':
    startprogram()