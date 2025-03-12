import random, time, os
from tkinter import *
from random import sample
base  = 3
side  = base*base
numberEmpty = 40
difficulty = numberEmpty/(side*side)
large_labels = []
empty_nums = []
empty_pos = []

root = Tk()

# pattern for a baseline valid solution
def pattern(r,c): return (base*(r%base)+r//base+c)%side

# randomize rows, columns and numbers
def shuffle(s): 
    return sample(s,len(s))

rBase = range(base) 
rows  = [g*base + r for g in shuffle(rBase) for r in shuffle(rBase)]
cols  = [g*base + c for g in shuffle(rBase) for c in shuffle(rBase)]
nums  = shuffle(range(1,base*base+1))

def check_board():
    entry_list = []   
    answers = []
    check = []
    count = 0

    print('checking board')

    #check against give
    for y in range(0,len(large_labels)):
        for x in range(0,len(large_labels[y])):
            label = str(large_labels[y][x])
            if label[2] == 'e':
                entry_list.append(large_labels[y][x])
                answers.append(str(solution[y][x]))

    for i in entry_list:
        check.append(i.get())

    for i in range(0,len(answers)):
        if check[i] == answers[i]:
            entry_list[i].config(bg = 'green')

        elif check[i] == 'gabe':
            print(answers)

        else:
            entry_list[i].config(bg = 'red')
            count+=1
        
    if count == 0:
        print('you completed it!')
        time.sleep(1)
        root.quit()
                    
def remove_nums(board):
    global empty_nums, empty_pos 
    empty_squares = int(len(board)*len(board[0])*difficulty)
    for i in range(0,empty_squares):
        x = random.randint(0,side-1)
        y = random.randint(0,side-1)
        while board[y][x] == '':
            x = random.randint(0,side-1)
            y = random.randint(0,side-1)
        board[y][x] = ''
        empty_pos.append(y)
        empty_pos.append(x)

def check_valid(board):
    breakCount = 15
    emptyCount = 0
    count = 0
    possibilities = 1
    numCoordsToCheck = []
    print('validating board')
    for i in range(0,len(empty_pos),2):
        possibleNumbers = []
        tempCoords = []
        for num in range(1,side+1):
            possibleNumbers.append(num)
        y = empty_pos[i]
        x = empty_pos[i+1]
        #check horizontal
        for checkx in range(0,side):
            if board[y][checkx] != '':
                possibleNumbers.remove(board[y][checkx])

        #check vertical
        for checky in range(0,side):
            for i in range(0,len(possibleNumbers)):
                if len(possibleNumbers) == 1:
                    break
                else:
                    if board[checky][x] == possibleNumbers[i-1]:
                        possibleNumbers.remove(board[checky][x])

        #check 3x3
        for boxy in range(0-(y%base),(0-(y%base))+3):
            for boxx in range(0-(x%base),(0-(x%base))+3):

                if board[y+boxy][x+boxx] != '':
                    for i in range(0,len(possibleNumbers)):
                        if possibleNumbers[i-1] == board[y+boxy][x+boxx]:
                            possibleNumbers.remove(board[y+boxy][x+boxx])
                            
        if len(possibleNumbers) > 1:
            #print(len(possibleNumbers))
            print('greater than length of 2')
            numCoordsToCheck.append(possibleNumbers)
            tempCoords.append(y)
            tempCoords.append(x)
            numCoordsToCheck.append(tempCoords)

        elif len(possibleNumbers) == 1:
            print('len --> 1')
            print(board[y][x])
            board[y][x] = possibleNumbers[0]
            for i in range(0,len(board)):
                print(board[i])

        if emptyCount==20:
            break

        for y in range(0,len(board)):
            for x in range(0,len(board)):
                if board[y][x] == '':
                    emptyCount+=1
                    breakCount+=1

        else:
            print('valid solution')
            finish = True

        if emptyCount>=1:
            if breakCount<=20:
                finish = True
    
        possibilities = possibilities*len(possibleNumbers)
        print('possible numbers are -> ',possibleNumbers, 'for -->',y,x)
        print(possibilities, 'current solution(s)')
        print(numCoordsToCheck)
        print('--->')
        count+=1

        if finish == True:
            break

def generate_Board():
    global board, solution, empty_squares,large_labels
    solution = [ [nums[pattern(r,c)] for c in cols] for r in rows ]
    board = [ [nums[pattern(r,c)] for c in cols] for r in rows ]

    remove_nums(board)
    check_valid(board)

    for y in range(0,len(board)):
        labels = []
        for x in range(0,len(board[0])):
            if board[y][x] != '':
                labels.append(Label(root,
                                width=5,
                                height=3,
                                text= str(board[y][x]),
                                font='Arial'))
                
            else:
                labels.append(Entry(root,
                                    width=5,
                                    font = 'Arial'))    
                        
            labels[x].grid(row = y+1, column = x+1)
        
        large_labels.append(labels)
    finished = Button(root,
                        width = 84,
                        height = 5,
                        text = 'Finished',
                        command=check_board)

    newboard = Button(root,
                        width = 84,
                        height = 5,
                        text='New Board',
                        command=generate_Board)

    finished.grid(row=len(board)+1,column = 0,columnspan=10)
    newboard.grid(row=len(board)+2,column=0,columnspan=10)

    labelx = Label(root,text='0')
    labelx1 = Label(root,text='1')
    labelx2 = Label(root,text='2')
    labelx3 = Label(root,text='3')
    labelx4 = Label(root,text='4')
    labelx5 = Label(root,text='5')
    labelx6 = Label(root,text='6')
    labelx7 = Label(root,text='7')
    labelx8 = Label(root,text='8')

    labely = Label(root,text='0')
    labely1 = Label(root,text='1')
    labely2 = Label(root,text='2')
    labely3 = Label(root,text='3')
    labely4 = Label(root,text='4')
    labely5 = Label(root,text='5')
    labely6 = Label(root,text='6')
    labely7 = Label(root,text='7')
    labely8 = Label(root,text='8')

    labelx.grid(row=0,column=1)
    labelx1.grid(row=0,column=2)
    labelx2.grid(row=0,column=3)
    labelx3.grid(row=0,column=4)
    labelx4.grid(row=0,column=5)
    labelx5.grid(row=0,column=6)
    labelx6.grid(row=0,column=7)
    labelx7.grid(row=0,column=8)
    labelx8.grid(row=0,column=9)

    labely.grid(row=1,column=0)
    labely1.grid(row=2,column=0)
    labely2.grid(row=3,column=0)
    labely3.grid(row=4,column=0)
    labely4.grid(row=5,column=0)
    labely5.grid(row=6,column=0)
    labely6.grid(row=7,column=0)
    labely7.grid(row=8,column=0)
    labely8.grid(row=9,column=0)

os.system('cls')
generate_Board()
root.mainloop()

