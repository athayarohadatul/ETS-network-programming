import os
import socket
import json
import base64
import logging

server_address = ('172.16.16.101', 7777)

def send_command(command_dict):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    logging.warning(f"connecting to {server_address}")
    try:
        message = json.dumps(command_dict) + "\r\n\r\n"
        logging.warning("sending message")
        sock.sendall(message.encode())

        data_received = ""
        while True:
            data = sock.recv(1024)
            if data:
                data_received += data.decode()
                if "\r\n\r\n" in data_received:
                    break
            else:
                break

        hasil = json.loads(data_received.strip().replace("\r\n\r\n", ""))
        logging.warning("data received from server:")
        return hasil
    except Exception as e:
        logging.warning(f"error during data receiving: {e}")
        return False
    finally:
        sock.close()

def remote_list():
    command = {
        "cmd": "list",
        "params": []
    }
    hasil = send_command(command)
    if hasil['status'] == 'OK':
        print("daftar file:")
        for f in hasil['data']:
            print(f"- {f}")
    else:
        print("Gagal mengambil daftar file")

def remote_get(filename):
    command = {
        "cmd": "get",
        "params": [filename]
    }
    hasil = send_command(command)
    if hasil['status'] == 'OK':
        namafile = hasil['data_namafile']
        isifile = base64.b64decode(hasil['data_file'])
        with open(namafile, 'wb') as f:
            f.write(isifile)
        print(f"{namafile} berhasil diunduh")
    else:
        print(f"Gagal: {hasil['data']}")

def remote_upload(filepath):
    try:
        with open(filepath, 'rb') as f:
            file_content = base64.b64encode(f.read()).decode()
        filename = os.path.basename(filepath)

        command = {
            "cmd": "upload",
            "params": [filename, file_content]
        }
        hasil = send_command(command)
        if hasil['status'] == 'OK':
            print(f"{filename} berhasil diupload")
        else:
            print(f"Gagal upload: {hasil['data']}")
    except Exception as e:
        print(f"Gagal upload: {e}")

def remote_delete(filename):
    command = {
        "cmd": "delete",
        "params": [filename]
    }
    hasil = send_command(command)
    if hasil['status'] == 'OK':
        print(f"{filename} berhasil dihapus")
    else:
        print(f"Gagal delete: {hasil['data']}")

if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)

    print("List file sebelum upload:")
    remote_list()

    remote_upload('test_upload.txt')

    print("List file setelah upload:")
    remote_list()

    remote_delete('test_upload.txt')

    print("List file setelah delete:")
    remote_list()

