from os.path import dirname, abspath, join
import sys

THIS_DIR = dirname(__file__)
WORDS_DIR = abspath(join(THIS_DIR, '..', 'cn_stopwords.txt'))

fs = open(WORDS_DIR, encoding="utf-8")
stopwords = fs.read()
stopwords = stopwords.split("\n")

class Node:
    def __init__(self,start):
        self.start = start
        self.children = []
        self.parent = Node
        self.text = ''
        self.type = ''
        self.semantic_role = ''
        self.raw_type = ''

class ParserTree:
    def __init__(self, list_root_node = False):
        self.list_root_node = list_root_node
        self.root = None
        self.leaves = []
        self.keywords = set()

    def list_of_leaves(self, node):
        result = []
        for child in node.children:
            result.extend(self.list_of_leaves(child))
        if not result:
            return [node]

        return result

    def get_keywords(self, leaf:list):
        phaselist = ['NP','VP']
        for node in leaf:
            self.inorder(node, phaselist)
        if not self.keywords and self.list_root_node:
            if leaf[0].type != None and leaf[0].type in phaselist:
                self.keywords.append(leaf[0].text)
        return self.keywords

    def inorder(self, node, phaselist):
        parent = node.parent
        if not parent == self.root and parent.type in phaselist:
            phase = ''
            for i in parent.children:
                phase = phase + i.text
            if len(phase)>1 and phase not in stopwords:
                self.keywords.add(phase)
        elif not parent == self.root:
            self.inorder(node=parent, phaselist=phaselist)

    def clear(self):
        self.root = None
        self.leaves = []
        self.keywords = set()


