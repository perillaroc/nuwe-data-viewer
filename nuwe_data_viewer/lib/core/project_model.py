# coding: utf-8
from enum import Enum

from PyQt5.QtCore import Qt, QFileInfo
from PyQt5.QtGui import QStandardItemModel, QStandardItem


class ProjectModelDataType(Enum):
    ItemType = Qt.UserRole + 300
    FileInfoType = Qt.UserRole + 302


class ProjectItemType(Enum):
    GribFile = Qt.UserRole + 1000


class ProjectModel(QStandardItemModel):
    def __init__(self, parent=None):
        super(QStandardItemModel, self).__init__(parent)

    def add_item(self, item_type: ProjectItemType, item):
        if item_type == ProjectItemType.GribFile:
            file_info = QFileInfo(item['file_path'])
            model_item = QStandardItem(file_info.fileName())
            model_item.setData(ProjectItemType.GribFile, ProjectModelDataType.ItemType.value)
            model_item.setData(file_info, ProjectModelDataType.FileInfoType.value)
            self.appendRow(model_item)
