# coding: utf-8
from PyQt5.QtGui import QStandardItem
from nuwe_data_viewer.lib.util.id import Id


class Node(QStandardItem):
    def __init__(self, text="", node_id: Id = None):
        QStandardItem.__init__(self, text)
        if node_id is None:
            node_id = Id()
        self.node_id = node_id
