import socket
import threading
import os

LOGFILE = "honeypot.log"

def log(message):
    with open(LOGFILE, "a") as f:
        f.write(message + "\n")
    print(message)

def handle_client(client_socket, client_address):
    log(f"Connection from {client_address}")

    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            log(f"Received from {client_address}: {data.decode('utf-8')}")
            client_socket.send(b"Invalid command\n")
    except Exception as e:
        log(f"Exception from {client_address}: {str(e)}")
    finally:
        log(f"Closing connection from {client_address}")
        client_socket.close()

def start_honeypot(host='0.0.0.0', port=23):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    log(f"Honeypot listening on {host}:{port}")

    while True:
        client_socket, client_address = server.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_handler.start()

if __name__ == "__main__":
    try:
        start_honeypot()
    except KeyboardInterrupt:
        log("Honeypot shutting down")
    except Exception as e:
        log(f"Error: {str(e)}")
