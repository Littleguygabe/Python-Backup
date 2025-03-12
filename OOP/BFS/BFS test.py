# create algorithm to generate the tree structure
graph = {
    '0':['3','5','9'],
    '1':['6','7','4'],
    '2':['10','5'],
    '3':['0'],
    '4':['1','5','8'],
    '5':['2','0','4'],
    '6':['1'],
    '7':['1'],
    '8':['4'],
    '9':['0'],
    '10':['2']
        }

def BFS(graph,startNode,endNode):
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
        print(currentNode)  ## this is where it moves from node to node 
    print(shortestP(parents,startNode,endNode))


def shortestP(parents,startNode,endNode):
    path = [endNode]
    currentNode = endNode
    while currentNode != startNode:
        currentNode = parents[currentNode]
        path.append(currentNode)

    path.reverse()
    return path

BFS(graph,'0','1')