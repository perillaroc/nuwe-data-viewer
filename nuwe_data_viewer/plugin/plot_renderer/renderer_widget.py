# coding: utf-8
from PyQt5 import QtWidgets

from nuwe_data_viewer.plugin.plot_renderer.plot.plot_scene import PlotScene
from nuwe_data_viewer.plugin.plot_renderer.plot.plot_layer import PlotLayer


class PlotRendererWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.plot_scene = None

    def set_plot_scene(self, plot_scene: PlotScene):
        pass

    def clear_plot_scene(self):
        pass

    def render_plot(self):
        pass

    def render_plot_layer(self, layer: PlotLayer):
        pass
