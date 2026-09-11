import argparse
import socket
import threading
import sys


def recv_loop(sock, verbose):
    """Odbieranie wiadomości w osobnym wątku."""
    try:
        while True:
            data = sock.recv(4096)
            if not data:
                print("\n[*] Połączenie zamknięte")
                break
            msg = data.decode("utf-8", errors="replace")
            print(f"\r<< {msg}\n> ", end="", flush=True)
    except (ConnectionResetError, OSError):
        pass


def send_loop(sock, verbose):
    """Wysyłanie wiadomości ze standardowego wejścia."""
    try:
        while True:
            msg = input("> ")
            if msg in ("exit", "quit", "/q"):
                break
            if not msg:
                continue
            sock.sendall(msg.encode("utf-8"))
    except (KeyboardInterrupt, EOFError):
        pass
    finally:
        try:
            sock.close()
        except OSError:
            pass


def run_peer(sock, verbose):
    """Główna logika po nawiązaniu połączenia."""
    if verbose:
        print("[*] Połączenie P2P nawiązane. Wpisz wiadomości, /q — wyjście.")

    t = threading.Thread(target=recv_loop, args=(sock, verbose), daemon=True)
    t.start()
    send_loop(sock, verbose)
    sys.exit(0)


def main():
    parser = argparse.ArgumentParser(
        description="Węzeł P2P: słuchanie lub połączenie z innym węzłem"
    )
    parser.add_argument("-H", "--host", default="0.0.0.0",
                        help="Adres do słuchania (tryb --listen)")
    parser.add_argument("-p", "--port", type=int, default=9000,
                        help="Port (domyślnie 9000)")
    parser.add_argument("-c", "--connect", metavar="HOST",
                        help="Połącz się ze zdalnym węzłem (tryb klienta)")
    parser.add_argument("-l", "--listen", action="store_true",
                        help="Oczekuj na połączenie przychodzące")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Szczegółowe dane wyjściowe")
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    # Tryb połączenia
    if args.connect:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((args.connect, args.port))
        except ConnectionRefusedError:
            print(f"[!] Nie udało się połączyć z {args.connect}:{args.port}")
            sys.exit(1)
        if args.verbose:
            print(f"[*] Połączono z {args.connect}:{args.port}")
        run_peer(sock, args.verbose)

    # Tryb słuchania
    elif args.listen:
        srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind((args.host, args.port))
        srv.listen(1)
        print(f"[*] Oczekiwanie na połączenie na {args.host}:{args.port}")
        conn, addr = srv.accept()
        srv.close()
        if args.verbose:
            print(f"[*] Połączył się {addr}")
        run_peer(conn, args.verbose)

    else:
        parser.print_help()
        sys.exit(0)


if __name__ == "__main__":
    main()
