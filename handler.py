import os


def hello(event, context):
    print("start")
    os.system("/usr/sbin/sshd")
    os.system("cloudflared tunnel --url ssh://localhost:22 --logfile ./cloudflared.log --metrics localhost:45678")
    print("end")
#