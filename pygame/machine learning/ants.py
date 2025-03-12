import pygame

DARKRED = 102,0,0
GREEN = 0,255,0
GRAY = 79,79,79

pygame.init()
clock = pygame.time.Clock()

screen_width = 1000
screen_height = 1000

screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Ants?')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    screen.fill(GRAY)

    pygame.display.update()
    clock.tick(144)