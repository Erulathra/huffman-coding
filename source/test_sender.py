import socket
import time

import tcp_conection as con

HOST = "192.168.184.132"
PORT = 61111

text = "Bartosz ma Nogę :3"
message = bytes(text, 'utf-8')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    for i in range(60):
        try:
            s.connect((HOST, PORT))
            con.send_data(s, message)
            print("Wysłano")
            break
        except ConnectionRefusedError:
            print(f"{i + 1} Odbiorca nie nawiązał połączenia")
            time.sleep(1)
