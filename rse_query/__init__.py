# Future directions
# Wrappare GraphFrame in una classe che nasconda le complessità di accesso al dato (nome colonne encodato in base 64 e accesso a campo value di una struct) tramite metodi

from SPARQLWrapper import *
from rdflib import *
from graphframes import *
from pyspark.sql import *
from pyspark.sql.types import *
import io
import csv
import json
import base64

def perform_select (spark,endpoint_url, query):

#Le URI sono mantenute complete in questo caso  
#TODO: concordare con rse il da farsi
  sparql = SPARQLWrapper(endpoint_url)
  sparql.setQuery(query)
  sparql.setReturnFormat(CSV)
  results = sparql.query().convert()

  sStr = io.StringIO(initial_value=results.decode('utf-8'), newline='\n')

  cReader = csv.DictReader(sStr)

  fn = list()
  for s in cReader.fieldnames:
    fn.append(StructField(s, StringType()))

  cSchema = StructType(fn)

  elements = list()
  for row in cReader:
    innerEl = list()
    for s in cReader.fieldnames:
      innerEl.append(row[s])
    elements.append(innerEl)
    
  selectDF = spark.createDataFrame(elements,cSchema)

  print(selectDF.columns)
  
  return selectDF

def perform_construct (spark,endpoint_url, query):
  
  sparql = SPARQLWrapper(endpoint_url)
  sparql.setQuery(query)
  sparql.setReturnFormat(JSONLD)
  results = sparql.query().convert()

  #Extract literals for the vertices
  verticesGraph = results.query("""
  CONSTRUCT {
      ?s ?p ?o
  }
  WHERE {
      ?s ?p ?o
      FILTER (isLiteral(?o))
  }
  """)
  verticesString = verticesGraph.serialize(format='json-ld').decode("utf-8").replace("@","")
  verticesDF = spark.read.json(spark.sparkContext.parallelize([verticesString]))

  for column in verticesDF.columns:
    if column.find('@') >= 0:
      newColumn = column[1:]
    elif column == "id":
      newColumn = column
    else :
      newColumn = base64.b16encode(column)
    verticesDF = verticesDF.withColumnRenamed(column, newColumn)

  #Extract nonliterals for the edges

  class Edge:
    def __init__(self, source, destination, relationship):
      self.src = source
      self.dst = destination
      self.relationship = relationship
    def __str__(self):
      return self.source + "," + self.destination + "," + self.relationship
  cSchema = StructType([StructField("src", StringType()),StructField("dst", StringType()),StructField("relationship", StringType())])
  edges = results.query("""
  SELECT ?s ?p ?o
  WHERE {
      ?s ?p ?o
      FILTER (!isLiteral(?o))
  }
  """)
  l=list()

  for row in edges:
    rel = str(row[Variable("p")])
    rel = base64.b16encode(rel)
    l.append(Edge(str(row[Variable("s")]), str(row[Variable("o")]), rel))

  edgesDF = spark.createDataFrame(l,schema=cSchema) 

  print(verticesDF.columns)

  print(verticesDF.columns)
  print(edgesDF.columns)

  return GraphFrame(verticesDF, edgesDF)