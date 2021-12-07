FROM registry.gitlab.com/getindata/streaming-labs/docker-images/vvp-flink-python:1.14.0-java8-python3.8-0.1.2

USER flink

COPY ./Pipfile /flink/opt

RUN set -ex && \
    cd /flink/opt && \
    pipenv lock -r > requirements.txt && \
    pip install -r requirements.txt

COPY ./src /app/src
COPY .streaming_config.yml ./jars/* /app/lib/