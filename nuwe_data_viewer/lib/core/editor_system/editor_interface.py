# coding: utf-8
from PyQt5.QtCore import QObject


class EditorInterface(QObject):
    def __init__(self, parent=None):
        QObject.__init__(self, parent)
        self.widget = None
