import sys
import socket
import select

'''Creating socket and connecting by intaking ip address, port'''

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   
IP_addr = str(sys.argv[1])
port = int(sys.argv[2])            
s.connect((IP_addr, port))

'''allows server to detect the first one to press the buzzer within 10 seconds'''

while True:

    sockets_list = [sys.stdin, s]

    i,j,e = select.select(sockets_list,[],[],10)      

    for sockets in i:
        if sockets == s:
            msg = sockets.recv(2048)                     
            print msg
        else:
            msg = sys.stdin.readline()
            s.send(msg)                                 
            sys.stdout.flush()

s.close()
sys.exit()
