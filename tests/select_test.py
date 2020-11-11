# -*- coding: utf-8 -*-

from tests.base_test import BaseTest

class TestSelect(BaseTest):

    def test_select(self):
        # GIVEN
        select_query = """
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
        selectDF = self.spark.createDataFrame(
            [
                (
                    'http://www.semanticweb.org/sparql2sparkwrapper/ontologies/foaf#john-doe', 
                    'John',
                    'Doe'
                ), 
                (
                    'http://www.semanticweb.org/sparql2sparkwrapper/ontologies/foaf#scott-farrell', 
                    'Scott',
                    'Farrell'), 
                (
                    'http://www.semanticweb.org/sparql2sparkwrapper/ontologies/foaf#freya-bolton', 
                    'Freya',
                    'Bolton'), 
                (
                    'http://www.semanticweb.org/sparql2sparkwrapper/ontologies/foaf#laura-williams', 
                    'Laura',
                    'Williams'
                )
            ],
            [
                'subject', 
                'name',
                'surname'
            ]
        )

        # WHEN
        dataFrame = self.wrapper.query(select_query)

        # THEN
        self._assert_dataframe_equal(dataFrame, selectDF)

        