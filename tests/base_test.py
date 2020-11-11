# -*- coding: utf-8 -*-

from pyspark.context import SparkConf, SparkContext
from pyspark.sql.session import SparkSession
from SPARQL2Spark import SPARQL2SparkWrapper

class BaseTest(object):
    wrapper = None
    sparql_endpoint = "http://jena-fuseki:3030/ds/sparql"

    def setup_method(self):
        sparkConf = SparkConf().set("spark.jars", "/jars/graphframes-0.7.0-spark2.4-s_2.11.jar")
        sparkContext = SparkContext(conf=sparkConf)
        spark = SparkSession(sparkContext)
        wrapper = SPARQL2SparkWrapper(spark, self.sparql_endpoint)
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
    
