# coding: utf-8
from enum import Enum

from PyQt5.QtCore import pyqtSlot, pyqtSignal, QFileInfo, Qt, QModelIndex
from PyQt5.QtWidgets import QDockWidget
from PyQt5.QtGui import QStandardItemModel, QStandardItem

from .UI_project_view_widget import Ui_ProjectViewWidget


class FileType(Enum):
    FILE_INFO = Qt.UserRole + 101


class ProjectViewWidget(QDockWidget):
    signal_file_clicked = pyqtSignal(QFileInfo)

    def __init__(self, parent=None):
        super(QDockWidget, self).__init__(parent)

        self.ui = Ui_ProjectViewWidget()
        self.ui.setupUi(self)
        self.project_model = None

        self.ui.project_view.clicked.connect(self.slot_project_view_clicked)

    def set_project_model(self, project_model: QStandardItemModel):
        self.project_model = project_model
        self.ui.project_view.setModel(self.project_model)

    def add_file(self, file_type, file_path):
        file_info = QFileInfo(file_path)
        file_item = QStandardItem(file_info.fileName())
        file_item.setData(file_info, FileType.FILE_INFO.value)
        self.project_model.appendRow(file_item)

    @pyqtSlot(QModelIndex)
    def slot_project_view_clicked(self, index: QModelIndex):
        item = self.project_model.itemFromIndex(index)
        file_info = item.data(FileType.FILE_INFO.value)
        self.signal_file_clicked.emit(file_info)
