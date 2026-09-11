# Simple P2P Chat

A minimalist console P2P chat in Python for direct messaging between two nodes.

## Quick Start

### 1. Host (Node A)
Run the script to listen for incoming connections:
```bash
py client.py -l -v
```

### 2. Client (Node B)
Connect to Node A by specifying its IP address:
```bash
# Local test on the same machine
py client.py -c 127.0.0.1 -v

# Remote connection
py client.py -c <NODE_A_IP> -v
```

### Exit
Type `/q`, `exit`, or `quit` to disconnect.

## Troubleshooting
* **Firewall block:** Open the port on Linux using `sudo ufw allow 9000/tcp`.
* **Port collision:** Change the default port with `-p` (e.g., `-p 9500`).

## Author
Developed by HpeS
