import socket
import sys

import utils
from process import Process


def start(hostname):
    port = utils.find_free_port()
    tunnel = Process(
        f"cloudflared access tcp --hostname {hostname}  localhost:{port}")
    tunnel.wait_started(message="Start Websocket listener")
    host = "127.0.0.1"
    # create a socket object and connect to the server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))

        # send a command to the server
        while True:
            cmd = input("Enter a command to execute on the server: ")
            s.sendall(cmd.encode())

            # receive and print the output from the server
            data = s.recv(1024)
            print(data.decode())

if __name__ == "__main__":
    start(hostname=sys.argv[1])
