import json
import logging

from file_interface import FileInterface

class FileProtocol:
    def __init__(self):
        self.file = FileInterface()

    def proses_string(self, string_datamasuk=''):
        logging.warning(f"string diproses: {string_datamasuk}")
        try:
            # parsing input json
            data = json.loads(string_datamasuk)
            c_request = data.get('cmd', '').lower()
            params = data.get('params', [])
            logging.warning(f"memproses request: {c_request}")
            cl = getattr(self.file, c_request)(params)
            return json.dumps(cl)
        except Exception as e:
            logging.error(f"error proses_string: {e}")
            return json.dumps(dict(status='ERROR', data='request tidak dikenali'))

if __name__=='__main__':
    fp = FileProtocol()
    print(fp.proses_string(json.dumps({"cmd":"list","params":[]})))
    print(fp.proses_string(json.dumps({"cmd":"get","params":["pokijan.jpg"]})))
