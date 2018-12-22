# coding: utf-8
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QFileInfo, QModelIndex, QPoint
from PyQt5.QtWidgets import QDockWidget, QMenu

from .UI_project_view_widget import Ui_ProjectViewWidget
from nuwe_data_viewer.lib.project_explorer.model.project_model import (
    ProjectModel, ProjectItemType
)
from .model.data_node import GribFileNode
from .model.field_node import FieldNode


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

        self.ui.project_view.doubleClicked.connect(self.slot_project_view_double_clicked)
        self.ui.project_view.customContextMenuRequested.connect(self.slot_project_context_menu_requested)

    def set_project_model(self, project_model: ProjectModel):
        self.project_model = project_model
        self.ui.project_view.setModel(self.project_model)

    def add_file(self, file_type, file_path):
        file_item = self.project_model.add_item(ProjectItemType.GribFile, {
            'file_path': file_path
        })
        self.ui.project_view.scrollTo(file_item.index())

    @pyqtSlot(QModelIndex)
    def slot_project_view_double_clicked(self, index: QModelIndex):
        item = self.project_model.itemFromIndex(index)
        if isinstance(item, GribFileNode):
            file_info = item.file_info

        else:
            pass

    @pyqtSlot(QPoint)
    def slot_project_context_menu_requested(self, point):
        index = self.ui.project_view.indexAt(point)
        if not index.isValid():
            print("[slot_project_context_menu_requested] index is not valid")
            return
        global_point = self.ui.project_view.mapToGlobal(point)
        item = self.project_model.itemFromIndex(index)
        if isinstance(item, GribFileNode):
            self.show_context_menu_for_grib_file_node(global_point, item)
        elif isinstance(item, FieldNode):
            self.show_context_menu_for_field_node(global_point, item)
        else:
            print("item_type not supported", item.__class__.__name__)

    def show_context_menu_for_grib_file_node(self, global_point, item: GribFileNode):
        file_info = item.file_info

        actions = [
            self.ui.action_read_file,
            self.ui.action_show_file_content,
            self.ui.action_show_file_viewer
        ]

        result_action = QMenu.exec(actions, global_point)

        if result_action == self.ui.action_show_file_viewer:
            self.signal_grib_file_show_chart_clicked.emit(file_info)
        elif result_action == self.ui.action_show_file_content:
            self.signal_grib_file_clicked.emit(file_info)
        elif result_action == self.ui.action_read_file:
            self.read_grib_file(item)

    def show_context_menu_for_field_node(self, global_point, item: FieldNode):
        actions = [
            self.ui.action_view_chart
        ]

        result_action = QMenu.exec(actions, global_point)

        if result_action == self.ui.action_view_chart:
            index_node = item.parent().child(item.index().row(), 0)
            message_count = int(index_node.text())
            file_info = index_node.data(FieldNode.FileInfoRole)
            print('show chart in viewer: message {message_count} in {file_path}'.format(
                message_count=message_count,
                file_path=file_info.absoluteFilePath()
            ))

    def read_grib_file(self, item: GribFileNode, reload=False):
        from nuwe_data_viewer.plugin.grib_data_handler.grib_file_info import GribFileInfo, project_file_list
        from nuwe_data_viewer.plugin.grib_data_handler.grib_info import GribKeyType, GribKey

        if item.grib_info is None or reload:
            grib_file_info = GribFileInfo(self.project_model.config)
            grib_file_info.set_file_path(item.file_info.filePath())
            grib_info = grib_file_info.get_grib_info(project_file_list)
            item.grib_info = grib_info

        extended_key_list = [
            GribKey('No', GribKeyType.Long)
        ]
        extended_key_list.extend(project_file_list)
        self.project_model.setColumnCount(len(extended_key_list))
        self.ui.project_view.setHeaderHidden(False)

        # cur_index = 0
        # for a_key in extended_key_list:
        #     self.project_model.setHeaderData(cur_index, Qt.Horizontal, a_key.name)
        #     cur_index += 1

        cur_index = 1
        for a_message_info in item.grib_info.messages:
            message_row = list()
            index_node = FieldNode(str(cur_index))
            index_node.setData(item.file_info, FieldNode.FileInfoRole)
            message_row.append(index_node)
            for prop in a_message_info.props:
                value_item = FieldNode(str(prop.value))
                message_row.append(value_item)
            item.appendRow(message_row)
            cur_index += 1