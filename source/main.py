from bitarray import bitarray

import huffman as h
import tcp_conection as con


def main():
    message_str = "Założyć gęślą jaźń"
    print(message_str)
    message = bytes(message_str, 'utf-8')
    frequency_list = h.calculate_frequency(message)
    root = h.create_huffman_tree(frequency_list)

    dictionary = h.create_huffman_dictionary(root)
    compressed = h.compress(message, dictionary)

    print(frequency_list)
    print(dictionary)

    test = bitarray()
    test.frombytes(compressed)
    print(test)

    decompressed = h.decompress(compressed, len(message), root)
    print(str(decompressed, 'utf-8'))

    header = con.create_connection_header(6500, 2137, frequency_list, "ziemniaki.txt")
    message_type, message_length, content_length, filename, frequency_table = con.read_data_from_header(header)
    print(message_type)
    print(message_length)
    print(content_length)
    print(filename)
    print(frequency_table)


if __name__ == "__main__":
    main()
