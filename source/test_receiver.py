import socket
import tcp_conection as com

HOST = ""
PORT = 61111

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        message_type, message = com.receive_data(conn)
        print(str(message, 'utf-8'))


