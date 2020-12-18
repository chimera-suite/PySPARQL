PySPARQLWrapper
===================

|Documentation Status|

This is a simple module that allows developer to query SPARQL endpoints
and analyze the results with Apache Spark. In particular, if a
**SELECT** query is used, a **DataFrame** is returned, while if a
**CONSTRUCT** query is used, a **GraphFrame** is returned. You can find
the documentation `here <https://PySPARQL.readthedocs.io/>`__.

Build
-----

To generate a ``.whl`` file just type ``make build``, and the file will
be generated under ``dist`` folder.

Test
----

To properly test the library a SPARQL endpoint is needed. Navigate to
``deplyoment`` folder and start a Jena-Fuseky component with the command
``docker-compose up -d``. A simple, hand made, **FOAF** ontology with
few individuals is loaded in Jena-Fuseki. You are encouraged to
experiment with the SPARQL endpoint availabe at
`localhost <http://localhost:3030>`__.

After starting Jena-Fuseki, navigate back to the main folder, and type
``make docker-test`` to start the test phase.

Please, feel free to add more tests and open a pull request 😁

.. |Documentation Status| image:: https://readthedocs.org/projects/PySPARQL/badge/?version=latest
   :target: https://PySPARQL.readthedocs.io/en/latest/?badge=latest
