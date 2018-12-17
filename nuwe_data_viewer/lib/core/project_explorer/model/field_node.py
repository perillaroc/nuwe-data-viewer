# coding: utf-8
from .node import Node


class FieldNode(Node):
    def __init__(self, text=""):
        Node.__init__(self, text)
