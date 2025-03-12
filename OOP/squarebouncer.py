import pygame,sys
pygame.init()

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

    return(r,g,b),count

def move(x,y,xmult,ymult,movestep,sw,sh,ss):
    #bounce off the top
    if y-ss/2<=0:
        ymult=1
        
    #bounce off bottom
    elif y+ss/2>=sh:
        ymult=-1
        
    #bounce off of left
    if x-ss/2<=0:
        xmult = 1
        
    elif x+ss/2>=sw:
        xmult=-1
        
    x+=xmult*movestep
    y+=ymult*movestep
    
    return x,y,xmult,ymult

def create_rect(width, height, border, color, border_color):
    surf = pygame.Surface((width+border*2, height+border*2), pygame.SRCALPHA)
    pygame.draw.rect(surf, color, (border, border, width, height), 0)
    for i in range(1, border):
        pygame.draw.rect(surf, border_color, (border-i, border-i, width+5, height+5), 1)
    return surf

def startprogram():
    sw=1500
    sh=900
    screen=pygame.display.set_mode((sw,sh))
    clock = pygame.time.Clock()
    
    movestep = 2
    xmult=1
    ymult=1
    
    squaresize=30
    x=squaresize/2
    y=squaresize/2
    
    maxval = 255
    minval = 0
    
    colour = maxval,minval,minval
    count = 0
    step = 10
    screen.fill('white')
    
    
    while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                        
            x,y,xmult,ymult = move(x,y,xmult,ymult,movestep,sw,sh,squaresize)
                        
            colour,count = shiftColour(colour,count,maxval,minval,step)
            colour = (255,0,0)
            rect1 = create_rect(squaresize, squaresize, 5, colour, (0, 0, 0))
            screen.blit(rect1,(x,y))
            
            pygame.display.flip()
            clock.tick(160)
            
            
if __name__ == '__main__':
    startprogram()