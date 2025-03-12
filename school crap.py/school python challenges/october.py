import random
player1 = [4,4,4,4,5]
player2 = []
player3 = []

""" for i in range(0,5):
    cardnum = random.randint(2,14)
    player1.append(cardnum) """
for i in range(0,5):
    cardnum = random.randint(1,13)
    player2.append(cardnum)
for i in range(0,5):
    cardnum = random.randint(1,13)
    player3.append(cardnum)
for i in range(0,5):
    cardnum = random.randint(1,13)
    player1.append(cardnum)
    
royalstart = 10
straightstart = 7
count = 0
for i in range(0,5):
    if player1[i] == royalstart:
        count = count+1
    royalstart=royalstart+1
    
if count == 5:
    print('royal')
    
count = 0
for i in range(0,5):
    if player1[i] == straightstart:
        count = count+1
    straightstart=straightstart+1
    
if count == 5:
    print('straight')
    
count = 0

if player1[0] == player1[1] and player1[0] == player1[2] and player1[0] == player1[3]:
    print('four of a kind')
    
elif player1[0] == player1[1] and player1[0] == player1[2] and player1[0] == player1[4]:
    print('four of a kind')
    
elif player1[0] == player1[1] and player1[0] == player1[3] and player1[0] == player1[4]:
    print('four of a kind')

elif player1[0] == player1[2] and player1[0] == player1[3] and player1[0] == player1[4]:
    print('four of a kind')
    
for i in range(0,5):
    
    for i in range(0,5):
    