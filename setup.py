from setuptools import setup

setup(name='SPARQL2Spark',
      version='0.0.2',
      description='SPARQL Result to Spark',
      author='Emanuele Falzone',
      author_email='emanuele.falzone@polimi.it',
      install_requires=['rdflib','rdflib-jsonld','sparqlwrapper','graphframes','pyspark'],
      packages=['SPARQL2Spark'],
      zip_safe=False)