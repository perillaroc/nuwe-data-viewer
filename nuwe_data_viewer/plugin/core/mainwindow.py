# coding: utf-8
from enum import Enum

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt

from nuwe_data_viewer.plugin.core.UI_mainwindow import Ui_MainWindow
from nuwe_data_viewer.plugin.core.editor_system.editor_manager import EditorManager


class FileContentItemModel(Enum):
    MESSAGE_COUNT = Qt.UserRole + 201


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.editor_manager = None

        # ui
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # connection
        self.ui.action_exit.triggered.connect(self.close)

        # variable
        self.config = None

    def load_config(self, config):
        self.config = config

    def set_central_widget(self, widget):
        self.setCentralWidget(widget)

    def set_editor_manager(self, editor_manager: EditorManager):
        self.editor_manager = editor_manager
