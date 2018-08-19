# coding: utf-8
import yaml
from enum import Enum

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt, QFileInfo, QModelIndex

from .ui.UI_mainwindow import Ui_MainWindow
from nuwe_data_viewer.lib.core.project_model import ProjectModel
from nuwe_data_viewer.lib.core.file_content_model import FileContentModel
from nuwe_data_viewer.lib.core.message_content_model import MessageContentModel
from nuwe_data_viewer.lib.core.grib_meta_data import GribMetaData


class FileContentItemModel(Enum):
    MESSAGE_COUNT = Qt.UserRole + 201


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # ui
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.table_viewer_splitter.setStretchFactor(0, 1)
        self.ui.table_viewer_splitter.setStretchFactor(1, 3)

        # connection
        self.ui.action_open.triggered.connect(self.on_open_file)
        self.ui.action_exit.triggered.connect(self.close)
        self.ui.file_content_widget.clicked.connect(self.slot_file_content_view_clicked)

        # variable
        self.config = None
        self.project_model = ProjectModel(self.config, self)
        self.file_info = None
        self.file_content_model = FileContentModel(self.config, self)
        self.message_content_model = MessageContentModel(self.config, self)

        self.ui.file_content_widget.setModel(self.file_content_model)

        # init views
        from .views.project_view_widget import ProjectViewWidget
        self.project_view_widget = ProjectViewWidget(self)
        self.project_view_widget.set_project_model(self.project_model)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.project_view_widget)
        self.project_view_widget.signal_file_clicked.connect(self.slot_file_clicked)

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
        self.file_info = file_info
        self.file_content_model.set_file_info(file_info)

    @pyqtSlot(QModelIndex)
    def slot_file_content_view_clicked(self, model_index):
        number_item = self.file_content_model.item(model_index.row(), 0)
        message_number = number_item.text()

        stdout = self.message_content_model.set_message(self.file_info, message_number)
        self.ui.message_content_widget.setText(stdout)

