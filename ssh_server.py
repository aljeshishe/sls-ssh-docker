import logging
import os
import re
import subprocess
import time
import requests
import server
import utils
log = logging.getLogger(__name__)

_server = None


def _message(msg):
    apiToken = '5803765903:AAH2ayWpVcook4JpoiHvMzgOvJCjsLItcmw'
    chatID = '99044115'
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'

    response = requests.post(apiURL, json={'chat_id': chatID, 'text': msg})
    response.raise_for_status()


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


class Process:
    def __init__(self, command):
        self.process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        os.set_blocking(self.process.stdout.fileno(), False)
        os.set_blocking(self.process.stderr.fileno(), False)

        self.buffer = []

    def wait_started(self, message, timeout=10):
        while True:
            if message in self._process(self.process.stderr, "stderr"):
                return
            if message in self._process(self.process.stdout, "stdout"):
                return

            exit_code = self.process.poll()
            if exit_code is None:
                time.sleep(.2)
                continue
            if exit_code == 0:
                return
            if exit_code > 0:
                output = "".join(self.process.stderr.readlines())
                raise Exception(f"Process exited with {exit_code} code\n{output}")

    def _process(self, file, name):
        line = file.readline()
        if line:
            line = line.strip()
            self.buffer.append(f"{name}: {line}")
            log.debug(line)
            return line
        return ""

    def stop(self):
        self.process.terminate()


class Server:
    def __init__(self):
        port = utils.find_free_port()
        log.info(f"Using port {port=}")
        # self.sshd = Process("/usr/sbin/sshd -f /app/sshd_config -e -D")
        # self.sshd.wait_started(message="Server listening on")

        self.tunnel = Process(
            f"cloudflared tunnel --url ssh://localhost:{port} --logfile ./cloudflared.log --metrics localhost:45678")
        self.tunnel.wait_started(message="registered with protocol")
        for line in self.tunnel.buffer:
            if result := re.search("https://.*.trycloudflare.com", line):
                url = result.group(0)
                host = url.replace("https://", "")
                message = f"{url}\nssh root@{host}"
                _message(message)
                break
        server.run_server(port=port)

    def stop(self):
        # self.sshd.stop()
        self.tunnel.stop()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    log.debug("started")
    start()
    time.sleep(10000)
