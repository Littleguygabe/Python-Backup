import os

#SEPERATE IF STATEMENT FOR EACH COLUMN

board = [[' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ',' ',' ']]

#posx = 0, posy = 1
positions =[]

finish = False

def player1turn(column):
    os.system('cls')
    if board[0][column] == ' ':
        for i in range(0,5):
            if board[i+1][column] != ' ':
                board[i][column] = 'X'
                posx = column
                posy = i
                positions.clear()
                positions.append(column)
                positions.append(i)
                #print(dropPosx,',',dropPosy)
                playerWinCheck()
                break
                
            elif i+1 == 5:
                positions.clear()
                board[5][column] = 'X'
                positions.append(column)
                positions.append(5)
                playerWinCheck()
    else:
        print('no room in column 1')
        
        
    for i in range(0,6):
        joinedboard = '|'.join(board[i])
        print(joinedboard)

def player2turn(column):
    os.system('cls')
    if board[0][column] == ' ':
        for i in range(0,5):
            if board[i+1][column] != ' ':
                board[i][column] = 'O'
                posx = column
                posy = i
                positions.clear()
                positions.append(column)
                positions.append(i)
                #print(dropPosx,',',dropPosy)
                playerWinCheck()
                break
                
            elif i+1 == 5:
                positions.clear()
                board[5][column] = 'O'
                positions.append(column)
                positions.append(5)
                playerWinCheck()
    else:
        print('no room in column 1')
        
        
    for i in range(0,6):
        joinedboard = '|'.join(board[i])
        print(joinedboard)

def playerWinCheck():
#check horizontal
    finish == False
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
    if posy>=3 and column<=4:
        if board[posy][posx] == board[posy-1][posx+1] and board[posy][posx] == board[posy-2][posx+2] and board[posy][posx] == board[posy-3][posx+3]:
            print('Player Win!')
            print('4 in a row')
            exit()
            
    if posy>=3 and column<=7:
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

while True:
    column= int(input('Player 1 enter a column to place your counter in '))
    column = column-1
    player1turn(column)
    

    column= int(input('Player 2 enter a column to place your counter in '))
    column = column-1
    player2turn(column)




""" posx = positions[0]
posy = positions[1]

print(board[posy][posx])
print(board[posy-1][posx-1])
print(board[posy-2][posx-2])
print(board[posy-3][posx-3]) """


