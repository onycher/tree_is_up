# src/tree_is_up/node.py

from typing import Any, Dict, List, Optional


class Node:
    """
    A class representing a node in a tree structure.

    Attributes:
        tag (Any): The label or content of the node.
        identifier (str): A unique identifier for the node.
        expanded (bool): Whether the node is expanded (True) or collapsed (False).
        _predecessor (Dict[str, Optional[str]]): Mapping from tree ID to predecessor node's identifier.
        _successors (Dict[str, List[str]]): Mapping from tree ID to list of successor node identifiers.
        data (Any): Additional data associated with the node.
    """

    def __init__(
        self,
        tag: Any = None,
        identifier: str = "",
        expanded: bool = True,
        data: Any = None,
    ) -> None:
        """
        Initializes a Node instance.

        Args:
            tag (Any, optional): The label or content of the node. Defaults to None.
            identifier (str, optional): A unique identifier for the node. Defaults to an empty string.
            expanded (bool, optional): Whether the node is expanded (True) or collapsed (False). Defaults to True.
            data (Any, optional): Additional data associated with the node. Defaults to None.
        """
        self.tag = tag
        self.identifier = identifier
        self.expanded = expanded
        self._predecessor: Dict[str, Optional[str]] = {}
        self._successors: Dict[str, List[str]] = {}
        self.data = data

    def update_successors(self, successor_id: str, tree_id: str) -> None:
        """
        Adds a successor node identifier to the list of successors for a specific tree.

        Args:
            successor_id (str): The identifier of the successor node.
            tree_id (str): The ID of the tree in which the relationship is being defined.
        """
        if tree_id not in self._successors:
            self._successors[tree_id] = []
        if successor_id not in self._successors[tree_id]:
            self._successors[tree_id].append(successor_id)

    def set_successors(self, successors: List[str], tree_id: str) -> None:
        """
        Sets the list of successor node identifiers for a specific tree.

        Args:
            successors (List[str]): The list of successor node identifiers.
            tree_id (str): The ID of the tree in which the relationship is being defined.
        """
        self._successors[tree_id] = successors

    def successors(self, tree_id: str) -> List[str]:
        """
        Returns the list of successor node identifiers for a specific tree.

        Args:
            tree_id (str): The ID of the tree in which to retrieve the successors.

        Returns:
            List[str]: The list of successor node identifiers.
        """
        return self._successors.get(tree_id, [])

    def set_predecessor(self, predecessor_id: Optional[str], tree_id: str) -> None:
        """
        Sets the identifier of the predecessor node for a specific tree.

        Args:
            predecessor_id (Optional[str]): The identifier of the predecessor node. Can be None.
            tree_id (str): The ID of the tree in which the relationship is being defined.
        """
        self._predecessor[tree_id] = predecessor_id

    def predecessor(self, tree_id: str) -> Optional[str]:
        """
        Returns the identifier of the predecessor node for a specific tree.

        Args:
            tree_id (str): The ID of the tree in which to retrieve the predecessor.

        Returns:
            Optional[str]: The identifier of the predecessor node. Can be None.
        """
        return self._predecessor.get(tree_id)

    def is_leaf(self, tree_id: str) -> bool:
        """
        Checks if the node is a leaf (has no successors) in a specific tree.

        Args:
            tree_id (str): The ID of the tree to check.

        Returns:
            bool: True if the node is a leaf, False otherwise.
        """
        return not self.successors(tree_id)

    def __repr__(self) -> str:
        """
        Returns a string representation of the Node instance.

        Returns:
            str: A string in the format "Node(tag=<tag>, identifier=<identifier>)".
        """
        return f"Node(tag={self.tag}, identifier={self.identifier})"