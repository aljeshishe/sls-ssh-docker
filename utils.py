import socket


def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Bind to an arbitrary port
        s.bind(('localhost', 0))
        # Get the socket name (host, port) tuple
        _, port = s.getsockname()
    return port
