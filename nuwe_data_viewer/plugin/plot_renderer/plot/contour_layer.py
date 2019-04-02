# coding: utf-8
from .plot_layer import PlotLayer
from nuwe_data_viewer.plugin.plot_renderer.grid_data import GridData


class ContourLayer(PlotLayer):
    def __init__(self, name, core_id):
        PlotLayer.__init__(self, name, core_id)
        self.grid_data = None

    def set_data(self, grid_data: GridData):
        self.grid_data = GridData
