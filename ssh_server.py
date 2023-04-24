import socket
import subprocess
import threading
import time

import utils


class SSHServer:
    def __init__(self, port: int):
        self.host = "127.0.0.1"
        self.port = port
        self._thread = threading.Thread(target=self._start, daemon=True)
        self._thread.start()

    def _start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            print(f"Listening on {self.host}:{self.port}")

            while True:
                conn, addr = s.accept()
                # start a new thread to handle the client connection
                thread = threading.Thread(target=self._handle_client, args=(conn, addr), daemon=True)
                thread.start()

    def _handle_client(self, conn, addr):
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            # execute the command and send the output back to the client
            try:
                result = subprocess.run(data.decode("utf-8"), shell=True, stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE, timeout=5, text=True)
                message = ""
                message += f"returncode: {result.returncode}\n"
                if result.stderr:
                    message += result.stderr + "\n"
                if result.stdout:
                    message += result.stdout + "\n"
            except Exception as e:
                import traceback
                message += traceback.format_exc()
            conn.sendall(message.encode("utf-8"))
        conn.close()
        print(f"Connection closed by {addr}")

    def stop(self):
        pass


if __name__ == "__main__":
    SSHServer(port=utils.find_free_port())
    time.sleep(1000)
