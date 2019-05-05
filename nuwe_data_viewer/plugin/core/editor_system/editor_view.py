# coding: utf-8
from PyQt5.QtWidgets import QWidget, QStackedLayout


class EditorView(QWidget):
    def __init__(self, parent_editor_area, parent=None):
        super(EditorView, self).__init__(parent)
        self.parent_editor_area = parent_editor_area
        from .UI_editor_view import Ui_EditorView
        self.ui = Ui_EditorView()
        self.ui.setupUi(self)

        self.editor = None

    def set_editor(self, editor):
        self.editor = editor
        self.ui.container.addWidget(editor.widget)
        self.ui.container.setCurrentWidget(editor.widget)
