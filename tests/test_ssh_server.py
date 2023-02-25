import time


def test1():
    import ssh_server
    ssh_server.start()
    time.sleep(4)
    ssh_server.stop()