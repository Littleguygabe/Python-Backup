import time
import os
import random

class Queue():
    def __init__(self) -> None:
        self.queue = []

    def push(self,x):
        self.queue.append(x)

    def pop(self):
        popped = self.queue.pop(0)
        return popped


class breadthFirstSearch():
    def __init__(self,map) -> None:
        self.queue = Queue()
        self.map = map
        self.rows = len(self.map)
        self.cols = len(self.map[0])



        self.findStartPosition()
        self.performSearch()        

    def performSearch(self) -> list: 
        #keep an array of the positions that get us to the end point
        self.queue.push([self.startX,self.startY])

        while len(self.queue.queue)!=0:
            curPos = self.queue.pop()
            self.visualise(curPos)

            neighbours = self.getNeighbours(curPos)
            if len(neighbours) == 0:
                continue

            if self.checkIsNeighbourFinish(neighbours):
                print('found the finish')
                time.sleep(1)
                return

            for pos in neighbours:
                self.queue.push(pos)

        print('Cannot reach the finish')
        time.sleep(1)
        return

    def visualise(self,curPos):
            os.system('cls')
            self.map[curPos[1]][curPos[0]] = 'o'
            self.printMap(curPos)
            time.sleep(0.05)       

    def printMap(self,curPos):
        for j in range(self.rows):
            for i in range(self.cols):
                if [i,j] == curPos:
                    print(f"\033[31m{self.map[j][i]}\033[0m",end= ' ')  # Prints "R" in red

                else:
                    print(self.map[j][i],end=' ')
        
            print()

    def checkIsNeighbourFinish(self,neighbours) -> bool:
        for i,j in neighbours:
            if self.map[j][i] == '1':
                return True
            
        return False

 
    def findStartPosition(self) -> None:
        for j in range(self.rows):
            for i in range(self.cols):

                if self.map[j][i] == '0':
                    self.startY = j
                    self.startX = i
                    return
                    


    def getNeighbours(self,curPos) -> list:
        # return list of coordinates of neighbours that havent alrady been chacked and arent X's
        neighbours = []
        blockedSymbols = ['X','o']    


        # check neighbour above
        if curPos[1]!=0 and self.map[curPos[1]-1][curPos[0]] not in blockedSymbols and [curPos[0],curPos[1]-1] not in self.queue.queue:
            neighbours.append([curPos[0],curPos[1]-1])

        #check below
        if curPos[1]!=self.rows and self.map[curPos[1]+1][curPos[0]] not in blockedSymbols and [curPos[0],curPos[1]+1] not in self.queue.queue:
            neighbours.append([curPos[0],curPos[1]+1])
        #check the left
        
        if curPos[0]!=0 and self.map[curPos[1]][curPos[0]-1] not in blockedSymbols and [curPos[0]-1,curPos[1]] not in self.queue.queue:
            neighbours.append([curPos[0]-1,curPos[1]])
        
        #check the right
        if curPos[0]!=self.cols and self.map[curPos[1]][curPos[0]+1] not in blockedSymbols and [curPos[0]+1,curPos[1]] not in self.queue.queue:
            neighbours.append([curPos[0]+1,curPos[1]])

        return neighbours


def createRandomMaze() -> list[list]:
    coverage = 30 
    width = 30
    height = 10
    maze = []
    
    for j in range(height):
        tempArr = []
        for i in range(width):
            if random.randint(0,100)<=coverage:
                tempArr.append('X')

            else:
                tempArr.append(' ')

        maze.append(tempArr)

    finalMaze = []
    tempArr = []
    for i in range(width+2):
        tempArr.append('X')

    finalMaze.append(tempArr)

    singleX = ['X']

    for row in maze:
        finalMaze.append(singleX+row+singleX)

    finalMaze.append(tempArr)




    finalMaze[random.randint(1,height)][0] = '0'
    finalMaze[random.randint(1,height)][width+1] = '1'




    for row in finalMaze:
        print(row)

    return finalMaze



while True:
    maze = createRandomMaze()
    search = breadthFirstSearch(maze)

