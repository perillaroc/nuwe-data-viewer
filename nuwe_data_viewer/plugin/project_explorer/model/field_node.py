# coding: utf-8
from PyQt5.QtCore import Qt
from .node import Node
from .container_node import ContainerNode


class FieldCategoryNode(ContainerNode):
    def __init__(self, display_name, node_id=None):
        ContainerNode.__init__(self, display_name, node_id)


class FieldNode(Node):
    FileInfoRole = Qt.UserRole + 511

    def __init__(self, display_name="", node_id=None):
        Node.__init__(self, display_name, node_id)
        self.file_info = None
        self.message_count = -1
