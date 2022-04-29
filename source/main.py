from genericpath import exists
from rich.markdown import Markdown
from rich.console import Console
from rich.prompt import Prompt
import socket
import time
import tcp_conection as con
import os

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

console = Console()
waiter_txt = "Wciśnij dowolny klawisz, aby kontynuować..."

def main():
    message = "Zażółć gęślą jaźń"
    path = "plik.txt"
    user_input = ''
    host_address = "127.0.0.1"
    port = 61111
    while user_input != 'q':
        cls()
        console.print("[bold][cyan]Wiadomość:[/][/]\n", message)
        console.print(f"[bold][cyan]Adres:[/][/] \n {host_address} : {port}\n")

        console.print(('''Podaj, czy chcesz:
        (1) Ustawić wiadomość
        (2) Ustawić adres hosta
        (3) Ustawić port
        (4) Nadać wiadomość
        (5) Odebrać wiadomość
        [dim]\[q - wyjście][/]'''))
        user_input = input("> ")
        print()
        match user_input:
            case '1': message, path = get_message(path) or (message, path)
            case '2': host_address = input("Podaj adres: ")
            case '3': port = int(input("Podaj port: "))
            case '4': send_message(message, host_address, port)
            case '5': receive_message(host_address, port)
            case 'q': break
            case _: continue


def get_message(path) -> (str, str):
    console.print('''Wczytaj wiadomość
    (1) Z konsoli
    (2) Z pliku''')
    match input("> "):
        case '1':
            message = input("Podaj treść wiadomości: ")
            if message != "": 
                return (message, path)
        case '2':
            path = Prompt.ask(f"Podaj ścieżkę", default=path)
            if exists(path):
                with open(path) as file:
                    return (file.read(), path)
            else:
                input(f"Nie znaleziono pliku. {waiter_txt}")


def send_message(message_str, host, port):
    message = bytes(message_str, 'utf-8')
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        for i in range(60):
            try:
                s.connect((host, port))
                con.send_data(s, message)
                input(f"Wysłano! {waiter_txt}")
                break
            except ConnectionRefusedError:
                console.print(f"{i + 1} Odbiorca nie nawiązał połączenia")
                time.sleep(1)


def receive_message(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        conn, addr = s.accept()
        with conn:
            console.print(f"Connected by {addr}")
            message_type, message = con.receive_data(conn)
            print()
            console.print(str(message, 'utf-8'))
            print()
    path = Prompt.ask("Gdzie zapisać plik? [dim]\[wciśnij Enter by pominąć][/]")
    if(path != ''):
        with open(path, 'w') as file:
            file.write(message.decode("utf-8"))
            input(f"Zapisano plik! {waiter_txt}")

if __name__ == "__main__":
    main()