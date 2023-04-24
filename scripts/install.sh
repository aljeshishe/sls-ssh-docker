#!/bin/bash
set -ex

mkdir -p /app 
cd /app

apt update && DEBIAN_FRONTEND=noninteractive apt install sudo procps wget openssh-server passwd rpm -y
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -O cloudflared
chmod +x cloudflared
mkdir -p /var/run/sshd
echo root:root | chpasswd

ssh-keygen -f /app/ssh_host_rsa_key -N '' -t rsa

cat << EOF > sshd_config
Port 2222
HostKey /app/ssh_host_rsa_key
# HostKey /app/ssh_host_dsa_key
AuthorizedKeysFile  ~/.ssh/authorized_keys
ChallengeResponseAuthentication no
UsePAM yes
Subsystem   sftp    /usr/lib/ssh/sftp-server
PidFile sshd.pid
PermitRootLogin yes
EOF

echo Done
