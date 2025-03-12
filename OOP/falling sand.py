import os
class sandGrid():
    def __init__(self) -> None:
        self.grid = setupGrid()
        
        self.displayGrid()

    def displayGrid(self):
        os.system('cls')
        for row in self.grid:
            print(row)

    def placeSand(self,x,y): # takes in read value rather than array value -- ie. 1 represents pos 0
        self.grid[y-1][x-1] = 1

        self.appPhysics()
    
    def appPhysics(self):
        pass

def setupGrid():
    cgrid = []
    gridSize = 10
    for i in range(gridSize):
        temp = []
        for k in range(gridSize):
            temp.append(0)
        cgrid.append(temp)

    return cgrid

def startProg():
    grid1 = sandGrid()
    grid1.placeSand(7,1)
    grid1.displayGrid()
    
if __name__ == '__main__':
    startProg()