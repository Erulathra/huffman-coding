from __future__ import annotations


class HuffmanTreeNode:
    def __init__(self, byte: bytes, frequency: int):
        self.__byte = byte
        self.__frequency = frequency
        self.__left = None
        self.__right = None
        self.__root = None

    @property
    def frequency(self):
        return self.__frequency

    @property
    def byte(self):
        return self.__byte

    @property
    def left(self):
        return self.__left

    @left.setter
    def left(self, value: HuffmanTreeNode):
        self.__left = value
        value.__root = self

    @property
    def right(self):
        return self.__right

    @right.setter
    def right(self, value: HuffmanTreeNode):
        self.__right = value
        value.__root = self

    @property
    def root(self):
        return self.__root

    def __lt__(self, other):
        return self.__frequency < other.__frequency

    def __eq__(self, other: HuffmanTreeNode):
        if other is None:
            return False
        if not isinstance(other, HuffmanTreeNode):
            return False
        return self.__frequency == other.__frequency


def get_all_leaves(huffman_tree_root: HuffmanTreeNode) -> list[HuffmanTreeNode]:
    stack = []
    result = []

    stack.append(huffman_tree_root)
    while len(stack) != 0:
        root = stack.pop()
        if root.left is None and root.right is None:
            result.append(root)
        if root.left is not None:
            stack.append(root.left)
        if root.right is not None:
            stack.append(root.right)

    return result
