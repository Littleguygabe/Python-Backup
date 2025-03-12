import os
import random

#SEPERATE IF STATEMENT FOR EACH COLUMN

board = [[' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ',' ',' ']]

#posx = 0, posy = 1
positions =[]
choice = input('AI or 2 player (ai/2p)? ')

finish = False

def playerturn(column, playertoken):
    if board[0][column] == ' ':
        for i in range(0,5):
            if board[i+1][column] != ' ':
                board[i][column] = playertoken
                positions.clear()
                positions.append(column)
                positions.append(i)
                #print(dropPosx,',',dropPosy)
                playerWinCheck()
                break
                
            elif i+1 == 5:
                positions.clear()
                board[5][column] = playertoken
                positions.append(column)
                positions.append(5)
                playerWinCheck()
                break
    else:
        print('no room in column 1')
        
    os.system('cls')
    for i in range(0,6):
        print(board[i])

def playerWinCheck():
#check horizontal
    posx = positions[0]
    posy = positions[1]

    #HORIZONTAL CHECKS
    if column<4:
        if board[posy][posx] == board[posy][posx+1] and board[posy][posx] == board[posy][posx+2] and board[posy][posx] == board[posy][posx+3]:
            print('Player Win!')
            print('4 in a row')
            exit()

    if column>1 and column<5:
        if board[posy][posx] == board[posy][posx-1] and board[posy][posx] == board[posy][posx+1] and board[posy][posx] == board[posy][posx+2]:
            print('Player Win!')
            print('4 in a row')
            exit()
            
    if column>2 and column<6:
        if board[posy][posx] == board[posy][posx-2] and board[posy][posx] == board[posy][posx-1] and board[posy][posx] == board[posy][posx+1]:
            print('Player Win!')
            print('4 in a row')
            exit()
            
    if column>3:
        if board[posy][posx] == board[posy][posx-1] and board[posy][posx] == board[posy][posx-2] and board[posy][posx] == board[posy][posx-3]:
            print('Player 1 Win!')
            print('4 in a row')
            exit()
            
    #VERTICAL CHECKS
    if posy<=2 :
        if board[posy][posx] == board[posy+1][posx] and board[posy][posx] == board[posy+2][posx] and board[posy][posx] == board[posy+3][posx]:
            print('Player Win!')
            print('4 in a row')
            exit()

    #POSITIVE DIAGONAL CHECK
    if posy>=3 and column<=2:
        if board[posy][posx] == board[posy-1][posx+1] and board[posy][posx] == board[posy-2][posx+2] and board[posy][posx] == board[posy-3][posx+3]:
            print('Player Win!')
            print('4 in a row')
            exit()
            
    if posy>=3 and column>=3:
        if board[posy][posx] == board[posy-1][posx-1] and board[posy][posx] == board[posy-2][posx-2] and board[posy][posx] == board[posy-3][posx-3]:
            print('Player Win!')
            print('4 in a row')
            exit()
            
    #NEGATIVE DIAGONAL CHECK
    if posy<=2 and column<=4:
        if board[posy][posx] == board[posy+1][posx+1] and board[posy][posx] == board[posy+2][posx+2] and board[posy][posx] == board[posy+3][posx+3]:
            print('Player Win!')
            print('4 in a row')
            exit()
            
    if posy<=2 and column>=4:
        if board[posy][posx] == board[posy+1][posx-1] and board[posy][posx] == board[posy+2][posx-2] and board[posy][posx] == board[posy+3][posx-3]:
            print('Player Win!')
            print('4 in a row')
            exit()

def hardAIplayChoice():
    

    x = positions[0]
    y= positions[1]
    print(positions)
    while True:
        if y != 5:
            if x<=3:
                if board[y][x+1] == 'X': #check to the right
                    print('to the right')
                    if board[y][x+2] == 'X': #check to the right
                        if x+3 != 6:
                            column=x+3
                            playerturn(column,'O')
                            break
                        
                        else:
                            column=x-1
                            playerturn(column,'O')
                            break
                    else:
                        print('ln131')
                        
                else:
                    print('ln134')
                    

            if x<=4:
                if board[y][x-1] == 'X': #check to the left
                    print('on the left')
                    if board[y][x-2] == 'X':
                        if x-3>0:
                            column = x-3
                            print(x-3)
                            playerturn(column,'O')
                            break
                            
                        else:
                            column = x+1
                            playerturn(column,'O')
                            break
                    else:
                        print('ln152')
                        
                else:
                    print('ln155')
                    

            if y<=3:
                if board[y+1][x] == 'X': #check below
                    if board[y+2][x] == 'X':
                        column = x
                        playerturn(column,'O')
                        break
                    else:
                        print('ln165')
                        
                else:
                    print('ln168')
                    

            if x<=4 and y>=2:
                if board[y-1][x+1] == 'X':#check top right
                    if board[y-2][x+2] == 'X':
                        if x+3>6:
                            column=x-1
                            playerturn(column,'O')
                            break
                        else:
                            column = x+3
                            playerturn(column,'O')
                            break
                    else:
                        print('ln183')
                        
                else:
                    print('ln186')
                    

            if x>=2 and y>=2:
                if board[y-1][x-1] == 'X': #check top left
                    if board[y-2][x-2] == 'X':
                        if x-3<0 or y-2 == 0:
                            column = x+1
                            playerturn(column,'O')
                            break
                        else:
                            column = x-3
                            playerturn(column,'O')
                            break
                    else:
                        print('ln201')
                        
                else:
                    print('ln204')
                    

            if x<=4 and y<=3:
                if board[y+1][x+1] == 'X': #check bottom right
                    if board[y+2][x+2] == 'X':
                        if x+3 == 7:
                            column = x-1
                            playerturn(column, 'O')
                            break
                        
                        else:
                            column = x+3
                            playerturn(column, 'O')
                    else:
                        print('ln219')
                        
                else:
                    print('ln222')
                    
            
            if x>=2 and y<=3:
                if board[y+1][x-1] == 'X': #check bottom left
                    if board[y+2][x-2] == 'X':
                        if x+1 == 7:
                            column = x-3
                            playerturn(column, 'O')
                            break
                
                        else:
                            column = x+1
                            playerturn(column, 'O')
                            break
                    else:
                        print('ln238')
                        
                else:
                    print('ln241')
                    
            if x == x:
                column = random.randint(0,6)
                playerturn(column,'O')
                break


        elif y == 5:
            if x<=3:
                if board[y][x+1] == 'X': #check to the right
                    print('to the right')
                    if board[y][x+2] == 'X':
                        if x+3 != 6:
                            column=x+3
                            playerturn(column,'O')
                            break
                        
                        else:
                            column=x-1
                            playerturn(column,'O')
                            break
                    else:
                        print('ln264')
                        
                else:
                    print('ln267')
                    
            
            if x<=4:
                if board[y][x-1] == 'X': #check to the left
                    print('on the left')
                    if board[y][x-2] == 'X':
                        if x-3>0:
                            column = x-3
                            print(x-3)
                            playerturn(column,'O')
                            break
                            
                        else:
                            column = x+1
                            playerturn(column,'O')
                            break
                    else:
                        print('ln286')
                        
                else:
                    print('ln288')
                    

            if x<=4 and y>=2:
                if board[y-1][x+1] == 'X':#check top right
                    if board[y-2][x+2] == 'X':
                        if x+3>6:
                            column=x-1
                            playerturn(column,'O')
                            break
                        else:
                            column = x+3
                            playerturn(column,'O')
                            break
                    else:
                        print('ln304')
                        
                else:
                    print('ln307')
                    
            
            if x>=2 and y>=2:
                if board[y-1][x-1] == 'X': #check top left
                    if board[y-2][x-2] == 'X':
                        if x-3<0 or y-2 == 0:
                            column = x+1
                            playerturn(column,'O')
                            break
                        else:
                            column = x-3
                            playerturn(column,'O')
                            break
                    else:
                        print('ln322')
                        
                else:
                    print('ln325')
                    
                    
            if x == x:
                column = random.randint(0,6)
                playerturn(column,'O')
                break

if choice == '2p':
    while True:
        column= int(input('Player 1 enter a column to place your counter in '))
        column = column-1
        playerturn(column, 'X')
        

        column= int(input('Player 2 enter a column to place your counter in '))
        column = column-1
        playerturn(column, 'O')

elif choice == 'ai':
    difficulty = input('do you want hard or easy?(h/e) ')
    difficulty = difficulty.lower()
    if difficulty == 'h':
        while True:
            column = int(input('Player 1 enter a column to place your counter in '))
            column = column-1
            playerturn(column, 'X')
            
            hardAIplayChoice()
            
            
    elif difficulty == 'e':
        while True:
            column = int(input('Player 1 enter a column to place your counter in '))
            column = column-1
            playerturn(column, 'X')
            
            column = random.randint(0,6)
            playerturn(column, 'O')


""" posx = positions[0]
posy = positions[1]

print(board[posy][posx])
print(board[posy-1][posx-1])
print(board[posy-2][posx-2])
print(board[posy-3][posx-3]) """


