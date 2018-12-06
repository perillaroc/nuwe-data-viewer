# coding: utf-8


class ParameterIndex(object):
    def __init__(self):
        pass


class Grib2ParameterIndex(ParameterIndex):
    def __init__(self, discipline, category, number):
        ParameterIndex.__init__(self)
        self.discipline = discipline
        self.category = category
        self.number = number
