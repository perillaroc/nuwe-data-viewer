# coding: utf-8
from PyQt5.QtWidgets import QWidget


class EditorView(QWidget):
    def __init__(self, parent_editor_area, parent=None):
        QWidget.__init__(self, parent)
        self.parent_editor_area = parent_editor_area
        self.editor = None
