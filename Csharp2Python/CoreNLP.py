from opencc import OpenCC
from stanza.server import CoreNLPClient
import stanza

t2s_ = OpenCC('t2s')
s2t_ = OpenCC('s2t')

class StanzaClient():
    def __init__(self):
        self.client = CoreNLPClient(annotators=[
            'tokenize',
            'ssplit',
            'pos',
            'lemma',
            'parse',
        ],
                                    timeout=30000,
                                    properties="zh",
                                    output_format="json",
                                    memory='5g')

    def get_parse_tree(self, sent):
        ann = self.client.annotate(sent)
        return ann["sentences"][0]["parse"]

def s2t(string):
    return s2t_.convert(string)

def t2s(string):
    return t2s_.convert(string)

