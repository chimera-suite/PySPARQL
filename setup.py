from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(name='SPARQL2Spark',
      version='0.0.3',
      description='SPARQL Result to Spark',
      author='Emanuele Falzone',
      author_email='emanuele.falzone@polimi.it',
      long_description=long_description,
      long_description_content_type="text/markdown",
      install_requires=['rdflib','rdflib-jsonld','sparqlwrapper','graphframes','pyspark'],
      packages=['SPARQL2Spark'],
      classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
      ],
      python_requires='>=3.6',)