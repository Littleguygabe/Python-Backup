import pygame, sys
pygame.init()
clock = pygame.time.Clock()

screen_width = 1920
screen_height = 1080
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Machine learning file')

bg_colour = pygame.Color('grey12')

while True:
    screen.fill(bg_colour)

    pygame.display.flip()
    clock.tick(144)