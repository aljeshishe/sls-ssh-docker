import socket
import subprocess
import threading
import utils

# function to handle a single client connection
def handle_client(conn, addr):
    print(f"Connected by {addr}")
    while True:
        data = conn.recv(1024)
        if not data:
            break
        # execute the command and send the output back to the client
        try:
            result = subprocess.run(data.decode("utf-8"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=5, text=True)
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


def run_server(port):
    # create a socket object and bind it to a specific address and port
    host = "127.0.0.1"
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Listening on {host}:{port}")

        while True:
            conn, addr = s.accept()
            # start a new thread to handle the client connection
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()


if __name__ == "__main__":
    run_server(utils.find_free_port())
