import socket
import threading
import time
import sys

# Let us define constant parameters
MAX_LEN = 64
PORT = 9001
SERVER = "127.0.0.1"
ADDR = (SERVER,PORT)
FORMAT = "utf-8"
DISCONNECT_MSG = "!END"

# Global variables
client_list = []
client_names = []

# Create server socket
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(ADDR)

# handle client
def handle_client(conn,addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    # receive username
    username = conn.recv(1024).decode(FORMAT)
    print(username)
    indx = client_list.index(conn)
    client_names[indx] = username

    # send wlcm message
    broadcast_wlcm(conn)

    connected = 1
    while connected:
        # receive message from client
        msg = conn.recv(4096).decode(FORMAT)
        print(msg)
        if(msg == DISCONNECT_MSG):
            closeConnection(conn)
            sys.exit()
        else:
            broadcast(msg,conn)

def closeConnection(conn):
    indx = client_list.index(conn)
    sender = client_names[indx]
    msg = "************ " + sender + " has left the chat. **************"
    for clients in client_list:
        if(clients != conn):
            clients.send(msg.encode(FORMAT))
    client_list.pop(indx)
    client_names.pop(indx)
    conn.close()

def broadcast_wlcm(conn):
    sender = client_names[client_list.index(conn)]
    conn_msg = "************* You have joined the chat. *****************"
    rest_msg = "************ " + sender + " has joined the chat. **************"
    for clients in client_list:
        if(clients == conn):
            clients.send(conn_msg.encode(FORMAT))
        else:
            clients.send(rest_msg.encode(FORMAT))

def broadcast(message,conn):
    # get message time and sender name
    msg_time = time.localtime()
    current_time = time.strftime("%H:%M:%S", msg_time)
    sender = client_names[client_list.index(conn)]
    formatted_msg = "["+current_time +"]" + " " + sender + ": "+ message  
    for clients in client_list:
        clients.send(formatted_msg.encode(FORMAT))


# start server
def init_server():
    # start listening
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn,addr = server.accept()         
        client_list.append(conn)
        client_names.append("player")
        thread = threading.Thread(target=handle_client,args=(conn,addr))
        thread.start()

    server.close()

init_server()