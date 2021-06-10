# -*- coding: UTF-8 -*-
from parser_util import get_parser_tree_cls
from parser_util import NodeType


if __name__ == "__main__":
    # Simple test
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
    print('---test Simple Mode---')
    pt = get_parser_tree_cls(NodeType.Simple)
    root = pt.make_tree(t)
    t = pt.list_of_leaves(root)
    k = pt.get_keywords(t)
    print(k)

    t = 'S(agent:NP(property:NP•的(head:NP(property:Nba:Outlook|property:Nad:主旨|Head:Nab:欄位字)|Head:DE:的)|Head:Nac:顏色)|reason:Dj:怎麼|Head:VC2:調整)'

    print('---test Origin Ckip Mode---')
    pt = get_parser_tree_cls(NodeType.Origin_Ckip)
    root = pt.make_tree(t)
    t = pt.list_of_leaves(root)
    k = pt.get_keywords(t)
    pt.clear()
    print(k)

    t = 'VP(reason:Dj:怎麼|theme:PP(Head:P07:將|DUMMY:NP(quantifier:DM:一個|property:NP•的(head:NP(property:Nba:PTT|Head:Nab:檔)|Head:DE:的)|Head:Nac:字型))|theme:Neqa:全部|manner:Dh:一起|Head:VC31:設定)'
    root = pt.make_tree(t)
    t = pt.list_of_leaves(root)
    k = pt.get_keywords(t)
    print(k)