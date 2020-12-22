from setuptools import setup

with open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(name='PySPARQL',
      version='0.0.6',
      description='Query a SPARQL endpoint and manage the result with Spark',
      author='Emanuele Falzone',
      author_email='emanuele.falzone@polimi.it',
      long_description=long_description,
      url = "https://github.com/chimera-suite/PySPARQL",
      install_requires=['rdflib','rdflib-jsonld','sparqlwrapper','graphframes'],
      packages=['PySPARQL'],
      classifiers=[
            "Programming Language :: Python :: 3",
            "Operating System :: OS Independent",
      ],
      python_requires='>=3.6',)