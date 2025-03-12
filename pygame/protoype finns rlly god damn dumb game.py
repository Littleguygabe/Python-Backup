#
import pygame, random, sys

player1_win = False
player2_win = False
boost = True
counter1 = 720
counter1_begin = False

counter2 = 720
counter2_begin = False

counter3 = 180

redraw = True

move = False

player1_win = False
player2_win = False

game_over = False

def player1_movement():
    global old_player1_centerx, old_player1_centery
    player1.y+=player1_y_speed
    player1.x+=player1_x_speed
    
    if player1.top<=0:
        player1.top=0

    if player1.bottom >= screen_height:
        player1.bottom = screen_height

    if player1.left <= 0:
        player1.left = 0

    if player1.right >= screen_width:
        player1.right = screen_width

    if old_player1_centerx != player1.centerx or old_player1_centery != player1.centery:
        old_player1_centerx = player1.centerx
        old_player1_centery = player1.centery

        player1_path.append(player1.centerx)
        player1_path.append(player1.centery)

def player2_movement():
    global old_player2_centerx, old_player2_centery
    player2.y+=player2_y_speed
    player2.x+=player2_x_speed
    
    if player2.top<=0:
        player2.top=0

    if player2.bottom >= screen_height:
        player2.bottom = screen_height

    if player2.left <= 0:
        player2.left = 0

    if player2.right >= screen_width:
        player2.right = screen_width

    if old_player2_centerx != player2.centerx or old_player2_centery != player2.centery:
        old_player2_centerx = player2.centerx
        old_player2_centery = player2.centery

        player2_path.append(player2.centerx)
        player2_path.append(player2.centery)

def text1_movement():
    textRect1.y+=player1_y_speed
    textRect1.x+=player1_x_speed

    if player1.top<=0:
        textRect1.top=-30

    if player1.bottom >= screen_height:
        textRect1.bottom = screen_height-30

    if player1.left <= 0:
        textRect1.left = -30

    if player1.right >= screen_width:
        textRect1.right = screen_width+30

def text2_movement():
    textRect2.y+=player2_y_speed
    textRect2.x+=player2_x_speed

    if player2.top<=0:
        textRect2.top=-30

    if player2.bottom >= screen_height:
        textRect2.bottom = screen_height-30

    if player2.left <= 0:
        textRect2.left = -30

    if player2.right >= screen_width:
        textRect2.right = screen_width+30

def player1_hit():
    global player2_win
    for i in range(0,len(player2_path),2):
        if player1.centerx == player2_path[i] and player1.centery == player2_path[i+1]:
            player2_win = True
  
def player2_hit():
    global player1_win
    for i in range(0,len(player1_path),2):
        if player2.centerx == player1_path[i] and player2.centery == player1_path[i+1]:
            player1_win = True

def move_boost_point():
    global randx, randy, distance2movex, distance2movey, move, boost_colour, counter3
    if counter3 == 0:
        if move == True:
            randx = random.randint(10,screen_width-10)
            randy = random.randint(10,screen_height-10)

            distance2movex = randx-boost_token.centerx
            distance2movey = randy-boost_token.centery
            move = False
            counter3 = 180

            boost_token.x += distance2movex
            boost_token.y += distance2movey

    else:
        counter3 = counter3-1

    if counter3 != 0:
        boost_colour = bg_colour
    
    else:
        boost_colour = YELLOW

pygame.init()
clock = pygame.time.Clock()

LIME = (177, 255, 110)
BLUE = (255, 0, 0)
YELLOW = (255,255,0)
bg_colour = pygame.Color('grey12')
boost_colour = YELLOW

screen_width = 1920
screen_height = 1080
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Tron')

player1_path = []
player2_path = []

IMAGE1 = pygame.image.load('motorbike lime up.png').convert_alpha()
# Create a rect with the size of the image.
player1 = IMAGE1.get_rect()
player1.center = (screen_width/3 - 10, screen_height/2 - 10)

IMAGE2 = pygame.image.load('motorbike red up.png').convert_alpha()
# Create a rect with the size of the image.
player2 = IMAGE2.get_rect()
player2.center = ((screen_width/3)*2 - 10, screen_height/2 - 10)

randx = random.randint(10,screen_width-10)
randy = random.randint(10,screen_height-10)

boost_token = pygame.Rect(randx, randy, 20,20)

font = pygame.font.Font('freesansbold.ttf', 20)
font_bigger = pygame.font.Font('freesansbold.ttf', 100)
text1 = font.render('Player 1', True, (255,255,255))
text2 = font.render('Player 2', True, (255,255,255))

p1info = font.render('Player 1 controls: W,A,S,D', True, (255,255,255))
p2info = font.render('Player 2 controls: Arrow Keys', True, (255,255,255))

win_colour = bg_colour

wintext1 = font.render('Player 1 win!', True, win_colour)
wintext2 = font.render('Player 2 win!', True, win_colour)

player1_y_speed = 0
player1_x_speed = 0

player2_y_speed = 0
player2_x_speed = 0

movement_speed1 = 2
movement_speed2 = 2

boost_point_xspeed = 20
boost_point_yspeed = 20


old_player1_centerx = 0
old_player1_centery = 0

old_player2_centerx = 0
old_player2_centery = 0

textRect1 = text1.get_rect()
textRect1.center = (screen_width/3 - 10, screen_height/2 - 50)

textRect2 = text2.get_rect()
textRect2.center = ((screen_width/3)*2, screen_height/2 - 30)

infoRect1 = p1info.get_rect()
infoRect1.center = (133.5, 20)

infoRect2 = p2info.get_rect()
infoRect2.center = (150, 50)

while True:

    if player1.centerx>boost_token.left and player1.centerx<boost_token.right and player1.centery>boost_token.top and player1.centery<boost_token.bottom:
        movement_speed1 = 3
        
        randx = random.randint(10,screen_width-10)
        randy = random.randint(10,screen_height-10)

        counter1_begin = True
        redraw = True
        move = True

    if player2.centerx>boost_token.left and player2.centerx<boost_token.right and player2.centery>boost_token.top and player2.centery<boost_token.bottom:
        movement_speed2 = 3
        
        randx = random.randint(10,screen_width-10)
        randy = random.randint(10,screen_height-10)

        counter2_begin = True
        redraw = True
        move = True
    
    if counter1_begin == True:
        counter1 = counter1 - 1
        if counter1 == 0:
            movement_speed1 = 2
            counter1_begin = False
            counter1 = 720

    if counter2_begin == True:
        counter2 = counter2 - 1
        if counter2 == 0:
            movement_speed2 = 2
            counter2_begin = False
            counter2 = 720

    if redraw == True:
        move_boost_point()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        #player 1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player1_y_speed -= movement_speed1
                IMAGE1 = pygame.image.load('motorbike lime up.png').convert_alpha()

            if event.key == pygame.K_s:
                player1_y_speed += movement_speed1
                IMAGE1 = pygame.image.load('motorbike lime down.png').convert_alpha()

            if event.key == pygame.K_a:
                player1_x_speed -= movement_speed1
                IMAGE1 = pygame.image.load('motorbike lime left.png').convert_alpha()

            if event.key == pygame.K_d:
                player1_x_speed += movement_speed1
                IMAGE1 = pygame.image.load('motorbike lime right.png').convert_alpha()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                player1_y_speed = 0

            if event.key == pygame.K_s:
                player1_y_speed = 0

            if event.key == pygame.K_a:
                player1_x_speed = 0

            if event.key == pygame.K_d:
                player1_x_speed = 0

        #player 2
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player2_y_speed -= movement_speed2
                IMAGE2 = pygame.image.load('motorbike red up.png').convert_alpha()

            if event.key == pygame.K_DOWN:
                player2_y_speed += movement_speed2
                IMAGE2 = pygame.image.load('motorbike red down.png').convert_alpha()

            if event.key == pygame.K_LEFT:
                player2_x_speed -= movement_speed2
                IMAGE2 = pygame.image.load('motorbike red left.png').convert_alpha()

            if event.key == pygame.K_RIGHT:
                player2_x_speed += movement_speed2
                IMAGE2 = pygame.image.load('motorbike red right.png').convert_alpha()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                player2_y_speed = 0

            if event.key == pygame.K_DOWN:
                player2_y_speed = 0

            if event.key == pygame.K_LEFT:
                player2_x_speed = 0

            if event.key == pygame.K_RIGHT:
                player2_x_speed = 0
       
    player1_movement()
    player2_movement()
    text1_movement()
    text2_movement()

    player1_hit()
    player2_hit()

    screen.fill(bg_colour)
    pygame.draw.ellipse(screen, boost_colour, boost_token)
    
    
    for i in range (0,len(player1_path),2):
        player1_line = pygame.Rect(player1_path[i]-2.5,player1_path[i+1]-2.5, 5, 5)
        pygame.draw.rect(screen, LIME, player1_line)
        
    for i in range (0,len(player2_path),2):
        player2_line = pygame.Rect(player2_path[i]-2.5,player2_path[i+1]-2.5, 5, 5)
        pygame.draw.rect(screen, BLUE, player2_line)

    screen.blit(IMAGE1, player1)
    screen.blit(IMAGE2, player2)
    screen.blit(text1, textRect1)
    screen.blit(text2, textRect2)

    screen.blit(p1info, infoRect1)
    screen.blit(p2info, infoRect2)

    if game_over == True:
        pygame.time.wait(2000)
        pygame.quit()

    if player1_win == True:
        label = font_bigger.render("Player 1 wins!", 1, LIME)
        screen.blit(label, (screen_width/2-350,screen_height/2-70))
        game_over = True

    if player2_win == True:
        label = font_bigger.render("Player 2 wins!", 1, BLUE)
        screen.blit(label, (screen_width/2-350,screen_height/2-70))
        game_over = True


    pygame.display.flip()
    clock.tick(144)