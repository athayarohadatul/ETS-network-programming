# file_server_processpool.py (ProcessPoolExecutor version)
from socket import *
import socket
import logging
from concurrent.futures import ProcessPoolExecutor

from file_protocol import FileProtocol

def handle_client(data):
    # Fungsi ini dijalankan di process pool, jadi tidak bisa menerima socket secara langsung
    fp = FileProtocol()
    request = data.decode()
    hasil = fp.proses_string(request)
    hasil = hasil + "\r\n\r\n"
    return hasil.encode()

def main():
    ip = '0.0.0.0'
    port = 7777
    max_workers = 50  # Jumlah maksimal proses dalam pool
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((ip, port))
    server_socket.listen(5)

    logging.warning(f"Server berjalan di {ip}:{port} dengan ProcessPoolExecutor")

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        while True:
            connection, address = server_socket.accept()
            logging.warning(f"Handling connection from {address}")

            # Baca data awal sampai request selesai (\r\n\r\n)
            buffer = ""
            while True:
                data = connection.recv(1024)
                if not data:
                    break
                buffer += data.decode()
                if "\r\n\r\n" in buffer:
                    break

            # Kirim request ke process pool
            future = executor.submit(handle_client, buffer.encode())
            hasil = future.result()

            # Kirim hasil kembali ke client
            connection.sendall(hasil)
            connection.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)
    main()
