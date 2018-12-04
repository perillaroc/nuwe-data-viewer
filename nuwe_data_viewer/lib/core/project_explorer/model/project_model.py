# coding: utf-8
from enum import Enum

from PyQt5.QtCore import Qt, QFileInfo, QModelIndex
from PyQt5.QtGui import QStandardItemModel

from nuwe_data_viewer.lib.core.project_explorer.model.data_node import DataNode


class ProjectModelDataType(Enum):
    ItemType = Qt.UserRole + 300
    FileInfoType = Qt.UserRole + 302


class ProjectItemType(Enum):
    GribFile = Qt.UserRole + 1000


class ProjectModel(QStandardItemModel):
    def __init__(self, config, parent=None):
        super(QStandardItemModel, self).__init__(parent)
        self.config = config

    def add_item(self, item_type: ProjectItemType, item):
        if item_type == ProjectItemType.GribFile:
            file_info = QFileInfo(item['file_path'])
            model_item = DataNode(file_info.fileName())
            model_item.setData(ProjectItemType.GribFile, ProjectModelDataType.ItemType.value)
            model_item.setData(file_info, ProjectModelDataType.FileInfoType.value)
            self.appendRow(model_item)
        else:
            raise TypeError("item type not supported:", item_type)

    def get_item_type(self, model_index: QModelIndex):
        model_item = self.itemFromIndex(model_index)
        model_type = model_item.data(ProjectModelDataType.ItemType.value)
        return model_type
