from parser_tree import Node
from parser_tree import ParserTree

class SimpleTree(ParserTree):
    def make_tree(self, s):
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

                if self.root is None:
                    self.root = cur

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

        return self.root