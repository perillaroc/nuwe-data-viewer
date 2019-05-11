# coding: utf-8
from .plot_layer import PlotLayer
from nuwe_data_viewer.plugin.plot_renderer.grid_data import GridData


class ContourLayer(PlotLayer):
    def __init__(self, name, core_id=None, fill=False):
        PlotLayer.__init__(self, name, core_id)
        self.grid_data = None
        self.fill = fill

        self.levels = None
        self.colors = None
        self.color_map = None
        self.line_width = None
        self.line_type = None

    def set_data(self, grid_data: GridData):
        self.grid_data = grid_data
