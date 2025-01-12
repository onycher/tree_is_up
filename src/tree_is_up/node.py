from typing import Any, Dict, List, Optional, Hashable


class Node:
    """
    Represents a node in a tree-like structure.

    Each node can have a tag, an identifier, and associated data.
    It also maintains relationships with its predecessors and successors within different trees.
    """

    def __init__(self, tag: Any, identifier: Optional[Hashable] = None) -> None:
        """
        Initializes a new Node object.

        Args:
            tag: The tag associated with this node. Can be any type.
            identifier: An optional identifier for this node. Must be hashable if provided.
        """
        self.tag: Any = tag
        self.identifier: Optional[Hashable] = identifier
        self.expanded: bool = True
        self._predecessor: Dict[str, Optional[Hashable]] = {}
        self._successors: Dict[str, List[Hashable]] = {}
        self.data: Any = None

    def __repr__(self) -> str:
        """
        Returns a string representation of the Node object.

        Returns:
            A string representing the Node object, including its tag and identifier.
        """
        return f"Node(tag={self.tag}, identifier={self.identifier})"

    def update_successors(self, identifier: Hashable, tree_id: str = "default") -> None:
        """
        Adds a successor to the node within a specified tree.

        Args:
            identifier: The identifier of the successor node.
            tree_id: The identifier of the tree to which the successor is added (default is "default").
        """
        if tree_id not in self._successors:
            self._successors[tree_id] = []
        self._successors[tree_id].append(identifier)

    def set_successors(
        self, identifiers: List[Hashable], tree_id: str = "default"
    ) -> None:
        """
        Sets the successors of the node within a specified tree.

        Args:
            identifiers: A list of identifiers representing the successor nodes.
            tree_id: The identifier of the tree to which the successors are set (default is "default").
        """
        self._successors[tree_id] = identifiers

    def successors(self, tree_id: str = "default") -> List[Hashable]:
        """
        Retrieves the successors of the node within a specified tree.

        Args:
            tree_id: The identifier of the tree for which successors are requested (default is "default").

        Returns:
            A list of identifiers representing the successor nodes. Returns an empty list if no successors exist
            for the given tree_id.
        """
        return self._successors.get(tree_id, [])

    def set_predecessor(
        self, identifier: Optional[Hashable], tree_id: str = "default"
    ) -> None:
        """
        Sets the predecessor of the node within a specified tree.

        Args:
            identifier: The identifier of the predecessor node. If None, it means there is no predecessor.
            tree_id: The identifier of the tree to which the predecessor is set (default is "default").
        """
        self._predecessor[tree_id] = identifier

    def predecessor(self, tree_id: str = "default") -> Optional[Hashable]:
        """
        Retrieves the predecessor of the node within a specified tree.

        Args:
            tree_id: The identifier of the tree for which the predecessor is requested (default is "default").

        Returns:
            The identifier of the predecessor node, or None if no predecessor exists for the given tree_id.
        """
        return self._predecessor.get(tree_id)

    def is_leaf(self, tree_id: str = "default") -> bool:
        """
        Checks if the node is a leaf node within a specified tree.

        A node is considered a leaf if it has no successors in the specified tree.

        Args:
            tree_id: The identifier of the tree for which to check (default is "default").

        Returns:
            True if the node is a leaf in the specified tree, False otherwise.
        """
        return not bool(self._successors.get(tree_id, []))
