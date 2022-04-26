from bitarray import bitarray

import huffman as h


def main():
    message = bytes("TO BE OR NOT TO BE", 'utf-8')
    frequency_list = h.calculate_frequency(message)
    root = h.create_huffman_tree(frequency_list)

    dictionary = h.create_huffman_dictionary(root)
    compressed = h.compress(message, dictionary)

    print(dictionary)

    test = bitarray()
    test.frombytes(compressed)
    print(test)

    decompressed = h.decompress(compressed, len(message), root)
    print(str(decompressed, 'utf-8'))


if __name__ == "__main__":
    main()
