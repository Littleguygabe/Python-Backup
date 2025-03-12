import pygame, sys, random
pygame.init()

class point():
    def __init__(self,x,y,screen,gridsize) -> None:
        self.x = x #stored as a grid position 
        self.y = y #rather than actual coordinates
        self.screen = screen
        self.gridsize = gridsize

        self.state = 0
        self.grid = []

        self.draw()

        self.neighbours = []
        
        

    def draw(self):
        pygame.draw.rect(self.screen,
                         self.getColour(),
                         pygame.Rect(
                            self.x*self.gridsize, #x
                            self.y*self.gridsize, #y
                            self.gridsize, #width
                            self.gridsize #height
                            ))

    def getColour(self):
        if self.state == 0:
            return (0,0,0) #black / off
        
        elif self.state == 1:
            return(255,255,255) #white / on
        
    def getNeighbourStates(self):
        neighbours = []
        #TL,TC,TR,CL,CR,BL,BC,BR
        #get above states
        if self.y!=0: #get top
            if self.x!=0:
                neighbours.append(self.grid[self.y-1][self.x-1].state) #top left

            neighbours.append(self.grid[self.y-1][self.x].state) # top center

            if self.x!=len(self.grid[self.y])-1:
                neighbours.append(self.grid[self.y-1][self.x+1].state) #top left
        if self.x!=0:
            neighbours.append(self.grid[self.y][self.x-1].state)#left

        if self.x!=len(self.grid[self.y])-1:
            neighbours.append(self.grid[self.y][self.x+1].state)#right

        #get below states
        
        if self.y!=len(self.grid)-1:
                if self.x!=len(self.grid[self.y])-1:
                    neighbours.append(self.grid[self.y+1][self.x-1].state) #bottom left

                neighbours.append(self.grid[self.y+1][self.x].state) # bottom center

                if self.x!=len(self.grid[self.y])-1:
                    neighbours.append(self.grid[self.y+1][self.x+1].state) #bottom left

        self.neighbours = neighbours
    
    def checkConditions(self):
        self.getNeighbourStates()
        #print(self.neighbours)
        i = len(self.neighbours)-1 #len of neighbours -1 - same as decreasing iteration as sorts from smallest to largest
        nLocals = 0
        tempNeighbours = sorted(self.neighbours)
        try:
            while tempNeighbours[i]!=0:
                nLocals+=1
                i-=1
            
            if self.state == 1:
                #under population
                if nLocals<2:
                    self.state=0
                
                #over population
                if nLocals>3:
                    self.state=0

            else:
                if nLocals == 3:
                    self.state = 1

        except:
            print(i)
            sys.exit()
            
def startProgram():
    sw = 800
    sh = 800

    screen = pygame.display.set_mode((sw,sh))
    clock = pygame.time.Clock()

    gridSize = 10
    grid = []
    for y in range(int(sh/gridSize)):
        temparr = []
        for x in range(int(sw/gridSize)):
            temparr.append(point(x,y,screen,gridSize))
        grid.append(temparr)

    for list in grid:
        for element in list:
            element.grid = grid

    startGame = False

    while True:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    
                    elif event.key == pygame.K_SPACE:
                        startGame = True
                
        cur = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if click[0] == True:
            x,y = cur
            x = x//gridSize
            y = y//gridSize
            try:
                grid[y][x].state = 1
                grid[y][x].draw()

            except:
                print('Error: exception handling')

        if startGame == True:
            for list in grid:
                for element in list:
                    element.grid = grid

                    element.checkConditions()
                    element.draw()

        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    startProgram()