import unittest
from typing import List

from pyflink.common import Row
from pyflink.table import DataTypes, TableSchema, TableResult
from pyflink.testing.test_case_utils import PyFlinkUTTestCase

from src.flink_app import simple_passthrough_job


class BaseTests(PyFlinkUTTestCase):

    @staticmethod
    def _elements_to_rows(elements: List):
        return [Row(*row) for row in elements]

    @staticmethod
    def _table_result_to_list(table_result: TableResult):
        results = []
        for result in table_result.collect():
            results.append(result)
        return results

    def test_simple_passthrough_job(self):
        columns = ['a', 'b', 'c']
        elements = [(1, 'Hi', 'Hello')]

        expected_schema = TableSchema.Builder()\
            .field("a", DataTypes.BIGINT())\
            .field("b", DataTypes.STRING())\
            .field("c", DataTypes.STRING())\
            .build()

        table_result = simple_passthrough_job(self.t_env, elements, columns).execute()

        self.assertEqual(table_result.get_table_schema(), expected_schema)
        self.assertEqual(self._table_result_to_list(table_result), self._elements_to_rows(elements))


if __name__ == '__main__':
    unittest.main()
