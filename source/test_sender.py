import socket

import tcp_conection as con

HOST = "127.0.0.1"
PORT = 61111

text = "Trzy Pierścienie dla królów elfów pod otwartym niebem, \n \
        Siedem dla władców krasnali w ich kamiennych pałacach, \n \
        Dziewięć dla śmiertelników, ludzi śmierci podległych, \n \
        Jeden dla Władcy Ciemności na czarnym tronie \n \
        W Krainie Mordor, gdzie zaległy cienie, \n \
        Jeden, by wszystkimi rządzić, Jeden, by wszystkie odnaleźć, \n \
        Jeden, by wszystkie zgromadzić i w ciemności związać \n \
        W Krainie Mordor, gdzie zaległy cienie."
message = bytes(text, 'utf-8')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    con.send_data(s, message)
    print("Wysłano")