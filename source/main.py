from genericpath import exists
from rich.console import Console
from rich.prompt import Prompt
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, MofNCompleteColumn
import socket
import time
import tcp_conection as con
import os


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


console = Console()
progress = Progress(SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    BarColumn(),
                    MofNCompleteColumn(),
                    transient=True)
waiter_txt = "Wciśnij dowolny klawisz, aby kontynuować..."


def main():
    message = bytes("Zażółć gęślą jaźń", "utf-8")
    path = ""

    user_input = ''
    host_address = "127.0.0.1"
    port = 61111
    while user_input != 'q':

        if len(path):
            file_name = os.path.basename(path)
        else:
            file_name = ""

        cls()

        try:
            console.print("[bold][cyan]Wiadomość:[/][/]\n",
                          str(message, 'utf-8'))
        except UnicodeDecodeError:
            console.print(
                f"[bold][cyan]Wiadomość:[/][/]\n[bold][cyan]Plik binarny")
        if len(path):
            console.print(f"[bold][cyan]Plik:[/][/] \n {path}\n")

        console.print(
            f"[bold][cyan]IP:PORT[/][/] \n {host_address} : {port}\n")

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
            case '4': send_message(message, host_address, port, file_name)
            case '5': receive_message(host_address, port)
            case 'q': break
            case _: continue


def get_message(path) -> tuple[bytes, str]:
    console.print('''Wczytaj wiadomość
    (1) Z konsoli
    (2) Z pliku''')
    match input("> "):
        case '1':
            message = input("Podaj treść wiadomości: ")
            if message != "":
                message = bytes(message, "utf-8")
                path = ""
                return (message, path)
        case '2':
            path = Prompt.ask(f"Podaj ścieżkę", default="message")
            if exists(path):
                with open(path, "rb") as file:
                    return (file.read(), path)
            else:
                input(f"Nie znaleziono pliku. {waiter_txt}")


def send_message(message, host, port, file_name):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s, progress as task_progress:
        task_connect = task_progress.add_task(
            "Próba nawiązania połączenia...", total=10)
        for i in range(10):
            try:
                s.connect((host, port))
                con.send_data(s, message, file_name)
                task_progress.update(task_connect, completed=10, visible=False)
                input(f"Wysłano! {waiter_txt}")
                break
            except ConnectionRefusedError:
                # console.print(f"{i + 1} Odbiorca nie nawiązał połączenia")
                task_progress.update(task_connect, advance=1)
                time.sleep(1)


def receive_message(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        conn, addr = s.accept()
        with conn:
            console.print(f"Connected by {addr}")
            message_type, filename, message = con.receive_data(conn)
            print()
            try:
                console.print(str(message, 'utf-8'))
            except UnicodeDecodeError:
                console.print("Plik binarny. Nie można wyświetlić.")
            print()

    if message_type == con.message_type_enum.file:
        path = Prompt.ask(
            "Gdzie zapisać plik? [dim]\[wciśnij Enter by pominąć][/]")
        with open(path + filename, 'wb') as file:
            file.write(message)
            print(f"Zapisano plik {filename}!")

    input(waiter_txt)


if __name__ == "__main__":
    main()
