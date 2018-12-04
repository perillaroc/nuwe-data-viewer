from nuwe_data_viewer.lib.core.project_explorer.model.node import Node


class DataNode(Node):
    def __init__(self, text=""):
        Node.__init__(self, text)