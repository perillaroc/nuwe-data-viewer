# coding: utf-8
from .node import Node


class DataNode(Node):
    def __init__(self, text=""):
        Node.__init__(self, text)


class GribFileNode(DataNode):
    def __init__(self, file_name):
        Node.__init__(self, file_name)
        self.file_name = file_name
        self.file_info = None

    def set_file_info(self, file_info):
        self.file_info = file_info
