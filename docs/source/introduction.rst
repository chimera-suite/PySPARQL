************
Introduction
************

This is a simple module that allows developer to query SPARQL endpoints and analyze the results with Apache Spark.
In particular, if a `SELECT` query is used, a `DataFrame` is returned, while if a `CONSTRUCT` query is used, a `GraphFrame` is returned.
