import logging
import os
import platform
import re
import tempfile
from pathlib import Path

import requests

from notifier import notify
from process import Process

log = logging.getLogger(__name__)


class Tunnel:
    def __init__(self, port: int):
        self.tmp_dir = Path(tempfile.gettempdir()) / "cloudflared_iubfoiu31bp4iufb"
        log.info(f"Using {self.tmp_dir=}")
        self.tmp_dir.mkdir(exist_ok=True, parents=True)

        self._ensure_installed()
        self._tunnel = self._start_tunnel(port)

    def _start_tunnel(self, port):
        self.tunnel = Process(
            f"{self.tmp_dir}/cloudflared tunnel --url ssh://localhost:{port} --logfile {self.tmp_dir}/cloudflared.log")
        self.tunnel.wait_started(message="registered with protocol")
        for line in self.tunnel.buffer:
            if result := re.search("https://.*.trycloudflare.com", line):
                url = result.group(0)
                host = url.replace("https://", "")
                message = f"{url}\nssh root@{host}"
                notify(message)
                break

    def _ensure_installed(self):
        dst_dir = self.tmp_dir
        if not Path("cloudflared").exists():
            system = platform.system()
            if system == "Darwin":
                self._download(
                    "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-darwin-amd64.tgz")
                os.system(f"tar -xzvf {dst_dir}/cloudflared-darwin-amd64.tgz -C {dst_dir}")
            elif system == "Linux":
                self._download(
                    "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64")
                os.system(f"mv {dst_dir}/cloudflared-linux-amd64 {dst_dir}/cloudflared")
        os.system(f"chmod 777 {dst_dir}/cloudflared")

    def _download(self, url):
        response = requests.get(url, stream=True)
        response.raise_for_status()

        file_name = self.tmp_dir / url.split("/")[-1]
        with file_name.open("wb") as file:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                file.write(chunk)

    def stop(self):
        self.tunnel.stop()
