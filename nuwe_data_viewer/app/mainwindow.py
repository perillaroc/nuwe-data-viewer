# coding: utf-8
import yaml
from enum import Enum

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMdiSubWindow
from PyQt5.QtCore import Qt, QFileInfo

from .ui.UI_mainwindow import Ui_MainWindow
from nuwe_data_viewer.app.widgets.file_content_widget import FileContentWidget
from nuwe_data_viewer.app.widgets.file_visual_widget import FileVisualWidget
from nuwe_data_viewer.lib.project_explorer.model.project_model import ProjectModel


class FileContentItemModel(Enum):
    MESSAGE_COUNT = Qt.UserRole + 201


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # ui
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # connection
        self.ui.action_open_grib2_file.triggered.connect(self.on_open_grib2_file)
        self.ui.action_exit.triggered.connect(self.close)

        # variable
        self.config = None
        self.project_model = ProjectModel(self.config, parent=self)

        # init views
        from nuwe_data_viewer.lib.project_explorer.project_view_widget import ProjectViewWidget
        self.project_view_widget = ProjectViewWidget(self)
        self.project_view_widget.set_project_model(self.project_model)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.project_view_widget)
        self.project_view_widget.signal_grib_file_clicked.connect(self.slot_file_clicked)
        self.project_view_widget.signal_grib_file_show_chart_clicked.connect(self.slot_file_show_chart_clicked)

    def load_config(self, config_file):
        with open(config_file) as f:
            config = yaml.load(f)
            self.config = config
            self.project_model.config = self.config

    def add_mdi_sub_window(self, sub_window: QMdiSubWindow):
        self.ui.central_mdi_area.addSubWindow(sub_window)

    @pyqtSlot(bool)
    def on_open_grib2_file(self, checked):
        file_path, file_type = QFileDialog.getOpenFileName(self, "Open a grib2 file")
        print("file path", file_path)
        self.project_view_widget.add_file(file_type, file_path)

    @pyqtSlot(QFileInfo)
    def slot_file_clicked(self, file_info: QFileInfo):
        file_content_widget = FileContentWidget(self.config, self)
        file_content_sub_window = QMdiSubWindow(self)
        file_content_sub_window.setWidget(file_content_widget)
        self.add_mdi_sub_window(file_content_sub_window)
        file_content_sub_window.show()
        file_content_widget.set_file_info(file_info)

    @pyqtSlot(QFileInfo)
    def slot_file_show_chart_clicked(self, file_info: QFileInfo):
        file_visual_widget = FileVisualWidget(self.config, self)
        file_visual_sub_window = QMdiSubWindow(self)
        file_visual_sub_window.setWidget(file_visual_widget)
        self.add_mdi_sub_window(file_visual_sub_window)
        file_visual_sub_window.show()
        file_visual_widget.set_file_info(file_info)

