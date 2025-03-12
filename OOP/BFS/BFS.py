import pygame,sys,random, time
pygame.init()

DARKGREY = (60,60,60)     

def BFS(graph,startNode,endNode,nodesP,screen):
    visitedNodes = []
    Q = [startNode]
    parents = {}

    while Q:
        currentNode = Q.pop(0)
        visitedNodes.append(currentNode)
        for neighbour in graph[currentNode]:
            if neighbour not in visitedNodes:
                Q.append(neighbour)
                parents[neighbour] = currentNode
        pygame.draw.circle(screen,'RED',(nodesP[int(currentNode)][0],nodesP[int(currentNode)][1]),10)
        pygame.display.flip()
        time.sleep(0.1)
    return (shortestP(parents,startNode,endNode))


def shortestP(parents,startNode,endNode):
    path = [endNode]
    currentNode = endNode
    while currentNode != startNode:
        currentNode = parents[(currentNode)]
        path.append(currentNode)
    path.reverse()
    return path



def startprogram():
    sw=3000
    sh=1000
    screen=pygame.display.set_mode((sw,sh))
    clock = pygame.time.Clock()
    screen.fill('WHITE')

    nodesP = {}
    nCount = 1

    radius = 10

    start = False
    structCreate = False

    finished = False

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
                    start = True

            if event.type == pygame.MOUSEBUTTONUP:
                center = pygame.mouse.get_pos()
                nodesP[nCount] = ([center[0],center[1]])
                nCount+=1
        if not finished:        
            for positions in nodesP:
                pygame.draw.circle(screen,DARKGREY,(nodesP[positions][0],nodesP[positions][1]),radius)
            
        if start:
            startNode = nodesP[1]
            endNode = nodesP[len(nodesP)]
            pygame.draw.circle(screen,'GREEN',(startNode[0],startNode[1]),radius)
            pygame.draw.circle(screen,'YELLOW',(endNode[0],endNode[1]),radius)
            ### create the tree data structure
            if not structCreate:
                tree = {}
                for id in nodesP:
                    temp = []
                    for i in range(1):
                        num = id
                        while num == id:
                            num = random.randint(1,len(nodesP))

                        temp.append(str(num))

                        ### make the path bidirectional

                    tree[str(id)] = temp
                
                for item in tree:
                    for itemid in tree[item]:
                        if item not in tree[itemid]:
                            temp = tree[itemid]
                            temp.append(item)
                            tree[itemid] = temp

                structCreate = True

                ### draw lines between connected nodes
                for i in range(1,len(tree)+1):
                    for k in tree[str(i)]:
                        pygame.draw.line(screen, DARKGREY, (nodesP[i][0],nodesP[i][1]), (nodesP[int(k)][0], nodesP[int(k)][1]),3)                
                path = BFS(tree,'1',str(len(tree)),nodesP,screen)
                for i in range(len(path)-1):
                    pointa = nodesP[int(path[i])]
                    pointb = nodesP[int(path[i+1])]
                    pygame.draw.line(screen,'GREEN',(pointa[0],pointa[1]),(pointb[0],pointb[1]))

            ## randomly pick 
        pygame.display.flip()
        clock.tick(60)
            
if __name__ == '__main__':
    startprogram()