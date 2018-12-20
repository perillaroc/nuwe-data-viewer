# coding: utf-8
import datetime

from PyQt5 import QtWidgets
from nuwe_data_viewer.lib.plot_renderer.grid_data import GridData
from nuwe_data_viewer.lib.plot_renderer.plot.plot_layer import PlotLayer


class PlotRendererWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.layers = list()

    def add_plot_layer(self, layer: PlotLayer):
        pass

    def render_plot(self):
        pass

    def render_plot_layer(self, layer: PlotLayer):
        pass
