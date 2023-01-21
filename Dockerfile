# syntax = docker/dockerfile:experimental
FROM public.ecr.aws/lambda/python:3.8


WORKDIR ${LAMBDA_TASK_ROOT}

RUN yum install procps wget openssh-server passwd -y && \
    wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-x86_64.rpm && \
    rpm -i cloudflared-linux-x86_64.rpm && \
    mkdir -p /var/run/sshd && \
    ssh-keygen -A && \
    echo root | passwd --stdin root && \
    echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config
COPY handler.py ./
CMD [ "handler.handler" ]

