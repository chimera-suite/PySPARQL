from pyspark.sql.types import StructType, StructField, StringType
from csv import DictReader
from io import StringIO

class PySPARQLSelectResult:
    """This is a class representation of the result of a `select` query.
    In particular, it has property that return the results as a DataFrame.
    """

    def __init__(self, spark, sparql_result):
        self.spark = spark
        self.sparql_result = sparql_result
        
    @property
    def dataFrame(self):
        """A DataFrame of representing the result of the select query.
        The columns represent the variables selected in the query. 

        :type: :class:`pyspark.sql.DataFrame`
        """

        memory_file = StringIO(initial_value=self.sparql_result.decode('utf-8'), newline='\n')
        reader = DictReader(memory_file)

        schema = StructType(
            list(map(lambda f: StructField(f, StringType()), reader.fieldnames))
        )

        data = list(map(lambda d: [d[f] for f in reader.fieldnames], list(reader)))

        return self.spark.createDataFrame(data, schema)