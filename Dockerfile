# Short Description: Apache PySpark
# Full Description: The ubuntu:xenial Docker image with Python 3 and Apache PySpark

FROM ubuntu:xenial

USER root

# 1. AP
# Install g++, nano, pigz, wget, make
RUN apt-get -qq update \
        && apt-get install -y g++ nano pigz wget make \
        && apt-get clean

# 2. JAVA
# Install java
RUN apt-get -qq update \
        && apt-get install -y openjdk-8* \
        && apt-get clean

# 3. PYTHON+PIP
# Add deadsnakes repository
RUN apt-get -qq update \
        && apt-get install -y software-properties-common \
        && add-apt-repository ppa:deadsnakes/ppa
# Install python
RUN apt-get -qq update \
        && apt-get install -y python3.6 python3.6-dev python3-pip
# Link python3 to python and pip3 to pip
RUN ln -sfn /usr/bin/python3.6 /usr/bin/python3 \
        && ln -sfn /usr/bin/python3 /usr/bin/python \
        && ln -sfn /usr/bin/pip3 /usr/bin/pip

ARG APACHE_SPARK_VERSION
ARG HADOOP_VERSION
ARG GRAPHFRAME_VERSION

# 4. SPARK
ARG APACHE_SPARK_VERSION
ARG HADOOP_VERSION
ARG GRAPHFRAME_VERSION

# Spark installation
WORKDIR /tmp

RUN wget -q "https://archive.apache.org/dist/spark/spark-${APACHE_SPARK_VERSION}/spark-${APACHE_SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz" && \
    tar xzf "spark-${APACHE_SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz" -C /usr/local && \
    rm "spark-${APACHE_SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz"

WORKDIR /usr/local

RUN ln -s "spark-${APACHE_SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}" spark

# Configure Spark
ENV SPARK_HOME=/usr/local/spark
ENV SPARK_OPTS="--driver-java-options=-Xms1024M --driver-java-options=-Xmx4096M --driver-java-options=-Dlog4j.logLevel=info"
ENV PATH=$PATH:$SPARK_HOME/bin
ENV SPARK_CONF_DIR="${SPARK_HOME}/conf"
ENV PYTHONPATH="${SPARK_HOME}/python:${PYTHONPATH}"
ENV PYTHONPATH="${SPARK_HOME}/python/lib/py4j-0.10.7-src.zip:${PYTHONPATH}"
ENV PYSPARK_PYTHONPATH_SET=1

# Download graphframes jar
RUN wget --directory-prefix /usr/local/spark/jars \
    http://dl.bintray.com/spark-packages/maven/graphframes/graphframes/${GRAPHFRAME_VERSION}/graphframes-${GRAPHFRAME_VERSION}.jar

# 5. PySPARQL
WORKDIR /code/package

COPY PySPARQL PySPARQL
COPY requirements.txt requirements.txt
COPY setup.py setup.py
COPY README.rst README.rst

RUN pip install -r requirements.txt
RUN pip install .

WORKDIR /code

RUN rm -rf package

COPY tests tests

CMD ["pytest"]