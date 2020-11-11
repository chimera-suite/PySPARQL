from SPARQLWrapper import SPARQLWrapper
from SPARQLWrapper.Wrapper import JSONLD, CSV
from SPARQLWrapper.Wrapper import SELECT, CONSTRUCT

from .SPARQL2SparkSelectResult import SPARQL2SparkSelectResult
from .SPARQL2SparkConstructResult import SPARQL2SparkConstructResult

class SPARQL2SparkWrapper:
    
    def __init__(self, spark, sparql_endpoint):
        self.__spark = spark
        self.__SPARQLWrapper = SPARQLWrapper(sparql_endpoint)
        
    def query(self, query):
        query_type = self.__SPARQLWrapper._parseQueryType(query)
        
        if query_type == SELECT:
            return self.select(query)
        elif query_type == CONSTRUCT:
            return self.construct(query)
        else:
            raise Exception("{} query type not supported!".format(query_type))
        
    def select(self, query):
        self.__SPARQLWrapper.resetQuery()
        self.__SPARQLWrapper.setReturnFormat(CSV)
        self.__SPARQLWrapper.setQuery(query)
        sparql_result = self.__SPARQLWrapper.query().convert()
        return SPARQL2SparkSelectResult(self.__spark, sparql_result).dataFrame
        
    def construct(self, query):
        self.__SPARQLWrapper.resetQuery()
        self.__SPARQLWrapper.setReturnFormat(JSONLD)
        self.__SPARQLWrapper.setQuery(query)
        sparql_result = self.__SPARQLWrapper.query().convert()
        return SPARQL2SparkConstructResult(self.__spark, sparql_result).graphFrame

