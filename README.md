# Prosty czat P2P

Minimalistyczny czat konsolowy P2P w Pythonie do bezpośredniej wymiany wiadomości między dwoma węzłami.

## Szybki start

### 1. Host (Węzeł A)
Uruchom skrypt, aby słuchać przychodzących połączeń:
```bash
py client.py -l -v
```

### 2. Klient (Węzeł B)
Połącz się z węzłem A, podając jego adres IP:
```bash
# Test lokalny na tej samej maszynie
py client.py -c 127.0.0.1 -v

# Połączenie zdalne
py client.py -c <IP_WĘZŁA_A> -v
```

### Wyjście
Wpisz `/q`, `exit` lub `quit`, aby się rozłączyć.

## Rozwiązywanie problemów
* **Blokada zapory sieciowej:** Otwórz port w systemie Linux za pomocą `sudo ufw allow 9000/tcp`.
* **Konflikt portów:** Zmień port domyślny za pomocą `-p` (np. `-p 9500`).

## Autor
Opracowano przez HpeS
