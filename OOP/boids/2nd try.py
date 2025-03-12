from math import sin, cos, pi, radians
import pygame,sys,random,math
pygame.init()

class boid():
    def __init__(self,screen,sw,sh,alignment) -> None:
        

        self.radius = 5
        self.alignDistance = 100

        self.alignmentScale = alignment

        self.sw = sw
        self.sh = sh

        self.screen = screen

        xvect = 0
        while xvect == 0:
            xvect = random.randint(-3,3)
        yvect = 0
        while yvect == 0:
            yvect = random.randint(-3,3)

        self.movementVector = [xvect,yvect]
        self.scale = 30
        self.makeTriangle(15,60,10)

        self.positionVector = [random.randint(10,1910),random.randint(10,1070)]

        self.move(self.positionVector[0],self.positionVector[1])
        self.draw()

    def makeTriangle(self,scale, internalAngle, rotation):
        #define the points in a uint space

        ra = math.atan(self.movementVector[1]/self.movementVector[0])
        ra = math.degrees(ra)
        if self.movementVector[0]>=0 and self.movementVector[1]>=0:
            ra+=90

        elif self.movementVector[0]<0 and self.movementVector[1]>=0:
            ra+=270

        elif self.movementVector[0]<0 and self.movementVector[1]<0:
            ra+=270

        elif self.movementVector[0]>=0 and self.movementVector[1]<0:
            ra+=90

        ia = (radians(internalAngle) * 2) - 1
        p1 = (0, -1)
        p2 = (cos(ia), sin(ia))
        p3 = (cos(ia) * -1, sin(ia))

        #rotate the points
        ra=math.radians(ra)
        rp1x = p1[0] * cos(ra) - p1[1] * sin(ra)
        rp1y = p1[0] * sin(ra) + p1[1] * cos(ra)                 
        rp2x = p2[0] * cos(ra) - p2[1] * sin(ra)
        rp2y = p2[0] * sin(ra) + p2[1] * cos(ra)                        
        rp3x = p3[0] * cos(ra) - p3[1] * sin(ra)                         
        rp3y = p3[0] * sin(ra) + p3[1] * cos(ra)
        rp1 = ( rp1x, rp1y )
        rp2 = ( rp2x, rp2y )
        rp3 = ( rp3x, rp3y )

        #scale the points 
        sp1 = [rp1[0] * scale, rp1[1] * scale]
        sp2 = [rp2[0] * scale, rp2[1] * scale]
        sp3 = [rp3[0] * scale, rp3[1] * scale]
                        
        self.triangle = Triangle(sp1, sp2, sp3)

    def draw(self): 
        pygame.draw.line(self.screen, 'WHITE', self.triangle.p2, self.triangle.p3,2)
        pygame.draw.line(self.screen, 'WHITE', self.triangle.p1, self.triangle.p2,2)
        pygame.draw.line(self.screen, 'WHITE', self.triangle.p3, self.triangle.p1,2)

        pygame.draw.line(self.screen,'RED',self.triangle.p1,(self.triangle.p1[0]+15*self.movementVector[0],self.triangle.p1[1]+15*self.movementVector[1]))

    def move(self,*args):

        if len(args) != 0:
            xoffset = args[0]
            yoffset = args[1]
        else:
            xoffset = self.movementVector[0]
            yoffset = self.movementVector[1]

        self.positionVector = [a+b for a,b in zip(self.positionVector,[xoffset,yoffset])]
        

        self.triangle.p1[0] += xoffset
        self.triangle.p1[1] += yoffset
        self.triangle.p2[0] += xoffset
        self.triangle.p2[1] += yoffset
        self.triangle.p3[0] += xoffset
        self.triangle.p3[1] += yoffset


        if self.triangle.p1[0]>self.sw:
            self.triangle.p1[0]-=self.sw
            self.triangle.p2[0]-=self.sw
            self.triangle.p3[0]-=self.sw
        
        elif self.triangle.p1[0]<0:
            self.triangle.p1[0]+=self.sw
            self.triangle.p2[0]+=self.sw
            self.triangle.p3[0]+=self.sw
        
        if self.triangle.p1[1]>self.sh:
            self.triangle.p1[1]-=self.sh
            self.triangle.p2[1]-=self.sh
            self.triangle.p3[1]-=self.sh
        
        elif self.triangle.p1[1]<0:
            self.triangle.p1[1]+=self.sh
            self.triangle.p2[1]+=self.sh
            self.triangle.p3[1]+=self.sh
 
    def align(self,flockArr):
        avgVect = [0,0]
        nBoids = 0
        for item in flockArr:
            distance = self.getDistance(item.positionVector)
            if distance<=self.alignDistance:
                nBoids+=1
                avgVect = [a+b for a,b in zip(avgVect,([c-d for c,d in zip(item.movementVector,self.movementVector)]))] 

        self.movementVector = [a+b for a,b in zip(self.movementVector,list(map(lambda x:x*self.alignmentScale,list(map(lambda x:x/nBoids,avgVect)))))]

    def getDistance(self,target):
        return math.sqrt((target[0] - self.positionVector[0])**2 + (target[1] - self.positionVector[1])**2)

class Triangle():
    def __init__(self, p1, p2, p3):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

class flock():
    def __init__(self,screen,sw,sh) -> None:
        flockSize = 100

        self.screen = screen
        self.sw = sw
        self.sh = sh

        self.alignment = 0.2

        self.flockArr = []
        for i in range(flockSize):
            self.flockArr.append(boid(self.screen,self.sw,sh,self.alignment))

    def updateFlock(self):
        for boiditem in self.flockArr:

            boiditem.align(self.flockArr)

            boiditem.move() 
            boiditem.draw()


def startprogram():
    sw=1200
    sh=800
    screen=pygame.display.set_mode((sw,sh))
    clock = pygame.time.Clock()

    flock1 = flock(screen,sw,sh)

    while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                    if event.key == pygame.K_UP:
                        if flock1.alignment<1:
                            flock1.alignment+=0.05
                            print(flock1.alignment) 

                    if event.key == pygame.K_DOWN:
                        if flock1.alignment>0:
                            flock1.alignment -= 0.05
                            print(flock1.alignment)
            screen.fill('BLACK')
            flock1.updateFlock()
            pygame.display.flip()
            clock.tick(60)
            
if __name__ == '__main__':
    startprogram()