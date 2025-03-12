import socket, time, os
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host='172.25.10.126'
port=5050
s.connect((host,port))
row_array = []
while True:
    s_msg=s.recv(1024)
    if s_msg.decode() == 'BOARD':
        s_msg = s.recv(1024)
        posArray = s_msg.decode().split('|')
        print('1')
        for i in range(0,len(posArray)):
            print(posArray[i])
            
    if s_msg.decode() == 'FINISHED':
        s_msg = s.recv(1024)
        symbol = s_msg.decode()
        s_msg = s.recv(1024)
        print(symbol, s_msg.decode())
        time.sleep(2)
        quit()
        
    c_msg=input("Place Counter at: ")
    s.send(c_msg.encode())
    print("wating for response")
