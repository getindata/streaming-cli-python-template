FROM registry.ververica.com/v2.9/flink:1.15.3-stream1-scala_2.12-java8

USER root

RUN pip install pipenv

USER flink

COPY ./Pipfile ./Pipfile.lock /flink/opt/

RUN set -ex && \
    cd /flink/opt && \
    pipenv requirements > requirements.txt && \
    pip install -r requirements.txt

COPY ./src /app/src
COPY .streaming_config.yml ./jars/* /app/lib/