# -*- coding: utf-8 -*-

from tests.base_test import BaseTest

class TestConstruct(BaseTest):
  
    def test_construct(self):
        # GIVEN
        construct_query = """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX : <http://www.semanticweb.org/sparql2sparkwrapper/ontologies/foaf#>

            CONSTRUCT {
            ?wife a :Girl ;
                    :name ?wifeName ;
                    :surname ?wifeSurname ;
                    :friendOf ?friend .
            ?friend a ?friendGender ;
                    :name ?friendName ;
                    :surname ?friendSurname .
            }
            WHERE {
            ?john a :Boy ;
                    :name "John" ;
                    :surname "Doe" ;
                    :marriedWith ?wife ;
                    :friendOf ?friend .
            ?wife :name ?wifeName ;
                    :surname ?wifeSurname .
            ?friend a ?friendGender ;
                    :name ?friendName ;
                    :surname ?friendSurname .
            ?friendGender  rdfs:subClassOf :Person .
            }
        """
        verticesDF = self.spark.createDataFrame(
            [
                (
                    'http://www.semanticweb.org/sparql2sparkwrapper/ontologies/foaf#laura-williams', 
                    'Laura', 
                    'Williams'
                ), 
                (
                    'http://www.semanticweb.org/sparql2sparkwrapper/ontologies/foaf#scott-farrell', 
                    'Scott',
                    'Farrell'
                )
            ],
            [
                'id', 
                'http://www_semanticweb_org/sparql2sparkwrapper/ontologies/foaf#name',
                'http://www_semanticweb_org/sparql2sparkwrapper/ontologies/foaf#surname'
            ]
        )
       
        edgesDF = self.spark.createDataFrame(
            [
                (
                    'http://www.semanticweb.org/sparql2sparkwrapper/ontologies/foaf#scott-farrell', 
                    'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', 
                    'http://www.semanticweb.org/sparql2sparkwrapper/ontologies/foaf#Boy'
                ), 
                (
                    'http://www.semanticweb.org/sparql2sparkwrapper/ontologies/foaf#laura-williams', 
                    'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', 
                    'http://www.semanticweb.org/sparql2sparkwrapper/ontologies/foaf#Girl'
                ), 
                (   'http://www.semanticweb.org/sparql2sparkwrapper/ontologies/foaf#laura-williams',
                    'http://www.semanticweb.org/sparql2sparkwrapper/ontologies/foaf#friendOf', 
                    'http://www.semanticweb.org/sparql2sparkwrapper/ontologies/foaf#scott-farrell'
                )
            ],
            [
                'src', 
                'relationship', 
                'dst'
            ]
        )
        
        # WHEN
        result = self.wrapper.query(construct_query)

        # THEN
        self._assert_dataframe_equal(result.graphFrame.edges, edgesDF)
        self._assert_dataframe_equal(result.graphFrame.vertices, verticesDF )