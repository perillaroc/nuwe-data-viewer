# coding: utf-8
import yaml
from enum import Enum

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PyQt5.QtCore import Qt, QFileInfo, QModelIndex

from .ui.UI_mainwindow import Ui_MainWindow
from .ui.file_content_widget import FileContentWidget
from nuwe_data_viewer.lib.core.project_model import ProjectModel
from nuwe_data_viewer.lib.core.file_content_model import FileContentModel
from nuwe_data_viewer.lib.core.message_content_model import MessageContentModel


class FileContentItemModel(Enum):
    MESSAGE_COUNT = Qt.UserRole + 201


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # ui
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.central_widget = None

        # connection
        self.ui.action_open.triggered.connect(self.on_open_file)
        self.ui.action_exit.triggered.connect(self.close)

        # variable
        self.config = None
        self.project_model = ProjectModel(self.config, self)

        # init views
        from .views.project_view_widget import ProjectViewWidget
        self.project_view_widget = ProjectViewWidget(self)
        self.project_view_widget.set_project_model(self.project_model)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.project_view_widget)
        self.project_view_widget.signal_grib_file_clicked.connect(self.slot_file_clicked)

    def load_config(self, config_file):
        with open(config_file) as f:
            config = yaml.load(f)
            self.config = config
            self.project_model.config = self.config
            self.file_content_model.config = self.config
            self.message_content_model.config = self.config

    @pyqtSlot(bool)
    def on_open_file(self, checked):
        file_path, file_type = QFileDialog.getOpenFileName(self, "Open a grib2 file")
        print("file path", file_path)
        self.project_view_widget.add_file(file_type, file_path)

    @pyqtSlot(QFileInfo)
    def slot_file_clicked(self, file_info: QFileInfo):
        file_content_widget = FileContentWidget(self.config, self)
        self.setCentralWidget(file_content_widget)
        file_content_widget.set_file_info(file_info)

