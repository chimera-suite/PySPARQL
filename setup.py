from setuptools import setup

setup(name='rse',
      version='0.2',
      description='Utilities for rse project',
      author='Marco Balduini',
      author_email='marco.balduini@polimi.it',
      install_requires=['rdflib','rdflib-jsonld','sparqlwrapper'],
      packages=['rse_query'],
      zip_safe=False)