#!/bin/bash
set -ex

mkdir -p /app 
cd /app

apt update && DEBIAN_FRONTEND=noninteractive apt install sudo procps wget openssh-server passwd rpm -y
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -O cloudflared
chmod +x cloudflared
mkdir -p /var/run/sshd
# ssh-keygen -A
# mkdir /root/.ssh/
echo root:root | chpasswd

ssh-keygen -f /app/ssh_host_rsa_key -N '' -t rsa
# ssh-keygen -f /app/ssh_host_dsa_key -N '' -t dsa

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
ls -la /app
# echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config
# echo "UsePrivilegeSeparation no" >> /etc/ssh/sshd_config
# cp /etc/ssh/sshd_config sshd_config
# chmod 777 sshd_config

echo Done


# now run 
# /usr/sbin/sshd -f /app/sshd_config -e && ./cloudflared tunnel --url ssh://localhost:2222 --logfile /tmp/cloudflared.log --metrics localhost:45678 &
