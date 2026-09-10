import argparse
import socket
import threading
import sys


def recv_loop(sock, verbose):
    """Приём сообщений в отдельном потоке."""
    try:
        while True:
            data = sock.recv(4096)
            if not data:
                print("\n[*] Соединение закрыто")
                break
            msg = data.decode("utf-8", errors="replace")
            print(f"\r<< {msg}\n> ", end="", flush=True)
    except (ConnectionResetError, OSError):
        pass


def send_loop(sock, verbose):
    """Отправка из stdin."""
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
    """Общая логика после установки соединения."""
    if verbose:
        print("[*] P2P-соединение установлено. Пиши сообщения, /q — выход.")

    t = threading.Thread(target=recv_loop, args=(sock, verbose), daemon=True)
    t.start()
    send_loop(sock, verbose)
    sys.exit(0)


def main():
    parser = argparse.ArgumentParser(
        description="P2P узел: либо слушает, либо подключается"
    )
    parser.add_argument("-H", "--host", default="0.0.0.0",
                        help="Адрес для прослушивания (режим --listen)")
    parser.add_argument("-p", "--port", type=int, default=9000,
                        help="Порт (по умолчанию 9000)")
    parser.add_argument("-c", "--connect", metavar="HOST",
                        help="Подключиться к удалённому узлу (режим клиента)")
    parser.add_argument("-l", "--listen", action="store_true",
                        help="Ждать входящее подключение")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Подробный вывод")
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

 
    if args.connect:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((args.connect, args.port))
        except ConnectionRefusedError:
            print(f"[!] Не удалось подключиться к {args.connect}:{args.port}")
            sys.exit(1)
        if args.verbose:
            print(f"[*] Подключено к {args.connect}:{args.port}")
        run_peer(sock, args.verbose)


    elif args.listen:
        srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind((args.host, args.port))
        srv.listen(1)
        print(f"[*] Жду подключения на {args.host}:{args.port}")
        conn, addr = srv.accept()
        srv.close()
        if args.verbose:
            print(f"[*] Подключился {addr}")
        run_peer(conn, args.verbose)

    else:
        parser.print_help()
        sys.exit(0)


if __name__ == "__main__":
    main()