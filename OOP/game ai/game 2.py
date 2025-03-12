import pygame,sys
pygame.init()

WHITE = (255,255,255)
RED = (255,0,0)
BLACK = (0,0,0)


def startprogram():
    sw=1920
    sh=1080

    ground = pygame.Rect(0,900,1920,30)
    player = pygame.Rect(500,500,20,40)

    screen=pygame.display.set_mode((sw,sh))
    clock = pygame.time.Clock()

    gravityMul = 1
    acceleration = 1
    jumpAcceleration = 1

    jumpStrength = 50
    is_jumping = False

    playerSpeed = 5

    movingRight = False
    movingLeft = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                elif event.key == pygame.K_SPACE and pygame.Rect.colliderect(player,ground):
                    acceleration = 1
                    jumpAcceleration = 1
                    is_jumping = True

                if event.key == pygame.K_d:
                    movingRight = True

                if event.key == pygame.K_a:
                    movingLeft = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    movingRight = False
                
                if event.key == pygame.K_a:
                    movingLeft = False

        screen.fill(BLACK)

        pygame.draw.rect(screen,WHITE,ground) #ground
        pygame.draw.rect(screen,RED,player) #player

        if movingRight and player.right<sw:
            player.x+=playerSpeed

        if movingLeft and player.left>0:
            player.x-=playerSpeed

        if not pygame.Rect.colliderect(player,ground):
            player.bottom+=1*gravityMul*acceleration
            acceleration+=0.1

            if player.bottom>=ground.top:
                player.bottom = ground.top+1 

        if is_jumping:
            if jumpAcceleration>=0:
                player.bottom -= jumpStrength*jumpAcceleration
                jumpAcceleration-=0.1
            else:
                is_jumping = False

        
        pygame.display.flip()
        clock.tick(60)
            
if __name__ == '__main__':
    startprogram()