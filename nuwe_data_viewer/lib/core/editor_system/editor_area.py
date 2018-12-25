# coding: utf-8
from PyQt5.QtWidgets import QWidget, QStackedLayout

from nuwe_data_viewer.lib.core.editor_system.editor_view import EditorView


class EditorArea(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.splitter = None
        self.view = None
        self.layout = QStackedLayout(self)
        self.setLayout(self.layout)

    def set_current_view(self, editor_view):
        self.view = editor_view
        self.layout.addWidget(self.view)
