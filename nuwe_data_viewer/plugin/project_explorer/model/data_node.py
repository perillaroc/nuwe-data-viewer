# coding: utf-8
from .node import Node


class DataNode(Node):
    def __init__(self, display_name="", node_id=None):
        Node.__init__(self, display_name, node_id)


class GribFileNode(DataNode):
    def __init__(self, file_name, node_id=None):
        Node.__init__(self, file_name, node_id)
        self.file_name = file_name
        self.file_info = None
        self.grib_info = None

    def set_file_info(self, file_info):
        self.file_info = file_info
