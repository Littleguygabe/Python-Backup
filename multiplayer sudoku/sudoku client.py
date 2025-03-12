import socket, time, os
from tkinter import *
root = Tk()
root2 = Tk()

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
port=5050
row_array = []
large_labels = []

def connect():
    host = IPentry.get()
    print(host)
    s.connect((host,port))
    root2.destroy()

IPentry = Entry(root)
IPbut = Button(root,text='Enter IP',command = connect)

IPentry.pack(root2)
IPbut.pack(root2)
root2.mainloop()

def generateVisuals():
    for y in range(0,len(board)):
        labels = []
        for x in range(0,len(board[0])):
            if board[y][x] != '':
                labels.append(Label(root,
                                width=5,
                                text= str(board[y][x]),
                                font='Arial'))
                
            else:
                labels.append(Entry(root,
                                    width=5,
                                    font = 'Arial'))    
                        
            labels[x].grid(row = y+1, column = x+1)
        
        large_labels.append(labels)

while True:
    s_msg=s.recv(1024)
    if s_msg.decode() == 'BOARD':
        s_msg = s.recv(1024)
        board = s_msg.decode().split('|')
        for y in range(0,len(board)):
            print(board[y])

        for i in range(0,len(board[0])):
            print(board[0][i])

    if s_msg.decode() == 'FINISHED':
        s_msg = s.recv(1024)
        symbol = s_msg.decode()
        s_msg = s.recv(1024)
        print(symbol, s_msg.decode())
        time.sleep(2)
        quit()

    if s_msg.decode() == 'ANSWERS':
        s_msg=s.recv(1024)
        answersArr = s_msg.decode().split('|')
        for y in range(0,len(answersArr)):
            print(answersArr[y])
    generateVisuals()
    root.mainloop()
