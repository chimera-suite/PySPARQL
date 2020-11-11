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
# Install python
RUN apt-get -qq update \
        && apt-get install -y python3 \
        && apt-get clean
# Link python3 to python
RUN ln -s /usr/bin/python3 /usr/bin/python
# Download get-pip.py file to '/tmp' directory
RUN wget --directory-prefix /tmp https://bootstrap.pypa.io/get-pip.py
# Install pip
RUN python /tmp/get-pip.py
# Remove '/tmp/get-pip.py' file
RUN rm /tmp/get-pip.py

# 4. SPARK
# Install Apache Spark using pip
RUN pip install pyspark==2.4.5

# 5 
# Download graphframes jar
RUN wget --directory-prefix /jars http://dl.bintray.com/spark-packages/maven/graphframes/graphframes/0.7.0-spark2.4-s_2.11/graphframes-0.7.0-spark2.4-s_2.11.jar