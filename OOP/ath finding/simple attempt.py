import random,os,time

class grid():
    def __init__(self) -> None:
        self.gridSize = 8
        self.createGrid()
    
        self.start = [1,2]
        self.finish = [7,8] #x,y

        self.grid[self.finish[1]-1][self.finish[0]-1] = 'F' #y,x
        self.grid[self.start[1]-1][self.start[0]-1] = 'S'


    def createGrid(self):
        self.grid = []
        for i in range(self.gridSize):
            temp = []
            for j in range(self.gridSize):
                blocked = random.randint(0,3)
                if blocked == 0:
                    temp.append('X')
                else:
                    temp.append(' ')
            self.grid.append(temp)

class searchAlgorithm():
    def __init__(self,grid) -> None:
        self.grid2work = grid

        self.voidList = [] # for cells that cannot be progressed

        self.goalFound = False

        self.findCurrentPosition()
        self.findFinishPosition()
        self.findStartPosition()

        self.visitedPoints = [] #2d array storing coordinates of visited cells [x,y]/[column,row]
        self.path = []
        self.path.append(self.startPosition)

        self.drawAlgGrid()

        while not self.goalFound:
            self.runAlgorithm()

    def findCurrentPosition(self):
        for j in range(len(self.grid2work)):
            for i in range(len(self.grid2work[j])):
                if self.grid2work[j][i] == 'S':
                    self.currentPosition = [i,j]
    
    def findFinishPosition(self):
        for j in range(len(self.grid2work)):
            for i in range(len(self.grid2work[j])):
                if self.grid2work[j][i] == 'F':
                    self.finishPosition = [i,j]

    def findStartPosition(self):
        for j in range(len(self.grid2work)):
            for i in range(len(self.grid2work[j])):
                if self.grid2work[j][i] == 'S':
                    self.startPosition = [i,j]

    def calculateHcost(self): #optimistic estimate to finish
        xHcost = abs(self.finishPosition[0]-self.currentPosition[0])
        yHcost = abs(self.finishPosition[1]-self.currentPosition[1])

        return xHcost+yHcost 

    def calculateGcost(self):
        return len(self.path)

    def calculateFcost(self):
        return self.calculateGcost()+self.calculateHcost()

    def drawAlgGrid(self):
        time.sleep(0.25)
        os.system('cls')

        for item in self.visitedPoints:
            try:
                self.grid2work[item[1]][item[0]] = '/'
            except:
                pass

        for item in self.path:
            self.grid2work[item[1]][item[0]] = 'P'
        self.grid2work[self.currentPosition[1]][self.currentPosition[0]] = 'O'
        self.grid2work[self.startPosition[1]][self.startPosition[0]] = 'S'
        self.grid2work[self.finishPosition[1]][self.finishPosition[0]] = 'F'

        print('Algorithm Grid View:')
        for horizontalRow in self.grid2work:
            print(horizontalRow)

    def runAlgorithm(self):
        lowestFcost = 10000
        nextPosition = []
        basePosition = self.currentPosition
        pos2check = [[0,1],[1,0],[0,-1],[-1,0]] #x,y
        blockedcells = 0
        for pos in pos2check:
            self.currentPosition = [a+b for a,b in zip(self.currentPosition,pos)]
            if self.currentPosition[0]>=0 and self.currentPosition[0]<=len(self.grid2work) and self.currentPosition[1]>=0 and self.currentPosition[1]<=len(self.grid2work):
                if self.grid2work[self.currentPosition[1]-1][self.currentPosition[0]-1] == 'F':
                    self.goalFound = True
                    self.drawAlgGrid()
                    break
                elif self.grid2work[self.currentPosition[1]-1][self.currentPosition[0]-1] == 'X':
                    blockedcells+=1
                    print(f'blocked cells: {blockedcells}')
                cost = self.calculateFcost()
                if cost<lowestFcost:
                    lowestFcost = cost
                    nextPosition = self.currentPosition

                self.visitedPoints.append(self.currentPosition)
                self.currentPosition = basePosition

                self.drawAlgGrid()
            else:
                blockedcells+=1
                print(f'blocked cells: {blockedcells}')
        if blockedcells == 3:
            self.voidList.append(self.currentPosition)
            self.currentPosition = self.path[-1]


        time.sleep(0.2)
        self.currentPosition = nextPosition
        self.path.append(self.currentPosition)

grid1 = grid()
alg = searchAlgorithm(grid1.grid)