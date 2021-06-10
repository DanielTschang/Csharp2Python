import socket
import re
import threading
from ckip_transformers.nlp import CkipWordSegmenter, CkipPosTagger
from Parser_Tree_Utils.parser_util import get_parser_tree_cls , NodeType
import ckip_classic.client
from utils import prepro,parse_tree
msg = '如果是在夜間或其他時後遭到家庭暴力'
text = []
# Initialize drivers with custom checkpoints
ws_driver  = CkipWordSegmenter(level=3, device=0)
pos_driver = CkipPosTagger(level=3, device=0)
ps = ckip_classic.client.CkipParserClient(username='danchang11', password='to26292661')
pt = get_parser_tree_cls(NodeType.Origin_Ckip)


text.append(str(msg))
ws = ws_driver(text)
pos = pos_driver(ws)
parse_input = prepro(ws, pos)
print(parse_input)
ParsTree = parse_tree(ps.apply_list(parse_input)[0])
print("pas",ParsTree)
root = pt.make_tree(ParsTree)
t = pt.list_of_leaves(root)
k = pt.get_keywords(t)
keywords = ""
for word in k:
    keywords += " " + word
print(keywords)