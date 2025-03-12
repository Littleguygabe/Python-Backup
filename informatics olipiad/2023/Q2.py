import time, os
        
def emptyShape():
        emptyShapeArr = []
        for y in range(10):
            temparr = []
            for x in range(10):
                temparr.append(0)
            emptyShapeArr.append(temparr)
        return emptyShapeArr
            
def createShape(points):
    shapeArr = emptyShape()            
    for i in range(0,len(points),2):
        shapeArr[points[i]][points[i+1]] = 1
        
    return shapeArr 
           
class Fshape():
    def __init__(self):
        self.points = [4,4,4,3,5,4,3,4,3,5]
        self.F = createShape(self.points)
            
class Gshape():
    def __init__(self):    
        self.points = [3,3,3,4,4,4,5,4,4,5]
        self.G = createShape(self.points)
        
class Ishape():
    def __init__(self):
        self.points = [2,4,3,4,4,4,5,4,6,4]
        self.I = createShape(self.points)

class Lshape():
    def __init__(self):
        self.points = [2,4,3,4,4,4,5,4,5,5]
        self.L = createShape(self.points)

class Jshape():
    def __init__(self):
        self.points = [2,4,3,4,4,4,5,4,5,3]
        self.J = createShape(self.points)

class Nshape():
    def __init__(self):
        self.points = [3,5,4,5,4,4,5,4,6,4]
        self.N = createShape(self.points)

class Mshape():
    def __init__(self):
        self.points = [3,3,4,3,4,4,5,4,6,4]
        self.M = createShape(self.points)

class Pshape():
    def __init__(self):
        self.points = [3,4,3,5,4,5,4,4,5,4]
        self.P = createShape(self.points)
        
class Qshape():
    def __init__(self):
        self.points = [3,3,3,4,4,3,4,4,5,4]
        self.Q = createShape(self.points)
        
class Tshape():
    def __init__(self):
        self.points = [3,3,3,4,3,5,4,4,5,4]
        self.T = createShape(self.points)
        
class Ushape():
    def __init__(self):
        self.points = [3,3,4,3,4,4,4,5,3,5]
        self.U = createShape(self.points)
        
class Vshape():
    def __init__(self):
        self.points = [3,3,4,3,5,3,5,4,5,5]
        self.V = createShape(self.points)
        
class Wshape():
    def __init__(self):
        self.points = [3,3,4,3,4,4,5,4,5,5]
        self.W = createShape(self.points)
    
class Xshape():
    def __init__(self):
        self.points = [3,4,4,3,5,4,4,5,4,4]
        self.X = createShape(self.points)
        
class Zshape():
    def __init__(self):
        self.points = [3,3,3,4,4,4,5,4,5,5]
        self.Z = createShape(self.points)
        
class Sshape():
    def __init__(self):
        self.points = [3,5,3,4,4,4,5,4,5,3]
        self.S = createShape(self.points)
        
class Yshape():
    def __init__(self):
        self.points = [3,4,4,3,4,4,5,4,6,4]
        self.Y = createShape(self.points)
        
class Ashape():
    def __init__(self):
        self.points = [3,4,4,5,4,4,5,4,6,4]
        self.A = createShape(self.points)
        
def printShape(shapeArr):
        for i in range(len(shapeArr)):
            print(shapeArr[i])
        
def combineShapes(shape1,shape2):
    finalShape = []
    for y in range(len(shape1)):
        temparr = []
        for x in range(len(shape1[y])):
            temparr.append(shape1[y][x]+shape2[y][x])
        finalShape.append(temparr)
        
    return finalShape
    
def shiftShape(shape,x,y):
    for i in range(0,len(shape.points),2):
        if shape.points[i]-y<0: #increases downwards
            shape.points[i] = 0
        
        elif shape.points[i]-y>9:
            shape.points[i] = 9
        
        else:
            shape.points[i] -= y
            
        if shape.points[i+1]+x<0: #increases upwards
            shape.points[i+1] = 0
        
        elif shape.points[i+1]+x>9:
            shape.points[i+1] = 9
        
        else:
            shape.points[i+1] += x
    
    return createShape(shape.points)
       

def checkCollision(points2,totalShape):
    poc = 0
    for i in range(0,len(points2),2):
        x = points2[i+1]
        y = points2[i]
        
        ## check around the point of point 2
        
        #check above
        if totalShape[y-1][x] == 1:
            for k in range(0,len(points2),2):
                if points2[k] != y-1 or points2[k+1] != x:
                    poc+=1
        #check below
        
        if totalShape[y+1][x] == 1:
            for k in range(0,len(points2),2):
                if points2[k] != y+1 or points2[k+1] != x:
                    poc+=1
                    
        #check right
        if totalShape[y][x+1] == 1:
            for k in range(0,len(points2),2):
                if points2[k] != y or points2[k+1] != x+1:
                    poc+=1
                    
        #check left
        if totalShape[y][x-1] == 1:
            for k in range(0,len(points2),2):
                if points2[k] != y or points2[k+1] != x-1:
                    poc+=1
                    
    return poc

F = Gshape()
F2 = Fshape()
collisionpoints = 0

for y in range(int(-1*(len(F.G)/2)),int(len(F.G)/2)):
    for x in range(int(-1*(len(F.G[y])/2)),int(len(F.G[y])/2)):
        F.G = shiftShape(Ishape(),x,y)
        os.system('cls')
        
        collisionpoints+=checkCollision(F2.points,combineShapes(F.G,F2.F))
        
        
print(collisionpoints)