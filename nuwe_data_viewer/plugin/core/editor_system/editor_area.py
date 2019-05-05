# coding: utf-8
from PyQt5.QtWidgets import QWidget, QStackedLayout, QSizePolicy


class EditorArea(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.splitter = None
        self.view = None
        self.layout = QStackedLayout(self)
        self.setLayout(self.layout)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.setStyleSheet("background-color: rgb(50, 60, 80);")

    def set_current_view(self, editor_view):
        self.view = editor_view
        self.layout.addWidget(self.view)
