import pygame,sys,random,time,math
pygame.init()

#[x] Seperation
#[] Alignment
#[] Cohesion

WHITE = (255,255,255)
GRAY = (75,75,75)
RED = (255,0,0)

class boid():
    def __init__(self,screen,sw,sh) -> None:
        self.screen = screen
        
        self.sw = sw
        self.sh = sh
        
        self.fov = 200
        self.currentAngle = random.randint(0,360)
        
        self.drawfov = False
        self.drawConnections = False

        self.pos = (random.randint(100,sw-100),random.randint(100,sh-100))
        
        self.speed=2
        self.rotationmax = 20
        
        self.viewDistance = 150
        
        self.move_vec = []
        
        self.seperate = True
        
        self.turnInterval = 5
        
        self.seperationWeight = 0.5
        self.cohesionWeight = 1.5
        
        self.nearBoids = []

    def draw(self):
        pygame.draw.circle(self.screen,GRAY,(self.pos[0],self.pos[1]),5)
        if self.drawfov:
            pygame.draw.arc(self.screen,RED,[self.pos[0]-self.viewDistance/2,self.pos[1]-self.viewDistance/2,self.viewDistance,self.viewDistance],math.radians(self.currentAngle-(self.fov/2)),math.radians(self.currentAngle+(self.fov/2)),1)
        
    def checkBorder(self):
        if self.pos[0]<=0:
            self.pos[0]+=self.sw
        elif self.pos[0]>=self.sw:
            self.pos[0]-=self.sw
            
        if self.pos[1]<=0:
            self.pos[1]+=self.sh
        elif self.pos[1]>=self.sh:
            self.pos[1]-=self.sh
                    
    def move(self,boidArr):
        #self.rotate()
        self.pos,self.move_vec = calculate_new_xy(self.pos,self.speed,-self.currentAngle)
        self.checkBorder()
        
        self.seperation(boidArr)
        self.cohesion()
        
        self.draw()
        
    def closeBoids(self,boidArr):
        self.nearBoids = []
        for boidObj in boidArr:
            dx = boidObj.pos[0] - self.pos[0]
            dy  = boidObj.pos[1] - self.pos[1]         
            if (dx*dx)+(dy*dy)<=self.viewDistance**2 and (dx**2)+(dy**2)!=0:
                temparr = []
                #calculate angle to see if within fov
                if dx == 0:
                    dx = 0.1
                    
                if dy == 0:
                    dy = 0.1
                angle2boid = math.degrees(math.atan(dy/dx))
                
                temparr.append(boidObj.pos[0])
                temparr.append(boidObj.pos[1])
                temparr.append(angle2boid)
                self.nearBoids.append(temparr)
        
    def seperation(self,boidArr):
        self.closeBoids(boidArr)
        
        for data in self.nearBoids:
            angle2boid = data[2]
            
            dx  = data[0] - self.pos[0]
            dy = data[1] - self.pos[1]
            
            boidx = data[0]
            boidy = data[1]
            
            if angle2boid>=(self.fov/2)*-1 and angle2boid<=self.fov/2:
                
                #check to ensure that the boid is on the facing side
                
                if self.isNegative(dx) == self.isNegative(self.move_vec[0]) and self.isNegative(dy) == self.isNegative(self.move_vec[1]):
                    
                    self.turnAway()
                    
                    if self.drawConnections:
                        pygame.draw.line(self.screen,RED,(self.pos[0],self.pos[1]),(boidx,boidy))
                        
    def turnAway(self):
        self.currentAngle+=self.turnInterval*self.seperationWeight
                            
    def isNegative(self,val):
        if val<0:
            return True
        else:
            return False
        
    def cohesion(self):
        angleArr = []
        for data in self.nearBoids:
            angleArr.append(data[2])
        if len(angleArr)!=0:
            averageAngle = sum(angleArr)/len(angleArr)
            
            if averageAngle<self.currentAngle:
                self.currentAngle-=self.turnInterval*self.cohesionWeight
                
            elif averageAngle>self.currentAngle:
                self.currentAngle+=self.turnInterval*self.cohesionWeight
        
        
def calculate_new_xy(old_xy, speed, angle_in_degrees):
    move_vec = pygame.math.Vector2()
    move_vec.from_polar((speed, angle_in_degrees))
    return old_xy + move_vec, move_vec
    
def startprogram():
    sw = 1800
    sh = 900
    
    screen=pygame.display.set_mode((sw,sh))
    clock = pygame.time.Clock()
    
    screen.fill(WHITE)
    
    nboids = 150
    boidArr = []
    
    for i in range(nboids):
        boidArr.append(boid(screen,sw,sh))
    boidArr[0].drawfov = True
    boidArr[0].drawConnections = True
    
    for boidObj in boidArr:
        boidObj.draw()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        
        screen.fill(WHITE)
        
        for boidObj in boidArr:
            boidObj.move(boidArr)
            
        
        pygame.display.flip()
        clock.tick()
        

if __name__ == '__main__':
    startprogram()