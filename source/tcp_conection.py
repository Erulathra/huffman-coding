import socket
from enum import Enum
import huffman as h


class message_type_enum(Enum):
    text = bytes('T', 'ascii')
    file = bytes('F', 'ascii')


def create_connection_header(message_length: int, content_length, frequency_list: list[tuple[bytes, int]],
                             file_name: str = "") -> bytes:
    message_type = message_type_enum.text
    if len(file_name):
        message_type = message_type_enum.file

    # add message type, message length, content length and file name to header and fill to 256 bytes with 0s
    header = bytearray()
    header += message_type.value
    header += bytearray(message_length.to_bytes(4, 'little'))
    header += bytearray(content_length.to_bytes(4, 'little'))
    header += bytearray(len(file_name).to_bytes(1, 'little'))
    header += bytearray(bytes(file_name, 'ascii'))
    header += bytearray(bytes(256 - len(header)))

    # add frequency table length and frequency table to header
    header += len(frequency_list).to_bytes(2, 'little')

    for byte, frequency in frequency_list:
        header += bytearray(byte)
        header += bytearray(frequency.to_bytes(1, 'little'))

    header += bytearray(bytes(1024 - len(header)))

    return bytes(header)


def read_data_from_header(header: bytes) -> (message_type_enum, int, str, str, list[tuple[bytes, int]]):
    if len(header) < 1024:
        raise WrongHeaderException()

    # read message type, message length, content length and file name
    test = header[0]
    if header[0] == 84:
        message_type = message_type_enum.text
    else:
        message_type = message_type_enum.file

    message_length = int.from_bytes(header[1:5], 'little')
    content_length = int.from_bytes(header[5:9], 'little')
    file_name_length = header[9]
    filename = str(header[10:10 + file_name_length], 'ascii')

    # read frequency table length and frequency table
    frequency_table_length = int.from_bytes(header[256:258], 'little')
    frequency_table = []
    for i in range(258, 258 + frequency_table_length * 2, 2):
        byte = header[i]
        frequency = header[i + 1]
        frequency_table.append((byte.to_bytes(1, 'little'), frequency))

    return message_type, message_length, content_length, filename, frequency_table


def send_data(sender_socket: socket.socket, message: bytes, file_name: str = ""):
    # encode message and calculate frequency table
    frequency_table = h.calculate_frequency(message)
    huffman_message = h.encode(message, frequency_table)

    # generate and send header
    header = create_connection_header(len(message), len(
        huffman_message), frequency_table, file_name)
    sender_socket.sendall(header)

    # send data
    sender_socket.sendall(huffman_message)


def receive_data(receiver_socket: socket.socket) -> tuple[message_type_enum, bytes]:
    header = receiver_socket.recv(1024)
    message_type, message_length, content_length, filename, frequency_table = read_data_from_header(
        header)
    message = receiver_socket.recv(content_length)

    huffman_root = h.create_huffman_tree(frequency_table)
    decoded_message = h.decompress(message, message_length, huffman_root)

    return message_type, filename, decoded_message


class WrongHeaderException(Exception):
    pass
