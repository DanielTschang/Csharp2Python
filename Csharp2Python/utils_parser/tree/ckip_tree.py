from parser_tree import Node
from parser_tree import ParserTree
import re

class CkipTree(ParserTree):
    def make_tree(self, s):
        # s = '('+s+')'
        match_pattern = '(.*):(.*):(.*)'
        stack = []
        cur = None
        flag = 0
        inx = 0
        root = None
        while(inx < len(s)):

            if s[inx] == '(':
                flag = 0
                cur = Node(inx)# '(' 的index是inx

                #backward for type
                tmp = inx-1
                while tmp >=0:
                    if s[tmp] == ':':
                        break
                    cur.type = s[tmp]+cur.type
                    tmp -= 1
                #backward for semantic role
                stop_chars = ['(',')','|']
                while tmp >= 0:
                    if s[tmp] in stop_chars:
                        break
                    cur.semantic_role = s[tmp]+cur.semantic_role
                    tmp -= 1

                if stack:
                    stack[-1].children.append(cur)
                    cur.parent = stack[-1]
                stack.append(cur)

                if self.root is None:
                    self.root = cur

            elif s[inx] == ')' and stack:
                topnode = stack.pop()
                tmp_text = topnode.text
                # print(tmp_text)
                split_text = tmp_text.split('|')
                for t in split_text:
                    if re.match(match_pattern, t):
                        tmp_node = Node(-1)
                        search_obj = re.search(match_pattern, t)
                        tmp_node.semantic_role = search_obj.group(1)
                        tmp_node.type = search_obj.group(2)
                        tmp_node.text = search_obj.group(3)
                        topnode.children.append(tmp_node)
                        tmp_node.parent = topnode
                if len(topnode.children) > 0:
                    topnode.text = ''
                if stack:
                    cur = stack[-1]
            elif not cur == None:
                cur.text += s[inx]

            inx += 1

        return self.root