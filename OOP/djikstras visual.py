import pygame,sys,math

def dijkstras(nodeArray,screen,nodesize):
    print(nodeArray)
    path = []
    temparray = []
    for i in range(0,len(nodeArray)):
        temparray.append(nodeArray[i]+(nodesize/2))

    basex = temparray[0]
    basey = temparray[1]

    temparray.remove(basex)
    temparray.remove(basey)

    path.append(basex)
    path.append(basey)

    while len(temparray)>0:
        shortestdist = 10000

        for i in range(0,len(temparray),2):
            xdif = basex-temparray[i]
            ydif = basey - temparray[i+1]
            totaldif = math.sqrt((xdif**2)+(ydif**2))
            if totaldif<shortestdist:
                shortestdist=totaldif
                closestx = temparray[i]
                closesty=temparray[i+1]
        temparray.remove(closestx)
        temparray.remove(closesty)
        path.append(closestx)
        path.append(closesty)
        
        basex = closestx
        basey = closesty

    screen.fill((0,0,0))
    for i in range(0,len(nodeArray),2):
        node = pygame.Surface((nodesize,nodesize))
        node.set_alpha(150)
        node.fill((200,0,50))
        screen.blit(node,(nodeArray[i],nodeArray[i+1]))

    for i in range(0,len(path)-2,2):
        pygame.draw.line(screen,(200,0,50),(path[i],path[i+1]),(path[i+2],path[i+3]))
        pygame.draw.line(screen,(200,0,50),(path[-4],path[-3]),(path[-2],path[-1]))
        pygame.draw.line(screen,(200,0,50),(path[-2],path[-1]),(path[0],path[1]))

def startsearch():
    print('program starting')

    nodeArray = []
    nodesize = 30

    sw = 1920
    sh = 1080
    screen = pygame.display.set_mode((sw,sh))
    pygame.display.set_caption("Dijkstra's Algorithm Visualisation")
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONUP:
                nodepos = pygame.mouse.get_pos()
                x=nodepos[0]-(nodesize/2)
                y=nodepos[1]-(nodesize/2)
                nodeArray.append(x)
                nodeArray.append(y)
                dijkstras(nodeArray,screen,nodesize)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        for i in range(0,len(nodeArray),2):
            node = pygame.Surface((nodesize,nodesize))
            node.set_alpha(150)
            node.fill((200,0,50))
            screen.blit(node,(nodeArray[i],nodeArray[i+1]))

        pygame.display.flip()
        clock.tick(60)
if __name__ == '__main__':
    startsearch()