#!/bin/bash
set -ex
mkdir /app
cd /app
pip3 install requests
#yum install sudo procps wget aws-cli -y
#wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
#chmod 777 cloudflared-linux-amd64
#mv cloudflared-linux-amd64 cloudflared
# ./cloudflared-linux-amd64
# wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-x86_64.rpm
# rpm -i cloudflared-linux-x86_64.rpm
ls -la /app
echo Done