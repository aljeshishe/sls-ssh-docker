import logging
import time

import utils
from ssh_server import SSHServer
from tunnel import Tunnel

log = logging.getLogger(__name__)

_server = None


def start():
    global _server
    if _server:
        raise Exception("Already started")
    _server = Server()


def stop():
    global _server
    if not _server:
        raise Exception("Not Started")
    _server.stop()


class Server:
    def __init__(self):
        port = utils.find_free_port()
        log.info(f"Using port {port=}")
        self.tunnel = Tunnel(port=port)
        self.ssh_server = SSHServer(port)
        # self.sshd = Process("/usr/sbin/sshd -f /app/sshd_config -e -D")
        # self.sshd.wait_started(message="Server listening on")

    def stop(self):
        self.ssh_server.stop()
        self.tunnel.stop()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    log.debug("started")
    start()
    time.sleep(10000)
