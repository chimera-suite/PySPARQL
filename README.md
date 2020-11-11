# SPARQL2SparkWrapper

This is a simple module that allows developer to query SPARQL endpoints and analyze the results with Apache Spark.
In particular, if a __SELECT__ query is used, a __DataFrame__ is returned, while if a __CONSTRUCT__ query is used, a __GraphFrame__ is returned.
You can find the documentation [here]().

## Example

Here is a simple example of a construct query.
```python
from pyspark.context import SparkContext
from pyspark.sql.session import SparkSession
from SPARQL2SparkWrapper import SPARQL2SparkWrapper

sparql_endpoint = "http://jena-fuseki:3030/ds/sparql"

query = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX : <http://www.semanticweb.org/sparql2sparkwrapper/ontologies/foaf#>

    SELECT ?subject ?name ?surname
    WHERE {
    ?gender  rdfs:subClassOf :Person .
    ?subject  rdf:type ?gender ;
            :name ?name ;
            :surname ?surname .
    }
"""

sparkContext = SparkContext.getOrCreate()
spark = SparkSession(sparkContext)
wrapper = SPARQL2SparkWrapper(spark, sparql_endpoint)
output = wrapper.query(query)
```

NOTE: the graphframe module needs the graphframe jar to be included in the CLASSPATH of Spark.
The jar an be easily downloaded from [here](http://dl.bintray.com/spark-packages/maven/graphframes/graphframes/0.7.0-spark2.4-s_2.11/graphframes-0.7.0-spark2.4-s_2.11.jar).


## Build
To generate a `.whl` file just type `make build`, and the file will be generated under `dist` folder.

## Test
To properly test the library a SPARQL endpoint is needed.
Navigate to `deplyoment` folder and start a Jena-Fuseky component with the command `docker-compose up -d`.
A simple, hand made, **FOAF** ontology with few individuals is loaded in Jena-Fuseki.
You are encouraged to experiment with the SPARQL endpoint availabe at [localhost](http://localhost:3030).

After starting Jena-Fuseki, navigate back to the main folder, and type `make docker-test` to start the test phase.

Please, feel free to add more tests and open a pull request 😁

