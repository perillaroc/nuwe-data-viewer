# coding: utf-8
from PyQt5.QtWidgets import QWidget, QGridLayout
from .editor_area import EditorArea


class EditorWindow(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.edit_area = EditorArea()
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.edit_area)

    def set_title(self, title):
        self.setWindowTitle(title)
