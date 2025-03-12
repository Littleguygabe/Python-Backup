import pygame,sys,opensimplex,math,time,random

def generateGrid(SWIDTH,SHEIGHT,GAPSIZE):
    print('generating Grid')
    scaling = 0.3
    ncolumns = int(SWIDTH/GAPSIZE)
    nrows = int(SHEIGHT/GAPSIZE)
    grid = []
    for y in range(0,ncolumns):
        temparr = []
        yrand = random.randint(-1,1)
        for x in range(0,nrows):
            xrand = random.randint(-1,1)
            temparr.append(opensimplex.noise2(xrand*scaling,yrand*scaling))
        grid.append(temparr)
    
    return grid

def drawGrid(SCREEN, grid, GAPSIZE):
    
    freq = 0.05 #The higher the value more 'zoomed out' the image is
    width = GAPSIZE
    offset = GAPSIZE/2
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            radius = opensimplex.noise2(x*freq,y*freq)
            radius = math.sqrt(radius**2)
            pixelRect = pygame.Surface((width,width))
            R = 200*radius
            G = 255*0#(((1-radius)+radius)/2)
            B = 200*(1-radius)          
            pixelRect.fill((R,G,B))
            #pixelRect.set_alpha(255*radius)
            SCREEN.blit(pixelRect,((x+1)*(GAPSIZE/1),(y+1)*(GAPSIZE/1)))
def startprogram():
    GAPSIZE = 3
    SWIDTH = 1900
    SHEIGHT = 1000
    count=0


    SCREEN = pygame.display.set_mode((SWIDTH,SHEIGHT))
    clock = pygame.time.Clock()
    
    grid = generateGrid(SWIDTH*1,SHEIGHT*1,GAPSIZE)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print('Shutting Down')
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print('Shutting Down')
                    pygame.quit()
                    sys.exit()
                    
                if event.key == pygame.K_SPACE:
                    grid = generateGrid(SWIDTH,SHEIGHT,GAPSIZE)
                    SCREEN.fill((0,0,0))
                    drawGrid(SCREEN,grid,GAPSIZE)
        start = time.time()
        while count<1:
            count+=1
            drawGrid(SCREEN,grid,GAPSIZE)
            finish = time.time()
            time2complete = round(finish-start)
            print(f'Took {time2complete}s to load')
        
        pygame.display.flip()
        clock.tick()

if __name__ == '__main__':
    startprogram()