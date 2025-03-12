import pygame, sys,math,time
pygame.init()

WHITE = (255,255,255)

def calculateCircleCoords(cx,cy,rotation):
    rotation = rotation*(math.pi/180)
    radius = 250
    x1 = radius*math.cos(rotation)+cx
    y1 = radius*math.sin(rotation)+cy
    
    return(x1,y1)

def shiftColour(colour,count,maxval,minval,step):
    interval = (maxval-minval)*6/round(360/step)
    r,g,b = colour
    if (count%6)+1 == 1:
        g+=interval
        if g>=maxval:
            count+=1
            
    elif (count%6)+1 == 2:
        r-=interval
        if r<=minval:
            count+=1
            
    elif (count%6)+1 == 3:
        b+=interval
        if b>=maxval:
            count+=1
            
    elif (count%6)+1 == 4:
        g-=interval
        if g <= minval:
            count+=1
            
    elif (count%6)+1 == 5:
        r+=interval
        if r >= maxval:
            count+=1
    
    elif (count%6)+1 == 6:
        b-=interval
        if b <= minval:
            count+=1
    
    print(r,g,b)
    return(r,g,b),count

def startprogram():
    print('program starting')
    
    sw = 1920
    sh = 1080
    
    screen = pygame.display.set_mode((sw,sh))
    clock = pygame.time.Clock()
    
    cx = sw/2-2.5
    cy = sh/2-2.5
    
    centerSpot = pygame.Rect(cx,cy,5,5)
    
    maxval = 255
    minval = 0
    
    colour = maxval,minval,minval
    
    rotation = 0
    step=math.pi**2
    count=0
    divisor = 2
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                
        pygame.draw.ellipse(screen,WHITE,centerSpot)
        
        x1,y1 = calculateCircleCoords(cx,cy,rotation)
        colour,count = shiftColour(colour,count,maxval,minval,step)
        circumferenceSpot = pygame.Rect(x1-2,y1-2,4,4)
        pygame.draw.ellipse(screen,colour,circumferenceSpot)
        rotation+=step
        
        for i in range(0,360):
            x2,y2 = calculateCircleCoords(x1,y1,i)
            circlespot2 = pygame.Rect(x2-0.5,y2-0.5,1,1)
            pygame.draw.ellipse(screen,colour,circlespot2)
            pygame.display.flip() 
        
        clock.tick()

if __name__ == '__main__':
    startprogram()