# coding: utf-8

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow

from .ui.UI_mainwindow import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = None

        self.init_ui()

    def init_ui(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
