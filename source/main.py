import huffman as h


def main():
    message = bytes("TO BE OR NOT TO BE", 'utf-8')
    frequency_list = h.calculate_frequency(message)
    h.create_huffman_tree(frequency_list)


if __name__ == "__main__":
    main()
