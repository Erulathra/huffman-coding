from __future__ import annotations

import collections
import heapq

from bitarray import bitarray

from HuffmanTreeNode import HuffmanTreeNode
from HuffmanTreeNode import get_all_leaves


# generate frequency dictionary
def calculate_frequency(message: bytes) -> list[tuple[bytes, int]]:
    frequency_list = collections.Counter(message).most_common()
    frequency_list = list(reversed(frequency_list))

    frequency_list = normalize_frequency_list(frequency_list)

    return frequency_list


def normalize_frequency_list(frequency_list):
    result = []
    i = 1
    previous_frequency = frequency_list[0][1]
    for byte, frequency in frequency_list:
        if frequency != previous_frequency:
            i += 1

        previous_frequency = frequency

        result.append((byte.to_bytes(1, 'big'), i))
        # result.append((byte.to_bytes(1, 'big'), frequency))
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


def compress(message: bytes, dictionary: dict[bytes, bitarray]) -> bytes:
    result = bitarray()

    # encode all bytes and add them to result
    for byte in message:
        byte = byte.to_bytes(1, 'big')
        result += dictionary[byte]

    return result.tobytes()


# creates dictionary {byte: huffman_code}
def create_huffman_dictionary(huffman_tree_root: HuffmanTreeNode) -> dict[bytes, bitarray]:
    result = {}

    for leaf in get_all_leaves(huffman_tree_root):
        code = extract_code_from_leaf(leaf)
        result[leaf.byte] = code

    return result


def extract_code_from_leaf(leaf) -> bitarray:
    code = bitarray()
    node = leaf
    while node.root is not None:
        # add to code 1 when node is right child and 0 when is left child
        if node.root.right is node:
            code.append(1)
        else:
            code.append(0)

        node = node.root

    # reverse code
    return code[::-1]


def decompress(message: bytes, message_length: int, huffman_tree_root: HuffmanTreeNode) -> bytes:
    message_as_bits = bitarray()
    message_as_bits.frombytes(message)

    result = bytearray()

    # repeat until message is not complete
    while len(result) != message_length:
        node = huffman_tree_root

        # Goes through all nodes and decodes byte
        while node.right is not None and node.left is not None:
            bit = message_as_bits.pop(0)
            if bit == 1:
                node = node.right
            else:
                node = node.left

        # Add decoded byte to result
        result += node.byte

    return bytes(result)

