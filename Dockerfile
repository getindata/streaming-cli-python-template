FROM flink:1.16-java8

USER root

RUN set -ex && \
    apt update && \
    apt-get install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev \
    libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev wget libbz2-dev && \
    wget https://www.python.org/ftp/python/3.8.12/Python-3.8.12.tgz && \
    tar -xf Python-3.8.12.tgz && \
    rm -rf Python-3.8.12.tgz && \
    cd Python-3.8.12 && \
    ./configure && \
    make -j 8 && \
    make altinstall && \
    ln -s /usr/local/bin/python3.8 /usr/bin/python && \
    ln -s /usr/local/bin/pip3.8 /usr/bin/pip && \
    pip install --upgrade pip && \
    pip install --upgrade setuptools && \
    pip install pipenv && \
    apt-get clean

RUN mkdir -p /flink/opt/ && \
    chown -R flink:flink /flink/opt/ && \
    chown -R flink:flink /opt/flink

USER flink

COPY ./Pipfile ./Pipfile.lock /flink/opt/

RUN set -ex && \
    cd /flink/opt && \
    pipenv install --system

COPY ./src /app/src
COPY .streaming_config.yml ./jars/* /app/lib/