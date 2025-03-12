import pygame,sys,math
pygame.init()

GRAY = 75,75,75
WHITE = 255,255,255

def drawLine(nodePoints,screen,sw,sh):
    thickness = 10
    
    maxdist = round(math.sqrt((sw**2)+(sh**2)),0)
    
    for i in range(len(nodePoints)):
        for j in range(len(nodePoints)):
            
            xdif = nodePoints[i][0]-nodePoints[j][0]
            ydif = nodePoints[i][1]-nodePoints[j][1]
            totaldif = round(math.sqrt((xdif**2)+(ydif**2)),0)
            scale = totaldif/maxdist
            multiplier = 1-scale
            
            R = 0
            G = 0
            B = 0
            opacity = 150*multiplier

            surface = pygame.Surface((sw,sh), pygame.SRCALPHA)
            pygame.draw.line(surface, (R,G,B,opacity),(nodePoints[i][0],nodePoints[i][1]), (nodePoints[j][0],nodePoints[j][1]), thickness)
            screen.blit(surface, (0,0))

def drawPoint(pos,screen):
    size = 25
    dot = pygame.Rect(pos[0]-(size/2),pos[1]-(size/2),size,size)
    pygame.draw.ellipse(screen,(GRAY),dot)

def startprogram():
    sw=2400
    sh=1200
    screen=pygame.display.set_mode((sw,sh))
    clock = pygame.time.Clock()
    
    nodePoints = []
    
    while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                        
                    if event.key == pygame.K_SPACE:
                        started = True
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    center = pygame.mouse.get_pos()
                    temparr = []
                    temparr.append(center[0])
                    temparr.append(center[1])
                    nodePoints.append(temparr)
                        
            screen.fill(WHITE)
            for i in range(len(nodePoints)):
                drawPoint(nodePoints[i],screen)
            
            drawLine(nodePoints,screen,sw,sh)
                        
            pygame.display.flip()
            clock.tick()
            
if __name__ == '__main__':
    startprogram()