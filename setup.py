from setuptools import setup

with open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(name='PySPARQL',
      version='0.0.5',
      description='SPARQL Result to Spark',
      author='Emanuele Falzone',
      author_email='emanuele.falzone@polimi.it',
      long_description=long_description,
      install_requires=['rdflib','rdflib-jsonld','sparqlwrapper','graphframes','pyspark'],
      packages=['PySPARQL'],
      classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
      ],
      python_requires='>=3.6',)