# coding: utf-8


class TableRecord(object):
    def __init__(self):
        self.code_ = None
        self.figure_ = None
        self.description = None


class Grib2TableDatabase(object):
    def __init__(self):

        self.disciplines = list()
        self.categories = list()
        self.numbers = list()

        self.table_version = 4
        self.definition_path = None
