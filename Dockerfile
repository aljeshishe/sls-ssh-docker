# syntax = docker/dockerfile:experimental
FROM public.ecr.aws/lambda/python:3.8


WORKDIR ${LAMBDA_TASK_ROOT}

ADD install2.sh ./
RUN --mount=type=cache,mode=0777,target=/var/cache/yum ./install2.sh
COPY . ./
CMD [ "handler.hello" ]

