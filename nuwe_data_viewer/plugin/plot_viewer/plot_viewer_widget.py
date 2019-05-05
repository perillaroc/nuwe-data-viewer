# coding: utf-8
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSizePolicy

from nuwe_data_viewer.plugin.plot_renderer.plot.plot_scene import PlotScene
from .UI_plot_viewer_widget import Ui_PlotViewerWidget


class PlotViewerWidget(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.ui = Ui_PlotViewerWidget()
        self.ui.setupUi(self)
        self.renderer_widget = None
        self.plot_scene = None

        self.content_layout = QVBoxLayout(self.ui.renderer_frame)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(0)

        self._init_plot_renderer()
        self._init_plot_scene()
        self.update_renderer()

    def _init_plot_scene(self):
        self.plot_scene = PlotScene()
        self.renderer_widget.set_plot_scene(self.plot_scene)

    def _init_plot_renderer(self):
        from nuwe_data_viewer.plugin.matplotlib_renderer.matplotlib_renderer_widget import MatplotlibRendererWidget
        self.renderer_widget = MatplotlibRendererWidget(self)
        self.content_layout.addWidget(self.renderer_widget)
        self.renderer_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def update_renderer(self):
        self.renderer_widget.render_plot()
