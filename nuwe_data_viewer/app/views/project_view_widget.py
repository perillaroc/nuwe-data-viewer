# coding: utf-8
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QFileInfo, QModelIndex, QPoint
from PyQt5.QtWidgets import QDockWidget, QAction, QMenu

from .UI_project_view_widget import Ui_ProjectViewWidget
from nuwe_data_viewer.lib.core.project_model import ProjectModel, ProjectItemType, ProjectModelDataType


class ProjectViewWidget(QDockWidget):
    """
    Tree-like project view widget
    """
    signal_grib_file_clicked = pyqtSignal(QFileInfo)
    signal_grib_file_show_chart_clicked = pyqtSignal(QFileInfo)

    def __init__(self, parent=None):
        super(QDockWidget, self).__init__(parent)

        self.ui = Ui_ProjectViewWidget()
        self.ui.setupUi(self)
        self.project_model = None

        self.ui.project_view.clicked.connect(self.slot_project_view_clicked)
        self.ui.project_view.customContextMenuRequested.connect(self.slot_project_context_menu_requested)

    def set_project_model(self, project_model: ProjectModel):
        self.project_model = project_model
        self.ui.project_view.setModel(self.project_model)

    def add_file(self, file_type, file_path):
        self.project_model.add_item(ProjectItemType.GribFile, {
            'file_path': file_path
        })

    @pyqtSlot(QModelIndex)
    def slot_project_view_clicked(self, index: QModelIndex):
        item_type = self.project_model.get_item_type(index)

        if item_type == ProjectItemType.GribFile:
            item = self.project_model.itemFromIndex(index)
            file_info = item.data(ProjectModelDataType.FileInfoType.value)
            self.signal_grib_file_clicked.emit(file_info)
        else:
            print("item_type not supported", item_type)

    @pyqtSlot(QPoint)
    def slot_project_context_menu_requested(self, point):
        index = self.ui.project_view.indexAt(point)
        if not index.isValid():
            print("[slot_project_context_menu_requested] index is not valid")
            return

        actions = []

        action_show_file_content = QAction(self)
        action_show_file_content.setObjectName('action_show_file_content')
        action_show_file_content.setText('Show file content')
        actions.append(action_show_file_content)

        action_show_file_viewer = QAction(self)
        action_show_file_viewer.setObjectName('action_show_file_viewer')
        action_show_file_viewer.setText('Show charts')
        actions.append(action_show_file_viewer)

        result_action = QMenu.exec(actions, self.ui.project_view.mapToGlobal(point))
        if result_action == action_show_file_viewer:
            item_type = self.project_model.get_item_type(index)

            if item_type == ProjectItemType.GribFile:
                item = self.project_model.itemFromIndex(index)
                file_info = item.data(ProjectModelDataType.FileInfoType.value)
                self.signal_grib_file_show_chart_clicked.emit(file_info)
