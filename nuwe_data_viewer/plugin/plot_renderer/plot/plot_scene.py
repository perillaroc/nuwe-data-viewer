# coding: utf-8
from .plot_layer import PlotLayer
from .map_layer import MapLayer


class PlotScene(object):
    def __init__(self):
        self.layers = []
        self._init_map_layer()

    def _init_map_layer(self):
        map_layer = MapLayer('map')
        self.append_layer(map_layer)

    def append_layer(self, layer: PlotLayer):
        self.layers.append(layer)
