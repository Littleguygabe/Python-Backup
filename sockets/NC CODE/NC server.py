import socket,os,time
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
board=[['1','2','3'],
        ['4','5','6'],
        ['7','8','9']]

host=socket.gethostname()
port=5050
ADDR = (host,port)
count2 = 0

s.bind(ADDR)
s.listen()

print("connected on",socket.gethostbyname(socket.gethostname()))

con,addr=s.accept()

print(addr,'connected')

def sendboard():
    socketArr = ''

    con.send('BOARD'.encode())

    for pos in board:
        socketArr = socketArr + str(pos) + '|'

    con.send(socketArr.encode())

def CounterPlace(pos,symbol):
    for y in range(0,len(board)):
        for x in range(0,len(board[y])):
            if board[y][x] == pos:
                board[y][x] = symbol
                
            checkWin(symbol)

for i in range(0,len(board)):
        print(board[i])

def announceWin(symbol):
    print(symbol,'is the Winner!')
    con.send('FINISHED'.encode())
    con.send(symbol.encode())
    con.send(' is the Winner!'.encode())
    time.sleep(2)
    quit()

def checkWin(symbol):
    global count2

    for checky in range(0,3):
        if board[checky][0] == board[checky][1] and board[checky][0] == board[checky][2]:
            announceWin(symbol)

    for checkx in range(0,3):
        if board[0][checkx]==board[1][checkx] and board[0][checkx]==board[2][checkx]:
            announceWin(symbol)

    if board[0][0] == board[1][1] and board[0][0]==board[2][2] or board[0][2] == board[1][1] and board[0][2] == board[2][0]:
        announceWin(symbol)


while True:
    msg=input("Place Counter at: ")

    CounterPlace(msg,'X')
    os.system('cls')
    for i in range(0,len(board)):
        print(board[i])


    count2+=1
    if count2==9:
        announceWin('no-one')

    sendboard()
    print("Waiting For Next Move")
    c_msg=con.recv(1024)
    CounterPlace(c_msg.decode(),'O')

    count2+=1
    if count2==9:
        announceWin('no-one')

    for i in range(0,len(board)):
        print(board[i])
