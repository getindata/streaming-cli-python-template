from typing import Iterable, List

from pyflink.datastream.stream_execution_environment import StreamExecutionEnvironment
from pyflink.table import DataTypes, StreamTableEnvironment, CsvTableSink, WriteMode


def simple_passthrough_job(t_env: StreamTableEnvironment, elements: Iterable, columns: List[str]):
    return t_env.from_elements(elements, columns)


def main():
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(1)
    t_env = StreamTableEnvironment.create(env)

    field_names = ['a', 'b', 'c']
    field_types = [DataTypes.BIGINT(), DataTypes.STRING(), DataTypes.STRING()]
    sink = CsvTableSink(field_names, field_types, '/tmp/test.csv', write_mode=WriteMode.OVERWRITE)
    t_env.register_table_sink("Results", sink)

    simple_passthrough_job(t_env, [(1, 'Hi', 'Helloo')], ['a', 'b', 'c']).execute_insert("Results").wait()


if __name__ == '__main__':
    main()
