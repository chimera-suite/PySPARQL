*******
Example
*******

Select
######

This is a simple select example::

    from pyspark.context import SparkContext
    from pyspark.sql.session import SparkSession
    from SPARQL2Spark.Wrapper import SPARQL2SparkWrapper

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
    result = wrapper.query(query)
    resultDF = result.dataFrame

NOTE: the graphframe module needs the `graphframe jar <http://dl.bintray.com/spark-packages/maven/graphframes/graphframes/0.7.0-spark2.4-s_2.11/graphframes-0.7.0-spark2.4-s_2.11.jar>`_ to be included in the CLASSPATH of Spark.