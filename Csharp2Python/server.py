import socket
import time
import threading
from node import *
from CoreNLP import *

HEADER = 1024
PORT = 9527
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER,PORT)
FORMAT = 'utf-8'
DISCONNECT_MSG = '!DISCONNECT!'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn,addr):
    print(f'[NEW CONNECTION] {addr} connected.')

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)

            if msg == DISCONNECT_MSG:
                connected = False
                break
            print(f"[{addr}] : {msg}")

            ParsTree = CoreN.get_parse_tree(msg)
            NodeTree = make_tree(ParsTree)
            Leaves = list_of_leaves(NodeTree)
            keywords = inorder(Leaves)

        conn.send(keywords.encode(FORMAT))

    conn.close()

def start():
    server.listen()
    print(f"[SERVER IS LISTENINGP {SERVER}:{PORT}]")
    while True:
        conn, addr =server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS:{threading.activeCount() -1}]")

if __name__ =='__main__':
    print("[STARTING SERVER]")
    CoreN = StanzaClient()
    sentence = t2s('初始化')
    t = CoreN.get_parse_tree(sent=sentence)

    print("[SERVER STRATED]")
    start()

