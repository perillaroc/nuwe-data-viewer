# coding: utf-8
from .node import Node


class ProjectNode(Node):
    def __init__(self, project_name):
        Node.__init__(self, project_name)
