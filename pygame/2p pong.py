import pygame, sys, random, os


player_score = 0
opponent_score = 0
old_player_score = 0
old_opponent_score = 0

def ball_animation():
    global ball_speed_x, ball_speed_y, player_score, opponent_score
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.left <= 0:
        player_score = player_score + 1
        #os.system('cls')
        print(f'Player 1: {player_score}')
        print(f'Player 2: {opponent_score}')
    if ball.right>= screen_width:
        os.system('cls')
        opponent_score = opponent_score + 1
        print(f'Player 1: {player_score}')
        print(f'Player 2: {opponent_score}')


    if ball.top <= 0 or ball.bottom>= screen_height:
        ball_speed_y *= -1
    if ball.left <= 0 or ball.right>= screen_width:
        ball_restart()

    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_speed_x *= -1

def player_animation():
    player.y+=player_speed
    
    if player.top<=0:
        player.top=0

    if player.bottom >= screen_height:
        player.bottom = screen_height

def player_2_animation():
    opponent.y+=player_2_speed
    
    if opponent.top<=0:
        opponent.top=0

    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height

def ball_restart():
    global ball_speed_x_variable, ball_speed_y_variable, ball_speed_x, ball_speed_y
    ball.center = (screen_width/2,screen_height/2)
    ball_speed_y_variable = ball_speed_y_variable + 0.5
    ball_speed_x_variable = ball_speed_x_variable + 0.5
    ball_speed_y = ball_speed_y_variable
    ball_speed_x = ball_speed_x_variable
    print(f'{ball_speed_x_variable}, {ball_speed_y_variable}')

    if ball_speed_x<1:
        ball_speed_x = ball_speed_x*-1

    if ball_speed_y<1:
        ball_speed_y = ball_speed_y*-1

    ball_speed_x = ball_speed_x * random.choice((1,-1))
    ball_speed_y = ball_speed_y * random.choice((1,-1))
#general setup
pygame.init()
clock = pygame.time.Clock()

#setting up the main window
screen_width = 1920
screen_height = 1080
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')

#rectangles in game
ball = pygame.Rect(screen_width/2 - 15,screen_height/2 - 15,30,30)
player = pygame.Rect(screen_width-20,screen_height/2 - 70,10,200)
opponent = pygame.Rect(10,screen_height/2 - 70,10,200)

bg_colour = pygame.Color('grey12')
light_grey = (200,200,200)

ball_speed_x = 3 * random.choice((1,-1))
ball_speed_y = 3 * random.choice((1,-1))
player_speed = 0
player_2_speed = 0
ball_speed_x_variable = 3
ball_speed_y_variable = 3

while True:
    #handling input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        #player 1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed += 3
            if event.key == pygame.K_UP:
                player_speed -= 3

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_speed -= 3
            if event.key == pygame.K_UP:
                player_speed += 3

        #player 2
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                player_2_speed += 3
            if event.key == pygame.K_w:
                player_2_speed -= 3

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_s:
                player_2_speed -= 3
            if event.key == pygame.K_w:
                player_2_speed += 3

    ball_animation()
    player_animation()
    player_2_animation()

    old_player_score = player_score
    old_opponent_score = opponent_score
    

    #visuals
    screen.fill(bg_colour)
    pygame.draw.rect(screen,light_grey, player)
    pygame.draw.rect(screen,light_grey, opponent)
    pygame.draw.ellipse(screen,light_grey,ball)
    pygame.draw.aaline(screen,light_grey,(screen_width/2,0), (screen_width/2,screen_height))

    #updating the window
    pygame.display.flip()
    clock.tick(144)
