# coding: utf-8
from nuwe_data_viewer.plugin.project_explorer.model.node import Node


class ContainerNode(Node):
    def __init__(self, display_name="", node_id=None):
        Node.__init__(self, display_name, node_id)
