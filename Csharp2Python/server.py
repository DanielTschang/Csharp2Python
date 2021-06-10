import socket
import re
import threading
from ckip_transformers.nlp import CkipWordSegmenter, CkipPosTagger
from utils_parser.parser_util import get_parser_tree_cls , NodeType
import ckip_classic.client
from utils import prepro, parse_tree


# Initialize drivers with custom checkpoints
ws_driver  = CkipWordSegmenter(level=3, device=0)
pos_driver = CkipPosTagger(level=3, device=0)
ps = ckip_classic.client.CkipParserClient(username='danchang11', password='to26292661')
pt = get_parser_tree_cls(NodeType.Origin_Ckip)

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
        text = []
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            print(f"msgl = {msg_length}")
            msg = conn.recv(msg_length).decode(FORMAT)

            if msg == DISCONNECT_MSG:
                connected = False
                break
            print(f"[{addr}] : {msg}")

            text.append(str(msg))
            ws = ws_driver(text)
            pos = pos_driver(ws)
            parse_input = prepro(ws,pos)
            ParsTree = parse_tree(ps.apply_list(parse_input)[0])
            root = pt.make_tree(ParsTree)

            t = pt.list_of_leaves(root)
            k = pt.getkeywords(t)
            keywords = ""
            for word in k:
                keywords += " " + word


            # ParsTree = CoreN.get_parse_tree(t2s(msg))
            # NodeTree = make_tree(ParsTree)
            # Leaves = list_of_leaves(NodeTree)
            # keywords = inorder(Leaves)
            # keywords = s2t(keywords)

            if(keywords == ""):
                keywords = "None"
                print(keywords)

        conn.send(keywords.encode(FORMAT))
    conn.close()

def punc_del(s):
    return re.sub(r'[^\w\s]', '', s)
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

    print("[SERVER STARTED]")
    start()

