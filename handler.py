import logging
import time

import server
import ssh_server

log = logging.getLogger(__name__)


def hello(event, context):
    print("start")

    logging.basicConfig(level=logging.DEBUG)
    log.debug("started")
    ssh_server.start()

    # os.system("bash -c './run.sh'")
    time.sleep(10000)
    print("end")


if __name__ == "__main__":
    hello(None, None)
