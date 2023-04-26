#!/bin/bash

OPTIND=1         # Reset in case getopts has been used previously in the shell.

# Initialize our own variables:
password=""
verbose=0
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -p|--password) password="$2"; shift ;;
        -v|--verbose) verbose=1 ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

echo "verbose=$verbose, password='$password', Leftovers: $@"
if [[ -z "$password" ]];
then
    echo "-p or --password option required" 1>&2
    exit 1
fi

if [[ $verbose == 1 ]];
then
    set -ex
else
    set -e
fi



mkdir -p /app 
cd /app

apt update && DEBIAN_FRONTEND=noninteractive apt install sudo procps wget openssh-server passwd rpm -y
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -O cloudflared
chmod +x cloudflared
mkdir -p /var/run/sshd
echo root:$password | chpasswd

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
