from os.path import dirname, abspath, join
import sys
# Find code directory relative to our directory
THIS_DIR = dirname(__file__)
TREE_DIR = abspath(join(THIS_DIR, 'tree'))
sys.path.append(TREE_DIR)

# use abs directory to import module
import importlib.util
simple_tree_spec = importlib.util.spec_from_file_location("module.name", abspath(join(TREE_DIR, 'simple_tree.py')))
simple_tree = importlib.util.module_from_spec(simple_tree_spec)
simple_tree_spec.loader.exec_module(simple_tree)
SimpleTree = simple_tree.SimpleTree

ckip_tree_spec = importlib.util.spec_from_file_location("module.name", abspath(join(TREE_DIR, 'ckip_tree.py')))
ckip_tree = importlib.util.module_from_spec(ckip_tree_spec)
ckip_tree_spec.loader.exec_module(ckip_tree)
CkipTree = ckip_tree.CkipTree

# from tree.simple_tree import SimpleTree
# from tree.ckip_tree import CkipTree
from enum import Enum
from enum import auto

class NodeType(Enum):
    Simple = auto()
    Origin_Ckip = auto()

def get_parser_tree_cls(node_type, list_root_node = False):
    if not isinstance(node_type, NodeType):
        raise TypeError('node_type must be an instance of NodeType Enum')
    if node_type == NodeType.Simple:
        return SimpleTree(list_root_node)
    elif node_type == NodeType.Origin_Ckip:
        return CkipTree(list_root_node)