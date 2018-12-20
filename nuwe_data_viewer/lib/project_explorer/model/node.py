# coding: utf-8
from PyQt5.QtGui import QStandardItem


class Node(QStandardItem):
    def __init__(self, text=""):
        QStandardItem.__init__(self, text)
