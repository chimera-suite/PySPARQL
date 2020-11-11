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

# 4. SPARK
# Install Apache Spark using pip
RUN pip install pyspark==2.4.5

# 5 
# Download graphframes jar
RUN wget --directory-prefix /jars http://dl.bintray.com/spark-packages/maven/graphframes/graphframes/0.7.0-spark2.4-s_2.11/graphframes-0.7.0-spark2.4-s_2.11.jar