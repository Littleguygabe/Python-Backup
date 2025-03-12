import pygame
import sys
import random
import math

pygame.init()

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
YELLOW = (252, 198, 3)


class Player:
    def __init__(self, x, y, screen, groundArr,previnstructions,reward):
        self.x = x
        self.y = y
        self.screen = screen
        self.velocity = 10
        self.groundArr = groundArr
        self.acceleration = 1
        self.jumpStrength = 5
        self.sw = screen.get_width()
        self.sh = screen.get_height()
        self.rewarded = False

        self.prevInstructions = previnstructions
        self.instructions = []

        self.gravity = 3

        self.obj = pygame.Rect(self.x, self.y, 20, 40)
        self.jumping = False
        self.falling = False

        self.reward = reward

    def moveLeft(self):
        if self.obj.left>0:
            self.obj.x -= self.velocity

    def moveRight(self):
        if self.obj.right<self.sw:
            self.obj.x += self.velocity

    def jump(self):
        if not self.jumping and not self.falling:
            self.jumping = True

    def checkFalling(self):
        self.falling = True
        for ground in self.groundArr:
            if self.obj.colliderect(ground.obj):
                self.falling = False
                break

        if self.falling:
            self.obj.y += self.acceleration * self.gravity
            self.acceleration += 0.1

    def draw(self):
        pygame.draw.rect(self.screen, RED, self.obj)

    def move(self):
        if self.jumping:
            self.obj.y -= self.jumpStrength
            self.jumpStrength -= 1
            if self.jumpStrength <= 0:
                self.jumping = False
                self.falling = True
                self.jumpStrength = 20

        if self.falling:
            self.checkFalling()

    def findNextMove(self):
        player_pos = (self.obj.centerx, self.obj.centery)
        reward_pos = (self.reward.centerx, self.reward.centery)
        angle = math.atan2(reward_pos[1] - player_pos[1], reward_pos[0] - player_pos[0])

        # Adjust the movement based on the angle
        if -math.pi / 4 < angle < math.pi / 4:
            self.moveRight()
        elif math.pi / 4 <= angle <= 3 * math.pi / 4:
            self.jump()
        else:
            self.moveLeft()

        self.move()
        self.draw()



class Ground:
    def __init__(self, x, y, width, height, screen):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen = screen
        self.obj = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self):
        pygame.draw.rect(self.screen, WHITE, self.obj)

def findDistance(player,reward):
    xdif = player.obj.x - reward.x
    ydif = player.obj.y - reward.y

    totalDif = math.sqrt((xdif**2)+(ydif**2))

    return int(totalDif)

def startProgram(batchSize, nMovements):
    sw = 1000
    sh = 800
    screen = pygame.display.set_mode((sw, sh))
    clock = pygame.time.Clock()

    groundList = []
    playerList = []

    movements = 0
    

    reward = pygame.Rect(sw-100, sh - 75, 30, 30)

    groundList.append(Ground(0, sh - 30, sw, 30, screen))

    generation = 0

    for i in range(batchSize):
        p1 = Player(50, groundList[0].obj.top - 40, screen, groundList,[],reward)
        playerList.append(p1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if event.key == pygame.K_d:
                    playerList[0].moveRight()

                if event.key == pygame.K_a:
                    playerList[0].moveLeft()

                if event.key == pygame.K_SPACE:
                    playerList[0].jump()

        screen.fill(BLACK)

        for object in groundList:
            object.draw()

        for item in playerList:
            item.findNextMove()

        pygame.draw.rect(screen, YELLOW, reward)

        for player in playerList:
            if player.obj.colliderect(reward):
                player.rewarded = True
                print(player.rewarded)
                print(player.instructions)
        movements+=1

        if movements == nMovements:
            #get instructions for the next generation
            newInstructions = []
            #find the agents closest to the reward
            aPosDict = {}
            distances = []
            for player in playerList:
                distance = findDistance(player,reward)
                aPosDict[distance] = player
                distances.append(distance)

            #for i in range(int(math.ceil(len(playerList)*0.1))):
                
            newInstructions.append(aPosDict[sorted(distances)[0]].instructions[:int(len(aPosDict[sorted(distances)[0]].instructions)/2)])
            playerList = []
            for i in range(batchSize):
                rand = random.randint(0,len(newInstructions)-1)
                p1 = Player(50,groundList[0].obj.top-40,screen,groundList,newInstructions[rand],reward)
                print(p1.prevInstructions)
                playerList.append(p1)
            movements = 0
            generation+=1
            print(generation)

        

        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    startProgram(100, 200)
