import pygame,sys, random,time
pygame.init()

WHITE = (255,255,255)
GRAY = (75,75,75)
RED = (255,0,0)
GREEN = (0,255,0)

class element():
    def __init__(self,x,y,size,screen,font):
        self.isBomb = False
        self.x = x
        self.y = y
        self.size = int(size)
        self.screen = screen
        self.colour = WHITE
        self.isExposed = False
        self.nearbyBombs = 0
        self.font = font
        self.isflagged=False

    def draw(self):
        rect = pygame.Rect(self.x,self.y,self.size,self.size)
        pygame.draw.rect(self.screen,self.colour,rect)

        #render text for nearby bombs
    def renderText(self):
        if self.nearbyBombs != 0 and not self.isBomb:
            text_surface = self.font.render(str(self.nearbyBombs), True, WHITE)
            text_rect = text_surface.get_rect()
            text_rect.topleft = (self.x, self.y)
            self.screen.blit(text_surface, text_rect)

    def countNearbyBombs(self,itemsArray,nsqaures):
        for dy in range(-1,2):
            for dx in range(-1,2):
                if dx == 0 and dy == 0:
                    continue
                x = (self.x//self.size)+dx
                y = (self.y//self.size)+dy
                if 0<=x<nsqaures and 0<=y<nsqaures:
                    if itemsArray[x][y].isBomb == True:
                        self.nearbyBombs+=1

def generateGrid(screen,sw,Nsquares):
    itemsArray = []
    nBombs = 145
    font = pygame.font.Font(None,int(sw/Nsquares)*2)

    for i in range(0,sw,int(sw/Nsquares)):
        
        temparr = []
        for j in range(0,sw,int(sw/Nsquares)):
            item = element(i,j,(sw/Nsquares),screen,font)            
            item.draw()

            temparr.append(item)

        itemsArray.append(temparr)

    for i in range(0,nBombs):
        randx = random.randint(0,Nsquares-1)
        randy = random.randint(0,Nsquares-1)
        itemsArray[randx][randy].isBomb = True


    return itemsArray  

def draw_grid(sw,Nsquares,screen):
    cw = int(sw/Nsquares)
    for x in range(0, sw, cw):
        pygame.draw.line(screen, GRAY, (x, 0), (x, sw))
    for y in range(0, sw, cw):
        pygame.draw.line(screen, GRAY, (0, y), (sw, y))

def findNeighbours(x,y,ns):
    neighbours = []
    for dy in range(-1,2):
        for dx in range(-1,2):
            if dy == 0 and dx == 0:
                continue
            nx = x+dx
            ny = y+dy
            if 0<=nx<ns and 0<=ny<ns:
                neighbours.append((nx,ny))
    return neighbours

def uncovercell(x, y, itemsArray, nsquares):
    stack = [(x, y)]
    while stack:
        x, y = stack.pop()
        if not itemsArray[x][y].isExposed:
            itemsArray[x][y].isExposed = True
            itemsArray[x][y].colour = GRAY
            itemsArray[x][y].draw()
            itemsArray[x][y].renderText()
            if not itemsArray[x][y].isBomb:
                for nx, ny in findNeighbours(x, y, nsquares):
                    if not itemsArray[nx][ny].isExposed and itemsArray[nx][ny].nearbyBombs==0 and not itemsArray[nx][ny].isBomb:
                        stack.append((nx, ny))
                    elif not itemsArray[nx][ny].isExposed and not itemsArray[nx][ny].isBomb:
                        itemsArray[nx][ny].colour=GRAY
                        itemsArray[nx][ny].draw()
                        itemsArray[nx][ny].renderText()

def checkBoard(itemsArray):
    for innerlist in itemsArray:
        for item in innerlist:
            if item.isBomb!=item.isflagged:
                return False
    return True

def drawCorrections(itemsArray):
    correctCount = 0
    totalCount = 0 
    for innerlist in itemsArray:
        for item in innerlist:
            if item.isBomb == True and item.isflagged:
                item.colour = GREEN
                totalCount+=1
                correctCount+=1
            elif item.isBomb == True:
                item.colour = RED
                totalCount+=1
            else:
                item.colour = GRAY
            item.draw()
    print(f'You got {correctCount}/{totalCount} bombs correct')
def startprogram():
    sw=1000
    screen=pygame.display.set_mode((sw,sw))
    clock = pygame.time.Clock()

    Nsquares = 40

    screen.fill(WHITE)
    itemsArray = generateGrid(screen,sw,Nsquares)

    #find num nearby bombs
    for innerlist in itemsArray:
        for item in innerlist:
            item.countNearbyBombs(itemsArray,Nsquares)

    draw_grid(sw,Nsquares,screen)

    while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                    if event.key == pygame.K_RETURN:
                        if checkBoard(itemsArray):
                            print('Winner!')
                        else:
                            print('Loser!')
                            print('Green is bombs you got correct and red is the ones you missed')
                        drawCorrections(itemsArray)
                            

                if event.type == pygame.MOUSEBUTTONUP:
                    x,y = pygame.mouse.get_pos()
                    item = itemsArray[int(x//(sw/Nsquares))][int(y//(sw/Nsquares))]

                    if event.button == 3:
                        #right click flag bomb
                        item.colour = RED
                        item.isflagged=True
                        item.draw()
                    elif event.button == 1:
                        item.colour = GRAY
                        if item.isBomb:
                            print('Game Over')
                            drawCorrections(itemsArray)
                        else:
                            uncovercell(int(x//(sw/Nsquares)),int(y//(sw/Nsquares)),itemsArray,Nsquares)
                            
                            item.draw()
                            item.renderText()
                    item.isExposed=True
                    
            
            pygame.display.flip()
            clock.tick(30)
            
if __name__ == '__main__':
    startprogram()