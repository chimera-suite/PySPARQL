from pyspark.sql.types import StructType, StructField, StringType
from graphframes import GraphFrame
from rdflib.term import Variable
from pyspark.sql.functions import udf, col, first

@udf
def _escape_udf(s):
    return s.replace(".", "_")

class SPARQL2SparkConstructResult:
    
    __SCHEMA = StructType([
        StructField("subject", StringType()),
        StructField("predicate", StringType()),
        StructField("object", StringType())
    ])
    
    __VERTICES_QUERY = """
    SELECT DISTINCT ?subject ?predicate ?object
    WHERE {
      ?subject ?predicate ?object
      FILTER (isLiteral(?object))
    }
    """

    __EDGES_QUERY = """
    SELECT DISTINCT ?subject ?predicate ?object
    WHERE {
      ?subject ?predicate ?object
      FILTER (!isLiteral(?object))
    }
    """
    
    __QUERY = """
    SELECT DISTINCT ?subject ?predicate ?object
    WHERE {
      ?subject ?predicate ?object
    }
    """
    
    def __init__(self, spark, sparql_result):
        self.spark = spark
        self.sparql_result = sparql_result
        
    def __to_dataframe(self, sparql_result):
        
        def __term_to_string(sparql_row): 
            return [
                str(sparql_row[Variable("subject")]),
                str(sparql_row[Variable("predicate")]),
                str(sparql_row[Variable("object")])
            ]
    
        data = list(map(__term_to_string, sparql_result))
        return self.spark.createDataFrame(data, schema=self.__SCHEMA)
 
        
    @property
    def dataFrame(self):
        sparql_result = self.sparql_result.query(self.__QUERY)
        return self.__to_dataframe(sparql_result)
    
    @property
    def verticesDataFrame(self):
        vertices_sparql_result = self.sparql_result.query(self.__VERTICES_QUERY)
        return self.__to_dataframe(vertices_sparql_result) \
            .withColumn("predicate", _escape_udf(col("predicate"))) \
            .groupby("subject") \
            .pivot("predicate") \
            .agg(first("object")) \
            .withColumnRenamed("subject", "id")

    @property
    def edgesDataFrame(self):
        edges_sparql_result = self.sparql_result.query(self.__EDGES_QUERY)
        return self.__to_dataframe(edges_sparql_result) \
            .withColumnRenamed("subject", "src") \
            .withColumnRenamed("object", "dst") \
            .withColumnRenamed("predicate", "relationship")
    
    @property
    def graphFrame(self):
        return GraphFrame(
            self.verticesDataFrame, 
            self.edgesDataFrame
        )