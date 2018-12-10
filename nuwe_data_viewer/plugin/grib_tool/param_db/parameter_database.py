# coding: utf-8
import os
import pathlib

from .parameter import Parameter


class ParameterDatabase(object):
    def __init__(self):
        self.parameters = list()

    def add_parameter(self, parameter: Parameter):
        self.parameters.append(parameter)
