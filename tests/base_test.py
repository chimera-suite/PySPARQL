# -*- coding: utf-8 -*-

from pyspark.sql.session import SparkSession
from PySPARQL.Wrapper import PySPARQLWrapper

class BaseTest(object):
    wrapper = None
    sparql_endpoint = "http://jena-fuseki:3030/ds/sparql"

    def setup_method(self):
        spark = SparkSession.builder.getOrCreate()
        wrapper = PySPARQLWrapper(spark, self.sparql_endpoint)
        self.spark = spark
        self.wrapper = wrapper

    def teardown_method(self):
        self.spark.stop()
        self.spark = None
        self.wrapper = None

    def _assert_dataframe_equal(self, first, second):
        assert first.schema == second.schema
        sorted_first = first.sort(first.schema.names).select(sorted(first.columns))
        sorted_second = second.sort(second.schema.names).select(sorted(second.columns))
        assert sorted_first.collect() == sorted_second.collect()
    
