# file_server.py (ThreadPoolExecutor version)
from socket import *
import socket
import logging
from concurrent.futures import ThreadPoolExecutor

from file_protocol import FileProtocol
fp = FileProtocol()

def handle_client(connection, address):
    logging.warning(f"Handling connection from {address}")
    buffer = ""
    while True:
        data = connection.recv(1024)
        if not data:
            break
        buffer += data.decode()
        while "\r\n\r\n" in buffer:
            request, buffer = buffer.split("\r\n\r\n", 1)
            hasil = fp.proses_string(request)
            hasil = hasil + "\r\n\r\n"
            connection.sendall(hasil.encode())
    connection.close()

def main():
    ip = '0.0.0.0'
    port = 7777
    max_workers = 1  # Jumlah maksimal thread dalam pool
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((ip, port))
    server_socket.listen(5)

    logging.warning(f"Server berjalan di {ip}:{port} dengan ThreadPoolExecutor")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        while True:
            connection, address = server_socket.accept()
            executor.submit(handle_client, connection, address)

if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)
    main()
