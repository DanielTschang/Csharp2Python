def prepro(ws,pos):
    ans = []
    for i in range(len(ws)):
        st = ''
        for j in range(len(ws[i])):
            st += ws[i][j] + '(' + pos[i][j] + ')' + '　'
        print(st)
        ans.append(st)
    return ans

def parse_tree(l):
    l = '(' + l[9:] + ')'
    l = l.replace("#", "")
    return l
