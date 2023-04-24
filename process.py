import logging
import os
import subprocess
import time

log = logging.getLogger(__name__)


class Process:
    def __init__(self, command):
        self.process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        os.set_blocking(self.process.stdout.fileno(), False)
        os.set_blocking(self.process.stderr.fileno(), False)

        self.buffer = []

    def wait_started(self, message, timeout=30):
        start = time.time()
        while True:
            if time.time() - start > timeout:
                raise Exception(f"Timeout waiting for {message}")
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
