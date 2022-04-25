from __future__ import annotations
import collections
import heapq


class HuffmanTreeNode:
    def __init__(self, byte: bytes, frequency: int):
        self.__byte = byte
        self.__frequency = frequency
        self.left = None
        self.right = None

    @property
    def frequency(self):
        return self.__frequency

    def __lt__(self, other):
        return self.__frequency < other.__frequency

    def __eq__(self, other: HuffmanTreeNode):
        if other is None:
            return False
        if not isinstance(other, HuffmanTreeNode):
            return False
        return self.__frequency == other.__frequency


# generate frequency dictionary
def calculate_frequency(message: bytes) -> list[tuple[bytes, int]]:
    frequency_list = collections.Counter(message).most_common()
    frequency_list = list(reversed(frequency_list))

    result = normalize_frequency_list(frequency_list)

    return result


def normalize_frequency_list(frequency_list):
    result = []
    i = 0
    previous_frequency = frequency_list[0][1]
    for byte, frequency in frequency_list:
        if frequency != previous_frequency:
            i += 1

        previous_frequency = frequency

        result.append((byte.to_bytes(1, 'big'), i))
    return result


def create_huffman_tree(frequency_list: list[tuple[bytes, int]]) -> HuffmanTreeNode:
    # generate trees with one node
    trees_list = [HuffmanTreeNode(byte, frequency) for byte, frequency in frequency_list]
    heapq.heapify(trees_list)

    while len(trees_list) > 1:
        node_one = heapq.heappop(trees_list)
        node_two = heapq.heappop(trees_list)

        # swap nodes when first node's frequency is greater than second
        if node_two < node_one:
            node_two, node_one = node_one, node_two

        # create new tree with upper two nodes
        new_tree = HuffmanTreeNode(None, node_one.frequency + node_two.frequency)
        new_tree.left = node_one
        new_tree.right = node_two

        heapq.heappush(trees_list, new_tree)

    return trees_list[0]

#TODO: Check huffman tree after list normalization