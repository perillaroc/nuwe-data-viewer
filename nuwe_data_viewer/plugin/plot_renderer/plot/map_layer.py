# coding: utf-8
from nuwe_data_viewer.plugin.plot_renderer.plot.plot_layer import PlotLayer


class MapLayer(PlotLayer):
    def __init__(self, name, core_id=None):
        PlotLayer.__init__(self, name, core_id)
