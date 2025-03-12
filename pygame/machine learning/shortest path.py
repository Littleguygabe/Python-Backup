import pygame, sys, keyboard,time

wall = False
draw = False
drawing_outline = []
pos_list = []
temp_array = []
rect_size= 20
counter = 0
counter2 = 0
rect_positions = []
RED = 255,0,0
BLUE = 0,0,255
YELLOW = 255,255,0
GRAY = 79,79,79

def square_coords(x,y):
    ix2 = x//rect_size
    iy2 = y//rect_size

    x,y = ix2*rect_size, iy2*rect_size
    
    return x,y

def player_win_check():
    if len(pos_list)>=1:
        x2,y2 = pos_list[0]

        bupper = y2+20
        blower = y2-20
        bright = x2+20
        bleft = x2-20

        if player1.centerx<=bright and player1.centerx>=bleft and player1.centery>=blower and player1.centery<=bupper:
            print('Completed the maze')
            pygame.quit()
            sys.exit()
            
def drawGrid(): #Set the size of the grid block
    for x in range(0, screen_width, rect_size):
        for y in range(0, screen_height, rect_size):
            rect = pygame.Rect(x, y, rect_size, rect_size)
            pygame.draw.rect(screen, GRAY, rect, 1)

pygame.init()
clock = pygame.time.Clock()

screen_width = 1000
screen_height = 1000
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('shortest path finder')

bg_colour = pygame.Color('white')

player1 = pygame.Rect(0, 0, rect_size, rect_size)

while True:
    counter2 = counter2+1
    if keyboard.is_pressed('Return'):
        print('WIP')
        draw = True 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                tx,ty = event.pos
                x,y = square_coords(tx,ty)
                rect_positions.append(x)
                rect_positions.append(y)
            if counter == 0:
                if event.button == 3:
                    pos_list.append(event.pos)
                    counter = counter+1

    screen.fill(bg_colour)
    pygame.draw.rect(screen, BLUE, player1)

    for x, y in pos_list:
        fx,fy = square_coords(x,y)
        temp_array.append(fx)
        temp_array.append(fy)
        pygame.draw.rect(screen, RED, (fx,fy, rect_size, rect_size))

    for i in range(0,len(rect_positions),2):
        pygame.draw.rect(screen,GRAY,(rect_positions[i],rect_positions[i+1],rect_size,rect_size))

    player_win_check()
    drawGrid()

    if draw == True:
        print('running')

    pygame.display.update()
    clock.tick(144)
        
