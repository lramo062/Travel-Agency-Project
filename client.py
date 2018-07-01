
import socket

# define socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# define server
server = 'localhost'
port = 10000

s.connect((server,port))
request = input('''
Welcome to our Travel Agency, here are your available options: 
\nLIST\nSEARCHD [DEST]\nSEARCHDEPARTURE [DEP]\nSEARCHALL [DEST]
BUY_TICKET [ROUTE] [SEATS]\nBUYRT_TICKET [ROUTE] [SEATS]
RETURN_TICKET [ROUTE] [SEATS]\nRETURNRT_TICKET [ROUTE] [SEATS]\nQUIT\n\n:''')

while request:
    if "QUIT" in request:
        print("GOODBYE!")
        break
    s.send(request.encode())
    print(s.recv(2048).decode())
    request = input(":")

s.close()
