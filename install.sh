#!/bin/bash
set -ex
mkdir /app
cd /app
pip3 install requests
yum install sudo procps wget openssh-server passwd -y
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-x86_64.rpm
rpm -i cloudflared-linux-x86_64.rpm
# mkdir -p /var/run/sshd
# ssh-keygen -A
mkdir /root/.ssh/
echo root | passwd --stdin root

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
EOF
ls -la /app
# echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config
# echo "UsePrivilegeSeparation no" >> /etc/ssh/sshd_config
# cp /etc/ssh/sshd_config sshd_config
# chmod 777 sshd_config

echo Done