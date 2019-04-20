from nuwe_data_viewer.plugin.project_explorer.model.node import Node


class PlotNode(Node):
    def __init__(self, display_name="", node_id=None):
        Node.__init__(self, display_name, node_id)
