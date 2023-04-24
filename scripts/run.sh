#!/bin/bash
set -ex

/usr/sbin/sshd -f /app/sshd_config -e && /app/cloudflared tunnel --url ssh://localhost:2222 --logfile /tmp/cloudflared.log --metrics localhost:45678