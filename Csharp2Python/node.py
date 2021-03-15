class Node:
    def __init__(self,start):
        self.start = start
        self.children = []
        self.parent = Node
        self.text = ''
        self.type = ''

def make_tree(s):
    stack = []
    nodes = []
    cur = None
    root = None
    parent = None
    flag = 0
    for i, c in enumerate(s):
        if c == '(':
            flag = 0
            cur = Node(i)#（的index是i
            if stack:
                stack[-1].children.append(cur)
                cur.parent = stack[-1]
            stack.append(cur)

            if root is None:
                root = cur

        elif c == ')' and stack:
            topnode = stack.pop()
            text = s[topnode.start + 1: i].split(" ")[1].split("(")[0]
            topnode.text = text


        elif flag == 0 and stack:
            if c == " ":
                flag = 1
                continue

            cur = stack[-1]
            cur.type = cur.type + s[i]


    return root

# list of leaves
def list_of_leaves(node):
    result = []
    for child in node.children:
        result.extend(list_of_leaves(child))
    if not result:
        return [node]

    return result


def inorder(leaf:list):
    phaselist = ['NP']
    tmp = None
    keywords = ''
    for node in leaf:
        parent = node.parent
        if tmp == parent:
            continue
        tmp = parent
        if parent.type in phaselist:
            phase = ''
            for i in parent.children:
                phase = phase + i.text
            keywords = keywords +' '+phase
    return keywords



if __name__ == "__main__":
    s = """\
    (ROOT
      (SQ (VBD Did)
        (NP (NNP Matt))
        (VP (VB win)
          (NP (DT the) (NNS men) (NN slalom)))
        (. ?)))
        """

    t = '''\
    (ROOT
      (CP
        (ADVP (CS 如果))
        (IP
          (VP (VC 是)
            (VP
              (PP (P 在)
                (NP
                  (NP (NN 夜间))
                  (CC 或)
                  (NP
                    (DP (DT 其他))
                    (NP (NN 时候)))))
              (VP (VV 遭到)
                (NP (NN 家庭) (NN 暴力))))))))
    '''

    root = make_tree(t)

    t = list_of_leaves(root)
    k = inorder(t)





