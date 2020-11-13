# SPARQL2SparkWrapper

[![Documentation Status](https://readthedocs.org/projects/sparql2spark/badge/?version=latest)](https://sparql2spark.readthedocs.io/en/latest/?badge=latest)

This is a simple module that allows developer to query SPARQL endpoints and analyze the results with Apache Spark.
In particular, if a __SELECT__ query is used, a __DataFrame__ is returned, while if a __CONSTRUCT__ query is used, a __GraphFrame__ is returned.
You can find the documentation [here](https://sparql2spark.readthedocs.io/).

## Build
To generate a `.whl` file just type `make build`, and the file will be generated under `dist` folder.

## Test
To properly test the library a SPARQL endpoint is needed.
Navigate to `deplyoment` folder and start a Jena-Fuseky component with the command `docker-compose up -d`.
A simple, hand made, **FOAF** ontology with few individuals is loaded in Jena-Fuseki.
You are encouraged to experiment with the SPARQL endpoint availabe at [localhost](http://localhost:3030).

After starting Jena-Fuseki, navigate back to the main folder, and type `make docker-test` to start the test phase.

Please, feel free to add more tests and open a pull request 😁

