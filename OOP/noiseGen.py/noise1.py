import pygame,sys,random,math
from pygame import gfxdraw
pygame.init()

GRAY = (75,75,75)
WHITE=(255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)

class vector():
    def __init__(self,x,y,screen):
        self.x = x
        self.y = y
        self.angle = random.randint(0,360) #degrees
        self.angle = self.angle*(math.pi/180) #into radians
        self.screen = screen
        
        self.increment = 5 #in degrees
        self.increment = self.increment*(math.pi/180) #into radians
        
        self.vectorLength = 30
        
        self.vectorx = None
        self.vectory = None
        
        self.vectorXoppo = None
        self.vectorYoppo = None
        
        self.colorInfluence = 60
        self.PcolourIntensity = 100 #255 is solid, 0 is transparent
        self.NcolourIntesity = 50
        
        
    def rotate(self):
        self.vectorx = self.vectorLength*math.cos(self.angle)+self.x
        self.vectory = self.vectorLength*math.sin(self.angle)+self.y
        
        self.vectorXoppo = self.vectorLength*math.cos(self.angle-math.pi)+self.x
        self.vectorYoppo = self.vectorLength*math.sin(self.angle-math.pi)+self.y
         
        self.angle+=self.increment   
        
    def draw(self):
           pygame.draw.line(self.screen,WHITE,(self.x,self.y),(self.vectorx,self.vectory),2)
           self.colourPoint()
           
    def colourPoint(self):
        
        for i in range(0,self.colorInfluence,5):
            gfxdraw.filled_circle(self.screen,int(self.vectorx),int(self.vectory),i,(255,255,255,self.PcolourIntensity))
            
            gfxdraw.filled_circle(self.screen,int(self.vectorXoppo),int(self.vectorYoppo),i,(255,0,0,self.NcolourIntesity))    
                

def startprogram():
    sw=2400
    sh=1200
    screen=pygame.display.set_mode((sw,sh))
    clock = pygame.time.Clock()
    vectorArr = []
    
    GAP = 100
    
    for x in range(GAP,sw,GAP):
        for y in range(GAP,sh,GAP):
            vectorArr.append(vector(x,y,screen))
    
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
            
            for i in range(len(vectorArr)):
                vectorArr[i].rotate()
                #vectorArr[i].draw()
                vectorArr[i].colourPoint()
            
            pygame.display.flip()
            clock.tick()
            
            
            
if __name__ == '__main__':
    startprogram()