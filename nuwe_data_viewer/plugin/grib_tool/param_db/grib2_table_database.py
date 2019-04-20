# coding: utf-8
import os
import pathlib
from nuwe_data_viewer.lib.util.id import Id


class TableRecord(object):
    def __init__(self):
        self.code = None
        self.figure = None
        self.description = None

    def is_valid(self):
        return self.code is not None


class Grib2TableDatabase(object):
    def __init__(self):

        self.disciplines = dict()
        self.categories = dict()
        self.numbers = dict()
        self.level_types = dict()

        self.table_version = 4
        self.definition_path = None

    def read_definition(self, table_version=4, eccodes_definition_path=None):
        if eccodes_definition_path is None:
            if 'ECCODES_DEFINITION_PATH' in os.environ:
                eccodes_definition_path = os.environ['ECCODES_DEFINITION_PATH']
        if eccodes_definition_path is None:
            print('ECCODES_DEFINITION_PATH is not set')
            return
        self.definition_path = eccodes_definition_path

        self.table_version = table_version

        table_directory = pathlib.Path(
            self.definition_path,
            './grib2/tables/{table_version}'.format(table_version=table_version))

        if not table_directory.exists():
            print("table_directory doesn't exist")
            return

        self.clear_database()
        self._read_disciplines()
        self._read_parameter_categories()
        self._read_parameter_numbers()
        self._read_levels()

    def clear_database(self):
        pass

    def _read_disciplines(self):
        table_path = pathlib.Path(self.definition_path, "grib2/tables", str(self.table_version), "0.0.table")
        if not table_path.exists():
            print("table path doesn't exist:", table_path)
            return

        with open(table_path) as table_file:
            for line in table_file:
                line = line.strip()
                if line.startswith('#'):
                    continue

                record = TableRecord()

                tokens = line.split(' ', 2)
                if len(tokens) != 3:
                    continue
                record.code = int(tokens[0])
                record.figure = tokens[1]
                record.description = tokens[2]
                self._save_discipline(record)

    def _read_parameter_categories(self):
        for ticket_id, discipline in self.disciplines.items():
            if discipline.code == 255:
                continue
            self._read_parameter_categories_for_discipline(discipline)

    def _read_parameter_categories_for_discipline(self, discipline: TableRecord):
        table_path = pathlib.Path(
            self.definition_path,
            "grib2/tables",
            str(self.table_version),
            "4.1." + str(discipline.code) + ".table"
        )
        if not table_path.exists():
            print("table path doesn't exist:", table_path)
            return

        with open(table_path) as table_file:
            for line in table_file:
                line = line.strip()
                if line.startswith('#'):
                    continue

                record = TableRecord()

                tokens = line.split(' ', 2)
                if len(tokens) != 3:
                    continue
                record.code = int(tokens[0])
                record.figure = tokens[1]
                record.description = tokens[2]
                self._save_parameter_category(discipline, record)

    def _read_parameter_numbers(self):
        for ticket_id, category in self.categories.items():
            if category.code == 255:
                continue
            discipline_id = Id(ticket_id.name.split('.')[0])
            discipline = self.disciplines[discipline_id]
            self._read_parameter_numbers_for_category(discipline, category)

    def _read_parameter_numbers_for_category(self, discipline: TableRecord, category: TableRecord):
        table_path = pathlib.Path(
            self.definition_path,
            "grib2/tables",
            str(self.table_version),
            "4.2." + str(discipline.code) + "." + str(category.code) + ".table"
        )
        if not table_path.exists():
            print("table path doesn't exist:", table_path)
            return

        with open(table_path) as table_file:
            for line in table_file:
                line = line.strip()
                if line.startswith('#'):
                    continue

                record = TableRecord()

                tokens = line.split(' ', 2)
                if len(tokens) != 3:
                    continue
                record.code = int(tokens[0])
                record.figure = tokens[1]
                record.description = tokens[2]
                self._save_parameter_number(discipline, category, record)

    def _read_levels(self):
        table_path = pathlib.Path(
            self.definition_path,
            "grib2/tables",
            str(self.table_version),
            "4.5.table"
        )
        if not table_path.exists():
            print("table path doesn't exist:", table_path)
            return

        with open(table_path) as table_file:
            for line in table_file:
                line = line.strip()
                if line.startswith('#'):
                    continue

                record = TableRecord()

                tokens = line.split(' ', 2)
                if len(tokens) != 3:
                    continue
                record.code = int(tokens[0])
                record.figure = tokens[1]
                record.description = tokens[2]
                self.level_types[Id(str(record.code))] = record

    def _save_discipline(self, discipline: TableRecord):
        ticket_id = Id("{discipline}".format(discipline=discipline.code))
        self.disciplines[ticket_id] = discipline

    def _save_parameter_category(self, discipline: TableRecord, category: TableRecord):
        ticket_id = Id("{discipline}.{category}".format(discipline=discipline.code, category=category.code))
        self.categories[ticket_id] = category

    def _save_parameter_number(self, discipline: TableRecord, category: TableRecord, number: TableRecord):
        ticket_id = Id("{discipline}.{category}.{number}".format(
            discipline=discipline.code,
            category=category.code,
            number=number.code
        ))
        self.numbers[ticket_id] = number
