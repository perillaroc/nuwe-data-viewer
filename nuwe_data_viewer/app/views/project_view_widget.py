# coding: utf-8

from PyQt5.QtCore import pyqtSlot, pyqtSignal, QFileInfo, QModelIndex
from PyQt5.QtWidgets import QDockWidget

from .UI_project_view_widget import Ui_ProjectViewWidget
from nuwe_data_viewer.lib.core.project_model import ProjectModel, ProjectItemType, ProjectModelDataType


class ProjectViewWidget(QDockWidget):
    signal_file_clicked = pyqtSignal(QFileInfo)

    def __init__(self, parent=None):
        super(QDockWidget, self).__init__(parent)

        self.ui = Ui_ProjectViewWidget()
        self.ui.setupUi(self)
        self.project_model = None

        self.ui.project_view.clicked.connect(self.slot_project_view_clicked)

    def set_project_model(self, project_model: ProjectModel):
        self.project_model = project_model
        self.ui.project_view.setModel(self.project_model)

    def add_file(self, file_type, file_path):
        self.project_model.add_item(ProjectItemType.GribFile, {
            'file_path': file_path
        })

    @pyqtSlot(QModelIndex)
    def slot_project_view_clicked(self, index: QModelIndex):
        item = self.project_model.itemFromIndex(index)
        file_info = item.data(ProjectModelDataType.FileInfoType.value)
        self.signal_file_clicked.emit(file_info)
