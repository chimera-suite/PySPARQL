# .PHONY defines parts of the makefile that are not dependant on any specific file
# This is most often used to store functions
.PHONY = help build test test-all

# Defines the default target that `make` will to try to make, or in the case of a phony target, execute the specified commands
# This target is executed whenever we just type `make`
.DEFAULT_GOAL = help

# The @ makes sure that the command itself isn't echoed in the terminal
help:
	@echo "---------------HELP-----------------"
	@echo "To build the project type make build"
	@echo "To test the project type make test-all"
	@echo "------------------------------------"

build:
	python setup.py sdist 

publish:
	twine upload dist/*
	
test: 
	docker build \
		--build-arg "APACHE_SPARK_VERSION=${APACHE_SPARK_VERSION}" \
		--build-arg "HADOOP_VERSION=${HADOOP_VERSION}" \
		--build-arg "GRAPHFRAME_VERSION=${GRAPHFRAME_VERSION}" \
		--tag "pysparql-test:${APACHE_SPARK_VERSION}-${HADOOP_VERSION}-${GRAPHFRAME_VERSION}" \
		.
		
	docker run \
		--network="test_network" \
		"pysparql-test:${APACHE_SPARK_VERSION}-${HADOOP_VERSION}-${GRAPHFRAME_VERSION}"

test-all:
	make test APACHE_SPARK_VERSION=2.4.0 HADOOP_VERSION=2.7 GRAPHFRAME_VERSION=0.8.1-spark2.4-s_2.11
	make test APACHE_SPARK_VERSION=2.4.1 HADOOP_VERSION=2.7 GRAPHFRAME_VERSION=0.8.1-spark2.4-s_2.11
	make test APACHE_SPARK_VERSION=2.4.3 HADOOP_VERSION=2.7 GRAPHFRAME_VERSION=0.8.1-spark2.4-s_2.11
	make test APACHE_SPARK_VERSION=2.4.4 HADOOP_VERSION=2.7 GRAPHFRAME_VERSION=0.8.1-spark2.4-s_2.11
	make test APACHE_SPARK_VERSION=2.4.5 HADOOP_VERSION=2.7 GRAPHFRAME_VERSION=0.8.1-spark2.4-s_2.11
	make test APACHE_SPARK_VERSION=3.0.0 HADOOP_VERSION=3.2 GRAPHFRAME_VERSION=0.8.1-spark3.0-s_2.12
	make test APACHE_SPARK_VERSION=3.0.1 HADOOP_VERSION=3.2 GRAPHFRAME_VERSION=0.8.1-spark3.0-s_2.12
