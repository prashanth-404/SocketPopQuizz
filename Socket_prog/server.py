import sys
import time
import random
import socket
import select
from thread import *

'''The Below Lists contain Questions and their answers in an ordered way and random questions are picked each time using randint generator in the random module'''

Q = ["What is Starbucks famous for? \n\na.Mozarella\nb.Pasty\nc.Patty\nd.Soft-Drinks and Smoothies\n",
     "What instrument is used to measure a thermometer?\n\na.Barometer\nb.Thermometer\nc.Magic Wand\nd.Aerometer\n",
     "What is the capital of India?\n\na.Apollo\nb.Delhi\nc.Kyoto\nd.Bakaboom\n",
     "Where is Taj Mahal?\n\na.Agra \nb.Nellore \nc.IIITB \nd.Pakistan\n",
     "Who is known to be the father of India?\n\na.Hitler \nb.Baba Ramdev \nc.Arun Jetley \nd.Gandhi\n",
     "Which is the first Indian film?\n\na.Harischandra \nb.Titanic \nc.Gully boys \nd.James Bond\n",
     "Name the first satellite launched by india?\n\na.Kurzekatz \nb.Aryabhatta \nc.Pablo Escobar \nd.Kali\n",
     "Which is the largest animal in the world ?\n\na.Blue Whale \nb.Elephants \nc.Octopops \nd.Homo sapiens\n",
     "Which is the fastest bird ?\n\na.Pigeon \nb.Hummingbird \nc.Swift \nd.Peacock\n",
     "Which is the biggest continent in the world ?\n\na.Asia \nb.Australia \nc.South Africa \nd.Antarctica\n",
     "Which is the largest country (area) in the world ?\n\na.India \nb.China \nc.New Zealand \nd.Russia\n",
     "Which is the most spoken language in the world ?\n\na.Chinese \nb.Hindi \nc.Japanese \nd.Kili-kili\n",
     "Which is the largest island in the world ?\n\na.Greenland \nb.Madagascar \nc.Lakhadweep \nd.Bermuda triangle\n",
     "Which place is known as tea garden of India?\n\na.IIITB canteen \nb.Modiji's tea stall \nc.Starbucks \nd.Assam\n",
     "Water boils at 212 Units at which scale? \n\na.Fahrenheit \nb.Celsius \nc.Rankine \nd.Kelvin\n",
     "Which sea creature has three hearts? \n\na.Dolphin \nb.Octopus \nc.Walrus \nd.Seal\n",
     "Who was the character famous in our childhood rhymes associated with a lamb? \n\na.Mary \nb.Jack \nc.Johnny \nd.Mukesh\n",
     "How many balls does an over consist of in cricket? \n\na.4 \nb.6 \nc.5 \nd.9\n",
     "How many members are in the secret seven gang? \n\na.7 \nb.8 \nc.10 \nd.4\n",
     "What element does not exist?\n \na.Xf \nb.Re \nc.Si \nd.Pa\n",
     "How many states are there in India? \n\na.24 \nb.29 \nc.30 \nd.31\n",
     "Who invented the telephone? \n\na.A.G Bell \nb.John Wick \nc.Thomas Edison \nd.G Marconi\n",
     "Who is Loki? \n\na.God of Thunder \nb.God of Dwarves \nc.God of Mischief \nd.God of Gods\n",
     "Who was the first Indian female astronaut ? \n\na.Sunita Williams \nb.Kalpana Chawla \nc.None of them \nd.Both of them \n",
     "What is the smallest continent?\n \na.Asia \nb.Antarctic \nc.Africa \nd.Australia\n",
     "The beaver is the national embelem of which country?\n \na.Zimbabwe \nb.Iceland \nc.Argentina \nd.Canada\n",
     "How many players are on the field in baseball?\n \na.6 \nb.7 \nc.9 \nd.8\n",
     "Hg stands for? \n\na.Mercury \nb.Hulgerium \nc.Argenine \nd.Halfnium\n",     
     "Which planet is Farthest to the sun? \n\na.Mercury \nb.Pluto \nc.Earth \nd.Venus\n"]

A = ['d','b', 'b', 'a', 'd', 'a', 'b', 'a', 'c', 'a', 'd', 'a', 'a', 'd', 'a', 'b', 'a', 'a', 'a', 'a', 'b', 'a', 'c', 'b', 'd', 'd', 'c', 'a', 'b']

'''Server socket is created and is setup to take client side connections'''

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
IP_address = str(sys.argv[1])
Port = int(sys.argv[2])


s.bind((IP_address, Port))
s.listen(4)


list_of_clients=[]       
Count=[]                  
client = ["address",-1]
buzzer =[0, 0, 0]


'''a simple function to send message to all the clients'''

def send_msg(message):
    for clients in list_of_clients:
            clients.send(message)


'''a function to throw randomly generated questions at the participents and send it to them'''

def quiz():
    buzzer[2] = random.randint(0,1000)%len(Q)
    if len(Q) != 0:
        for connection in list_of_clients:
            connection.send(Q[buzzer[2]])


'''This function receives answers from clients and increases/reduces their marks according to the validity of the answer, also calls end_quiz() when any one of termination conditions are met'''

def client_thread(conn, addr):
    conn.send('Welcome to the Game Show !\n\nOnly the first one to press the buzzer within 10 seconds is allowed to answer the question,\nIf the answer is correct the participent will be awarded a point, if the answer turns out to be wrong, half a mark will be deducted from his total points...\nThe first one to get 5 points, WINS the game!\n\n\n\t\t Let us start the GAME!!! \n\n')
    time.sleep(0.5)
    while True:
            message = conn.recv(2048)
            if message:
                if buzzer[0]==0:
                    client[0] = conn
                    buzzer[0] = 1
                    i = 0
                    while i < len(list_of_clients):
                            if list_of_clients[i] == client[0]:
                                break
                            i +=1
                    client[1] = i

                elif buzzer[0] ==1 and conn==client[0]:
                        bol = message[0] == A[buzzer[2]][0]
                        print A[buzzer[2]][0]
                        if bol:                           
                            Count[i] += 1
                            if Count[i]==5:
                                send_msg("Player" + str(client[1]+1) + " WON !!!" + "\n")
                                end_quiz()
                                sys.exit()

                        else:                            
                            Count[i] -= 0.5
                        buzzer[0]=0
                        if len(Q) != 0:
                            Q.pop(buzzer[2])
                            A.pop(buzzer[2])
                        if len(Q)==0:
                            end_quiz()
                        quiz()

                else:
                        conn.send("Player " + str(client[1]+1) + " pressed buzzer first\n\n")
            else:
                if connection in list_of_clients:
                	list_of_clients.remove(connection)



'''A function to end the quiz when any one of end termination conditions are met'''

def end_quiz():
        send_msg("Game Over !\n")
        buzzer[1]=1
        i = Count.index(max(Count))
        send_msg("Player " + str(i+1)+ " Wins by scoring "+str(Count[i])+" points. The participents are now requested to exit the game and leave their seats (or press Ctrl + Z)")
        s.close()


'''Used to listen to new connections and register them by appending their details into list _of_clients and starts quiz when 3 participents join the game'''

while True:
    conn, addr = s.accept()
    list_of_clients.append(conn)
    Count.append(0)
    print addr[0] + " is now connected"
    start_new_thread(client_thread,(conn,addr))     
    if(len(list_of_clients)==3):
        quiz()


conn.close()
s.close()





