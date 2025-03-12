import pygame,sys
pygame.init()

class globalAttributes():
    def __init__(self) -> None:
        self.zoom = 1.0


    def getZoom(self):
        return self.zoom

    def zoomOut(self):
        if self.zoom>0:
            self.zoom-=0.1

    def zoomIn(self):
        self.zoom+=0.1

class Circle():
    def __init__(self,x,y,screen,sw,sh) -> None:
        self.screen = screen
        self.x = x # relative to the centre of the screen
        self.y = y
        
        self.sw = sw
        self.sh = sh


        self.radius = 100

        self.colour = (255,255,255)

        self.scale = None

    def draw(self): 

        pygame.draw.circle(self.screen,self.colour,((self.x*self.scale)+self.sw/2,(self.y*self.scale)+self.sh/2),self.radius*self.scale)

    def setScale(self,scale2set2):
        self.scale = scale2set2


def startprogram():
    sw=2400
    sh=1200
    screen=pygame.display.set_mode((sw,sh))
    clock = pygame.time.Clock()

    attributes = globalAttributes()

    shapeArr = []
    shapeArr.append(Circle(-1,-1,screen,sw,sh))

    while True:
            
            screen.fill('black')

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                if event.type == pygame.MOUSEWHEEL:
                    if event.y>0:
                        for i in range(2):
                            attributes.zoomIn()
                            for obj in shapeArr:
                                obj.setScale(attributes.getZoom())
                                obj.draw()

                    if event.y<0:
                        for i in range(2):
                            attributes.zoomOut()
                            for obj in shapeArr:
                                obj.setScale(attributes.getZoom())
                                obj.draw()


            for obj in shapeArr:
                obj.setScale(attributes.getZoom())
                obj.draw()

            pygame.display.flip()
            clock.tick(30)
            
if __name__ == '__main__':
    startprogram()

