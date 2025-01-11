import pytest

from tree_is_up.node import Node


@pytest.fixture
def node1():
    return Node("Test One", "identifier 1")


@pytest.fixture
def node2():
    return Node("Test One", "identifier 1")


def test_initialization(node1):
    assert node1.tag == "Test One"
    assert node1.identifier == "identifier 1"
    assert node1.expanded is True
    assert node1._predecessor == {}
    assert node1._successors == {}
    assert node1.data is None


def test_set_tag(node1):
    node1.tag = "Test 1"
    assert node1.tag == "Test 1"


def test_object_as_node_tag():
    node = Node(tag=(0, 1))
    assert node.tag == (0, 1)
    assert node.__repr__().startswith("Node")


def test_set_identifier(node1):
    node1.identifier = "ID1"
    assert node1.identifier == "ID1"


def test_update_successors(node1):
    node1.update_successors("identifier 2", tree_id="tree 1")
    assert node1.successors("tree 1") == ["identifier 2"]
    assert node1._successors["tree 1"] == ["identifier 2"]
    node1.set_successors([], tree_id="tree 1")
    assert node1._successors["tree 1"] == []


def test_set_predecessor(node2):
    node2.set_predecessor("identifier 1", "tree 1")
    assert node2.predecessor("tree 1") == "identifier 1"
    assert node2._predecessor["tree 1"] == "identifier 1"
    node2.set_predecessor(None, "tree 1")
    assert node2.predecessor("tree 1") is None


def test_set_is_leaf(node1, node2):
    node1.update_successors("identifier 2", tree_id="tree 1")
    node2.set_predecessor("identifier 1", "tree 1")
    assert node1.is_leaf("tree 1") is False
    assert node2.is_leaf("tree 1") is True


def test_data(node1):
    class Flower:
        def __init__(self, color):
            self.color = color

            def __str__(self):
                return f"{self.color}"

    node1.data = Flower("red")
    assert node1.data.color == "red"
