# coding: utf-8
from PyQt5.QtCore import Qt
from .node import Node


class FieldNode(Node):
    FileInfoRole = Qt.UserRole + 511

    def __init__(self, text=""):
        Node.__init__(self, text)
