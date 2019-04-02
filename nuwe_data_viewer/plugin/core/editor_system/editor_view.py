# coding: utf-8
from PyQt5.QtWidgets import QWidget, QStackedLayout


class EditorView(QWidget):
    def __init__(self, parent_editor_area, parent=None):
        QWidget.__init__(self, parent)
        self.parent_editor_area = parent_editor_area
        self.layout = QStackedLayout()
        self.setLayout(self.layout)
        self.editor = None

    def set_editor(self, editor):
        self.editor = editor
        self.layout.addWidget(editor.widget)
