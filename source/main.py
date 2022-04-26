from bitarray import bitarray

import huffman as h


def main():
    message = bytes("TO BE OR NOT TO BE", 'utf-8')
    frequency_list = h.calculate_frequency(message)
    root = h.create_huffman_tree(frequency_list)

    dictionary = h.create_huffman_dictionary(root)
    compressed = h.compress(message, dictionary)

    test = bitarray()
    test.frombytes(compressed)
    print(test)


if __name__ == "__main__":
    main()
