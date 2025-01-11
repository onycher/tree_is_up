# src/tree_is_up/node.py
from typing import Any, Dict, List


class Node:
    """
    Represents a node in a tree structure with the ability to store data and maintain relationships with other nodes.
    
    Attributes:
        tag (Any): The tag associated with the node.
        identifier (str): A unique identifier for the node.
        expanded (bool): Whether the node is currently expanded or not.
        _predecessor (Dict[str, str]): Predecessors of the node in different trees.
        _successors (Dict[str, List[str]]): Successors of the node in different trees.
        data (Any): Optional data associated with the node.
    """

    def __init__(self, tag: Any = None, identifier: str = "", expanded: bool = True):
        """
        Initializes a new instance of Node.

        Args:
            tag (Any, optional): The tag for the node. Defaults to None.
            identifier (str, optional): A unique identifier for the node. Defaults to an empty string.
            expanded (bool, optional): Whether the node is expanded or not. Defaults to True.
        """
        self.tag = tag
        self.identifier = identifier
        self.expanded = expanded
        self._predecessor: Dict[str, str] = {}
        self._successors: Dict[str, List[str]] = {}
        self.data: Any = None

    def __repr__(self) -> str:
        """
        Returns a string representation of the Node instance.

        Returns:
            str: A formatted string representing the node.
        """
        return f"Node(tag={self.tag}, identifier={self.identifier})"

    @property
    def tag(self) -> Any:
        """Getter for the node's tag."""
        return self._tag

    @tag.setter
    def tag(self, value: Any):
        """Setter for the node's tag."""
        self._tag = value

    @property
    def identifier(self) -> str:
        """Getter for the node's identifier."""
        return self._identifier

    @identifier.setter
    def identifier(self, value: str):
        """Setter for the node's identifier."""
        self._identifier = value

    def set_predecessor(self, predecessor_id: str, tree_id: str) -> None:
        """
        Sets or removes a predecessor for this node in a specific tree.

        Args:
            predecessor_id (str): The ID of the predecessor node. Pass `None` to remove the predecessor.
            tree_id (str): The identifier of the tree in which the predecessor is set.
        """
        if predecessor_id is None:
            self._predecessor.pop(tree_id, None)
        else:
            self._predecessor[tree_id] = predecessor_id

    def set_successors(self, successor_ids: List[str], tree_id: str) -> None:
        """
        Sets the successors of this node in a specific tree.

        Args:
            successor_ids (List[str]): A list of IDs for successor nodes.
            tree_id (str): The identifier of the tree in which the successors are set.
        """
        self._successors[tree_id] = successor_ids

    def update_successors(self, successor_id: str, tree_id: str) -> None:
        """
        Adds a new successor to this node for a specific tree.

        Args:
            successor_id (str): The ID of the successor node.
            tree_id (str): The identifier of the tree in which the successor is added.
        """
        if tree_id not in self._successors:
            self._successors[tree_id] = []
        self._successors[tree_id].append(successor_id)

    def successors(self, tree_id: str) -> List[str]:
        """
        Retrieves a list of successor IDs for this node in a specific tree.

        Args:
            tree_id (str): The identifier of the tree.

        Returns:
            List[str]: A list of successor IDs.
        """
        return self._successors.get(tree_id, [])

    def predecessor(self, tree_id: str) -> str:
        """
        Retrieves the predecessor ID for this node in a specific tree.

        Args:
            tree_id (str): The identifier of the tree.

        Returns:
            str: The predecessor's ID or None if there is no predecessor.
        """
        return self._predecessor.get(tree_id, None)

    def is_leaf(self, tree_id: str) -> bool:
        """
        Determines whether this node is a leaf in a specific tree (i.e., has no successors).

        Args:
            tree_id (str): The identifier of the tree.

        Returns:
            bool: True if the node is a leaf; False otherwise.
        """
        return not self.successors(tree_id)