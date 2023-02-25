#!/bin/bash
set -ex
/usr/sbin/sshd -f /app/sshd_config -e
cloudflared tunnel --url ssh://localhost:65432 --logfile /tmp/cloudflared.log --metrics localhost:45678 &
