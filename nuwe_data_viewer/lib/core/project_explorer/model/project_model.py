# coding: utf-8
from enum import Enum

from PyQt5.QtCore import Qt, QFileInfo, QModelIndex
from PyQt5.QtGui import QStandardItemModel

from .data_node import DataNode, GribFileNode
from .container_node import ContainerNode
from .project_node import ProjectNode


class ProjectModelDataType(Enum):
    ItemType = Qt.UserRole + 300


class ProjectItemType(Enum):
    GribFile = Qt.UserRole + 1000


class ProjectModel(QStandardItemModel):
    def __init__(self, config, project_name='new project', parent=None):
        super(QStandardItemModel, self).__init__(parent)
        self.config = config
        self.project_node = ProjectNode(project_name)
        self.appendRow(self.project_node)

        self.data_container_node = ContainerNode('data')
        self.project_node.appendRow(self.data_container_node)
        self.plot_container_node = ContainerNode('plot')
        self.project_node.appendRow(self.plot_container_node)

    def add_item(self, item_type: ProjectItemType, item):
        if item_type == ProjectItemType.GribFile:
            file_info = QFileInfo(item['file_path'])
            model_item = GribFileNode(file_info.fileName())
            model_item.set_file_info(file_info)
            model_item.setData(ProjectItemType.GribFile, ProjectModelDataType.ItemType.value)
            self.data_container_node.appendRow(model_item)
        else:
            raise TypeError("item type not supported:", item_type)

    def get_item_type(self, model_index: QModelIndex):
        model_item = self.itemFromIndex(model_index)
        model_type = model_item.data(ProjectModelDataType.ItemType.value)
        return model_type
