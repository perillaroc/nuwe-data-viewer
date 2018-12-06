# coding: utf-8
import os
import pathlib

from .parameter import Parameter


class ParameterDatabase(object):
    def __init__(self):
        self.parameters = list()

    def add_parameter(self, parameter: Parameter):
        self.parameters.append(parameter)

    @classmethod
    def create_from_definition(cls, table_version=4, eccodes_definition_path=None):
        if eccodes_definition_path is None:
            if 'ECCODES_DEFINITION_PATH' in os.environ:
                eccodes_definition_path = os.environ['ECCODES_DEFINITION_PATH']
        if eccodes_definition_path is None:
            print('ECCODES_DEFINITION_PATH is not set')
            return None

        table_directory = pathlib.Path(
            eccodes_definition_path,
            './grib2/tables/{table_version}'.format(table_version=table_version))

        if not table_directory.exists():
            print("table_directory doesn't exist")
            return None

        db = ParameterDatabase()
        return db
