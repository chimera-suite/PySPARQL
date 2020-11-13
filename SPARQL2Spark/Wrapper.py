from SPARQLWrapper import SPARQLWrapper
from SPARQLWrapper.Wrapper import JSONLD, CSV
from SPARQLWrapper.Wrapper import SELECT, CONSTRUCT

from .SelectResult import SPARQL2SparkSelectResult
from .ConstructResult import SPARQL2SparkConstructResult

class SPARQL2SparkWrapper:
    """This is a wrapper class that allows to query a SPARQL endpoint and 
    process the results as a Spark DataFrame or as a GraphFrame.

    :param spark: An existing spark session.
    :type spark: :class:`pyspark.sql.SparkSession`
    :param sparql_endpoint: The SPARQL endpoint to be queried.
    :type sparql_endpoint: string
    """

    def __init__(self, spark, sparql_endpoint):
        """ Constructor
        """

        self.__spark = spark
        self.__SPARQLWrapper = SPARQLWrapper(sparql_endpoint)
        
    def query(self, query):
        """Executes the query against the SPARQL endpoind and, depending on 
        the query type, returns a :class:`SPARQL2Spark.SelectResult.SPARQL2SparkSelectResult` or a
        :class:`SPARQL2Spark.SelectResult.SPARQL2SparkConstructResult`.

        :param query: A string representing the SPARQL query to be executed
        :type query: string
        :raises Exception: when the query type is not supported
        :rtype: :class:`SPARQL2Spark.SelectResult.SPARQL2SparkSelectResult` or
            :class:`SPARQL2Spark.ConstructResult.SPARQL2SparkConstructResult`
        
        """

        query_type = self.__SPARQLWrapper._parseQueryType(query)
        
        if query_type == SELECT:
            return self.select(query)
        elif query_type == CONSTRUCT:
            return self.construct(query)
        else:
            raise Exception("{} query type not supported!".format(query_type))
        
    def select(self, query):
        """Executes the `select` query against the SPARQL endpoind.

        :param query: A string representing the `select` SPARQL query 
            to be executed
        :type query: string
        :rtype: :class:`SPARQL2Spark.SelectResult.SPARQL2SparkSelectResult`
        """

        self.__SPARQLWrapper.resetQuery()
        self.__SPARQLWrapper.setReturnFormat(CSV)
        self.__SPARQLWrapper.setQuery(query)
        sparql_result = self.__SPARQLWrapper.query().convert()
        return SPARQL2SparkSelectResult(self.__spark, sparql_result)
        
    def construct(self, query):
        """Executes the `construct` query against the SPARQL endpoind.

        :param query: A string representing the `construct` SPARQL query 
            to be executed
        :type query: string
        :rtype: :class:`SPARQL2Spark.ConstructResult.SPARQL2SparkConstructResult`
        """
        self.__SPARQLWrapper.resetQuery()
        self.__SPARQLWrapper.setReturnFormat(JSONLD)
        self.__SPARQLWrapper.setQuery(query)
        sparql_result = self.__SPARQLWrapper.query().convert()
        return SPARQL2SparkConstructResult(self.__spark, sparql_result)

