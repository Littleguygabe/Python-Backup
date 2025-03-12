import pygame
pygame.init()

win = pygame.display.set_mode((1000,500))
pygame.display.set_caption("First Game")

x = 0
y = 260
width = 1000
height = 240
vel = 5

isJump = False
jumpCount = 10

player_run_sprite = pygame.image.load('sprite2.jpg').convert_alpha()

run = True

while run:
    pygame.time.delay(20)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
            
    if not(isJump): 
        if keys[pygame.K_SPACE]:
            isJump = True
    else:
        if jumpCount >= -10:
            y -= (jumpCount * abs(jumpCount)) * 0.5
            jumpCount -= 1
        else: 
            jumpCount = 10
            isJump = False
    
    win.fill((255,255,255))
    win.blit(player_run_sprite, (x, y))  
    pygame.display.update() 
    
pygame.quit()