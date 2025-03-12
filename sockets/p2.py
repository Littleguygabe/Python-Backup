import socket
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host=socket.gethostname()
port=5050
s.connect((host,port))
while True:
    s_msg=s.recv(1024)
    if s_msg.decode() == 'BOARD':
        for row in range(0,3):
            row_array = []
            for column in range(0,3):
                s_msg=s.recv(1024)
                row_array.append(s_msg.decode())
            print(row_array)
    c_msg=input("Place Counter at: ")
    s.send(c_msg.encode())
    print("wating for response")