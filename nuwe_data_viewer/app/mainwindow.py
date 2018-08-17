# coding: utf-8
import yaml
from enum import Enum

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt, QFileInfo

from .ui.UI_mainwindow import Ui_MainWindow
from nuwe_data_viewer.lib.core.grib_meta_data import GribMetaData, key_list


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

        # variable
        self.config = None
        self.project_model = QStandardItemModel(self)
        self.file_content_model = QStandardItemModel(self)
        self.message_content_model = QStandardItemModel(self)

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

    @pyqtSlot(bool)
    def on_open_file(self, checked):
        file_path, file_type = QFileDialog.getOpenFileName(self, "Open a grib2 file")
        print("file path", file_path)
        self.project_view_widget.add_file(file_type, file_path)

    @pyqtSlot(QFileInfo)
    def slot_file_clicked(self, file_info: QFileInfo):
        print(file_info.fileName())
        grib_meta_data = GribMetaData(self.config)
        grib_meta_data.set_file_path(file_info.filePath())
        grib_info = grib_meta_data.get_grib_info()

        self.file_content_model.clear()

        cur_index = 0
        extended_key_list = ['No']
        extended_key_list.extend(key_list)
        self.file_content_model.setColumnCount(len(extended_key_list))
        for a_key in extended_key_list:
            self.file_content_model.setHeaderData(cur_index, Qt.Horizontal, a_key)
            cur_index += 1
        cur_index = 1
        for a_message_info in grib_info:
            message_row = [QStandardItem(str(cur_index))]
            for prop in a_message_info:
                value_item = QStandardItem(prop['value'])
                message_row.append(value_item)
            # message_row[0].setData(cur_index, FileContentItemModel.MESSAGE_COUNT.value)
            self.file_content_model.appendRow(message_row)
            cur_index += 1

