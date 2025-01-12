import pytest
from tree_is_up.tree import Tree, NodeIDAbsentError, LoopError
from tree_is_up.node import Node


@pytest.fixture
def tree():
    t = Tree(identifier="tree 1")
    t.create_node("Harry", "harry")
    t.create_node("Jane", "jane", parent="harry")
    t.create_node("Bill", "bill", parent="harry")
    t.create_node("Diane", "diane", parent="jane")
    t.create_node("George", "george", parent="bill")
    return t


@pytest.fixture
def input_dict():
    return {
        "Bill": "Harry",
        "Jane": "Harry",
        "Harry": None,
        "Diane": "Jane",
        "Mark": "Jane",
        "Mary": "Harry",
    }


@pytest.fixture
def t1():
    t = Tree(identifier="t1")
    t.create_node(tag="root", identifier="r")
    t.create_node(tag="A", identifier="a", parent="r")
    t.create_node(tag="B", identifier="b", parent="r")
    t.create_node(tag="A1", identifier="a1", parent="a")
    return t


@pytest.fixture
def t2():
    t = Tree(identifier="t2")
    t.create_node(tag="root2", identifier="r2")
    t.create_node(tag="C", identifier="c", parent="r2")
    t.create_node(tag="D", identifier="d", parent="r2")
    t.create_node(tag="D1", identifier="d1", parent="d")
    return t


def test_tree(tree):
    assert isinstance(tree, Tree)
    copy_tree = Tree(tree, deep=True)
    assert isinstance(copy_tree, Tree)


def test_is_root(tree):
    assert tree._nodes["harry"].is_root()
    assert not tree._nodes["jane"].is_root()


def test_tree_wise_is_root(tree):
    subtree = tree.subtree("jane", identifier="subtree 2")
    assert tree._nodes["harry"].is_root("tree 1")
    assert "harry" not in subtree._nodes
    assert not tree._nodes["jane"].is_root("tree 1")
    assert subtree._nodes["jane"].is_root("subtree 2")


def test_paths_to_leaves(tree):
    paths = tree.paths_to_leaves()
    assert len(paths) == 2
    assert ["harry", "jane", "diane"] in paths
    assert ["harry", "bill", "george"] in paths


def test_nodes(tree):
    assert len(tree.nodes) == 5
    assert len(tree.all_nodes()) == 5
    assert tree.size() == 5
    assert tree.get_node("jane").tag == "Jane"
    assert tree.contains("jane")
    assert "jane" in tree
    assert not tree.contains("alien")
    tree.create_node("Alien", "alien", parent="jane")
    assert tree.contains("alien")


def test_getitem(tree):
    for node_id in tree.nodes:
        try:
            tree[node_id]
        except NodeIDAbsentError:
            pytest.fail("Node acces should be possible via getitem.")
        try:
            tree["root"]
        except NodeIDAbsentError:
            pass
        else:
            pytest.fail("There should be no default fallback value for getitem")


def test_parent(tree):
    for nid in tree.nodes:
        if nid == tree.root:
            assert tree.parent(nid) is None
        else:
            assert tree.parent(nid) in tree.all_nodes()


def test_ancestor(tree):
    for nid in tree.nodes:
        if nid == tree.root:
            assert tree.ancestor(nid) is None
        else:
            for level in range(tree.level(nid) - 1, 0, -1):
                assert tree.ancestor(nid, level=level) in tree.all_nodes()


def test_children(tree):
    for nid in tree.nodes:
        children = tree.is_branch(nid)
        for child in children:
            assert tree[child] in tree.all_nodes()
        children = tree.children(nid)
        for child in children:
            assert child in tree.all_nodes()

    tree.create_node("Alien", "alien", parent="jane")
    tree.remove_node("alien")
    try:
        tree.is_branch("alien")
    except NodeIDAbsentError:
        pass
    else:
        pytest.fail("The absent node should be declaimed")


def test_remove_node(tree):
    tree.create_node("Jill", "jill", parent="george")
    tree.create_node("Mark", "mark", parent="jill")
    assert tree.remove_node("jill") == 2
    assert tree.get_node("jill") is None
    assert tree.get_node("mark") is None


def test_tree_wise_depth(tree):
    assert tree.depth() == 2
    tree.create_node("Jill", "jill", parent="george")
    assert tree.depth() == 3
    tree.create_node("Mark", "mark", parent="jill")
    assert tree.depth() == 4

    assert tree.depth(tree.get_node("mark")) == 4
    assert tree.depth(tree.get_node("jill")) == 3
    assert tree.depth(tree.get_node("george")) == 2
    assert tree.depth("jane") == 1
    assert tree.depth("bill") == 1
    assert tree.depth("harry") == 0

    node = Node("Test One", "identifier 1")
    with pytest.raises(NodeIDAbsentError):
        tree.depth(node)


def test_leaves(tree):
    leaves = tree.leaves()
    for nid in tree.expand_tree():
        assert tree[nid].is_leaf() == (tree[nid] in leaves)
    leaves = tree.leaves(nid="jane")
    for nid in tree.expand_tree(nid="jane"):
        assert tree[nid].is_leaf() == (tree[nid] in leaves)


def test_tree_wise_leaves(tree):
    leaves = tree.leaves()
    for nid in tree.expand_tree():
        assert tree[nid].is_leaf("tree 1") == (tree[nid] in leaves)
    leaves = tree.leaves(nid="jane")
    for nid in tree.expand_tree(nid="jane"):
        assert tree[nid].is_leaf("tree 1") == (tree[nid] in leaves)


def test_link_past_node(tree):
    tree.create_node("Jill", "jill", parent="harry")
    tree.create_node("Mark", "mark", parent="jill")
    assert "mark" not in tree.is_branch("harry")
    tree.link_past_node("jill")
    assert "mark" in tree.is_branch("harry")


def test_expand_tree(tree):
    # Traverse in depth first mode preserving insertion order
    nodes = [nid for nid in tree.expand_tree(sorting=False)]
    assert nodes == ["harry", "jane", "diane", "bill", "george"]
    assert len(nodes) == 5

    # By default traverse depth first and sort child nodes by node tag
    nodes = [nid for nid in tree.expand_tree()]
    assert nodes == ["harry", "bill", "george", "jane", "diane"]
    assert len(nodes) == 5

    # expanding from specific node
    nodes = [nid for nid in tree.expand_tree(nid="bill")]
    assert nodes == ["bill", "george"]
    assert len(nodes) == 2

    # changing into width mode preserving insertion order
    nodes = [nid for nid in tree.expand_tree(mode=Tree.WIDTH, sorting=False)]
    assert nodes == ["harry", "jane", "bill", "diane", "george"]
    assert len(nodes) == 5

    # Breadth first mode, child nodes sorting by tag
    nodes = [nid for nid in tree.expand_tree(mode=Tree.WIDTH)]
    assert nodes == ["harry", "bill", "jane", "george", "diane"]
    assert len(nodes) == 5

    # expanding by filters
    # Stops at root
    nodes = [nid for nid in tree.expand_tree(filter=lambda x: x.tag == "Bill")]
    assert len(nodes) == 0
    nodes = [nid for nid in tree.expand_tree(filter=lambda x: x.tag != "Bill")]
    assert nodes == ["harry", "jane", "diane"]
    assert len(nodes) == 3


def test_move_node(tree):
    tree.move_node("diane", "bill")
    assert "diane" in tree.is_branch("bill")


def test_paste_tree(tree):
    new_tree = Tree()
    new_tree.create_node("Jill", "jill")
    new_tree.create_node("Mark", "mark", parent="jill")
    tree.paste("jane", new_tree)
    assert "jill" in tree.is_branch("jane")
    tree.remove_node("jill")
    assert "jill" not in tree.nodes.keys()
    assert "mark" not in tree.nodes.keys()


def test_merge_on_empty(t2):
    # merge on empty initial tree
    t = Tree(identifier="t1")
    t.merge(nid=None, new_tree=t2)

    assert t.identifier == "t1"
    assert t.root == "r2"
    assert set(t._nodes.keys()) == {"r2", "c", "d", "d1"}


def test_merge_on_new_empty(t1):
    # merge empty new_tree (on root)
    t = Tree(identifier="t2")
    t1.merge(nid="r", new_tree=t)

    assert t1.identifier == "t1"
    assert t1.root == "r"
    assert set(t1._nodes.keys()) == {"r", "a", "a1", "b"}


def test_merge_at_root(t1, t2):
    # merge at root
    t1.merge(nid="r", new_tree=t2)

    assert t1.identifier == "t1"
    assert t1.root == "r"
    assert "r2" not in t1._nodes.keys()
    assert set(t1._nodes.keys()) == {"r", "a", "a1", "b", "c", "d", "d1"}


def test_merge_on_node(t1, t2):
    # merge on node
    t1.merge(nid="b", new_tree=t2)
    assert t1.identifier == "t1"
    assert t1.root == "r"
    assert "r2" not in t1._nodes.keys()
    assert set(t1._nodes.keys()) == {"r", "a", "a1", "b", "c", "d", "d1"}


def test_paste_under_root(t1, t2):
    # paste under root
    t1.paste(nid="r", new_tree=t2)
    assert t1.identifier == "t1"
    assert t1.root == "r"
    assert t1.parent("r2").identifier == "r"
    assert set(t1._nodes.keys()) == {"r", "r2", "a", "a1", "b", "c", "d", "d1"}


def test_paste_under_non_existing_node(t1, t2):
    # paste under non-existing node
    with pytest.raises(NodeIDAbsentError) as e:
        t1.paste(nid="not_existing", new_tree=t2)
    assert e.exception.args[0] == "Node 'not_existing' is not in the tree"


def test_paste_under_none_nid(t1, t2):
    # paste under None nid
    with pytest.raises(ValueError) as e:
        t1.paste(nid=None, new_tree=t2)
    assert e.exception.args[0] == 'Must define "nid" under which new tree is pasted.'


def test_paste_under_node(t1, t2):
    # paste under node
    t1.paste(nid="b", new_tree=t2)
    assert t1.identifier == "t1"
    assert t1.root == "r"
    assert t1.parent("b").identifier == "r"
    assert set(t1._nodes.keys()) == {"r", "a", "a1", "b", "c", "d", "d1", "r2"}


def test_paste_empty_new_tree_under_root(t1):
    # paste empty new_tree (under root)
    t2 = Tree(identifier="t2")
    t1.paste(nid="r", new_tree=t2)

    assert t1.identifier == "t1"
    assert t1.root == "r"
    assert set(t1._nodes.keys()) == {"r", "a", "a1", "b"}


def test_rsearch(tree):
    for nid in ["harry", "jane", "diane"]:
        assert nid in tree.rsearch("diane")


def test_subtree(tree):
    subtree_copy = Tree(tree.subtree("jane"), deep=True)
    assert subtree_copy.parent("jane") is None
    subtree_copy["jane"].tag = "Sweeti"
    assert tree["jane"].tag == "Jane"
    assert subtree_copy.level("diane") == 1
    assert subtree_copy.level("jane") == 0
    assert tree.level("jane") == 1


def test_remove_subtree(tree):
    tree.remove_subtree("jane")
    assert "jane" not in tree.is_branch("harry")


def test_remove_subtree_whole_tree(tree):
    tree.remove_subtree("harry")
    assert tree.root is None
    assert len(tree.nodes.keys()) == 0


def test_to_json(tree):
    tree.to_json()
    tree.to_json(True)


def test_siblings(tree):
    assert len(tree.siblings("harry")) == 0
    assert tree.siblings("jane")[0].identifier == "bill"


def test_tree_data(tree):
    class Flower(object):
        def __init__(self, color):
            self.color = color

    tree.create_node("Jill", "jill", parent="jane", data=Flower("white"))
    assert tree["jill"].data.color == "white"


def test_level(tree):
    assert tree.level("harry") == 0
    depth = tree.depth()
    assert tree.level("diane") == depth
    assert tree.level("diane", lambda x: x.identifier != "jane") == depth - 1


def test_size(tree):
    assert tree.size(level=2) == 2
    assert tree.size(level=1) == 2
    assert tree.size(level=0) == 1


def test_all_nodes_itr():
    """
    tests: Tree.all_nodes_iter
    Added by: William Rusnack
    """
    new_tree = Tree()
    assert len(new_tree.all_nodes_itr()) == 0
    nodes = list()
    nodes.append(new_tree.create_node("root_node"))
    nodes.append(new_tree.create_node("second", parent=new_tree.root))
    for nd in new_tree.all_nodes_itr():
        assert nd in nodes


def test_filter_nodes():
    """
    tests: Tree.filter_nodes
    Added by: William Rusnack
    """
    new_tree = Tree(identifier="tree 1")

    assert tuple(new_tree.filter_nodes(lambda n: True)) == ()

    nodes = list()
    nodes.append(new_tree.create_node("root_node"))
    nodes.append(new_tree.create_node("second", parent=new_tree.root))

    assert tuple(new_tree.filter_nodes(lambda n: False)) == ()
    assert tuple(new_tree.filter_nodes(lambda n: n.is_root("tree 1"))) == (nodes[0],)
    assert tuple(new_tree.filter_nodes(lambda n: not n.is_root("tree 1"))) == (
        nodes[1],
    )
    assert set(new_tree.filter_nodes(lambda n: True)) == set(nodes)


def test_loop():
    tree = Tree()
    tree.create_node("a", "a")
    tree.create_node("b", "b", parent="a")
    tree.create_node("c", "c", parent="b")
    tree.create_node("d", "d", parent="c")
    try:
        tree.move_node("b", "d")
    except LoopError:
        pass


def test_modify_node_identifier_directly_failed():
    tree = Tree()
    tree.create_node("Harry", "harry")
    tree.create_node("Jane", "jane", parent="harry")
    n = tree.get_node("jane")
    assert n.identifier == "jane"

    # Failed to modify
    n.identifier = "xyz"
    assert tree.get_node("xyz") is None
    assert tree.get_node("jane").identifier == "xyz"


def test_modify_node_identifier_recursively():
    tree = Tree()
    tree.create_node("Harry", "harry")
    tree.create_node("Jane", "jane", parent="harry")
    n = tree.get_node("jane")
    assert n.identifier == "jane"

    # Success to modify
    tree.update_node(n.identifier, identifier="xyz")
    assert tree.get_node("jane") is None
    assert tree.get_node("xyz").identifier == "xyz"


def test_modify_node_identifier_root():
    tree = Tree(identifier="tree 3")
    tree.create_node("Harry", "harry")
    tree.create_node("Jane", "jane", parent="harry")
    tree.update_node(tree["harry"].identifier, identifier="xyz", tag="XYZ")
    assert tree.root == "xyz"
    assert tree["xyz"].tag == "XYZ"
    assert tree.parent("jane").identifier, "xyz"


def test_subclassing():
    class SubNode(Node):
        pass

    class SubTree(Tree):
        node_class = SubNode

    tree = SubTree()
    node = tree.create_node()
    assert isinstance(node, SubNode)

    tree = Tree(node_class=SubNode)
    node = tree.create_node()
    assert isinstance(node, SubNode)


def test_shallow_copy_hermetic_pointers(tree):
    # tree 1
    # Harry
    #   └── Jane
    #       └── Diane
    #   └── Bill
    #       └── George
    tree2 = tree.subtree(nid="jane", identifier="tree 2")
    # tree 2
    # Jane
    #   └── Diane

    # check that in shallow copy, instances are the same
    assert tree["jane"] is tree2["jane"]
    assert tree["jane"]._predecessor == {"tree 1": "harry", "tree 2": None}
    assert dict(tree["jane"]._successors) == {"tree 1": ["diane"], "tree 2": ["diane"]}

    # when creating new node on subtree, check that it has no impact on initial tree
    tree2.create_node("Jill", "jill", parent="diane")
    assert "jill" in tree2
    assert "jill" in tree2.is_branch("diane")
    assert "jill" not in tree
    assert "jill" not in tree.is_branch("diane")


def test_paste_duplicate_nodes():
    t1 = Tree()
    t1.create_node(identifier="A")
    t2 = Tree()
    t2.create_node(identifier="A")
    t2.create_node(identifier="B", parent="A")

    with pytest.raises(ValueError) as e:
        t1.paste("A", t2)
    assert e.exception.args == ("Duplicated nodes ['A'] exists.",)


def test_shallow_paste():
    t1 = Tree()
    n1 = t1.create_node(identifier="A")

    t2 = Tree()
    n2 = t2.create_node(identifier="B")

    t3 = Tree()
    n3 = t3.create_node(identifier="C")

    t1.paste(n1.identifier, t2)
    assert t1.to_dict() == {"A": {"children": ["B"]}}
    t1.paste(n1.identifier, t3)
    assert t1.to_dict() == {"A": {"children": ["B", "C"]}}

    assert t1.level(n1.identifier) == 0
    assert t1.level(n2.identifier) == 1
    assert t1.level(n3.identifier) == 1


def test_root_removal():
    t = Tree()
    t.create_node(identifier="root-A")
    assert len(t.nodes.keys()) == 1
    assert t.root == "root-A"
    t.remove_node(identifier="root-A")
    assert len(t.nodes.keys()) == 0
    assert t.root is None
    t.create_node(identifier="root-B")
    assert len(t.nodes.keys()) == 1
    assert t.root == "root-B"


def test_from_map(input_dict):
    tree = Tree.from_map(input_dict)
    assert tree.size() == 6
    assert tree.root == [k for k, v in input_dict.items() if v is None][0]
    tree = Tree.from_map(input_dict, id_func=lambda x: x.upper())
    assert tree.size() == 6

    def data_func(x):
        return x.upper()

    tree = Tree.from_map(input_dict, data_func=data_func)
    assert tree.size() == 6
    assert tree.get_node(tree.root).data == data_func(
        [k for k, v in input_dict.items() if v is None][0]
    )
    with pytest.raises(ValueError):
        # invalid input payload without a root
        tree = Tree.from_map({"a": "b"})

    with pytest.raises(ValueError):
        # invalid input payload without more than 1 root
        tree = Tree.from_map({"a": None, "b": None})
