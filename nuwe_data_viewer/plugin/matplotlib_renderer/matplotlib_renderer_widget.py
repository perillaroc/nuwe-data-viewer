# coding: utf-8
import datetime

import matplotlib
from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.backends.backend_qt5agg import (
    FigureCanvas as Canvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
import matplotlib.ticker as mticker

import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

from nuwe_data_viewer.plugin.plot_renderer.renderer_widget import PlotRendererWidget, PlotLayer
from nuwe_data_viewer.plugin.plot_renderer.plot.contour_layer import ContourLayer

from nuwe_data_viewer.plugin.matplotlib_renderer import logger


matplotlib.use('Qt5Agg')


class PlotCanvas(Canvas):
    def __init__(self):
        # self.fig = Figure(tight_layout=True)
        self.fig = Figure()
        super(PlotCanvas, self).__init__(self.fig)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.updateGeometry()


class MatplotlibRendererWidget(PlotRendererWidget):
    def __init__(self, parent=None):
        super(MatplotlibRendererWidget, self).__init__(parent)
        from .UI_matplotlib_renderer_widget import Ui_MatplotlibRendererWidgetPlotWidget
        self.ui = Ui_MatplotlibRendererWidgetPlotWidget()
        self.ui.setupUi(self)

        # self.navigation_tool_bar = NavigationToolbar(self.canvas, self)
        # self.ui.navi_bar_layout.addWidget(self.navigation_tool_bar)

        self.canvas = PlotCanvas()
        self.ui.canvas_layout.addWidget(self.canvas)

    def clear_scene(self):
        self.canvas.fig.clf()

    def set_plot_scene(self, plot_scene):
        self.plot_scene = plot_scene
        self.render_plot()

    def render_plot(self):
        logger.info('plot begin: {time}'.format(time=datetime.datetime.utcnow()))
        self.canvas.fig.clf()

        self.canvas.ax = self.canvas.fig.add_subplot(
            111,
            projection=ccrs.PlateCarree(central_longitude=150)
        )

        for a_layer in self.plot_scene.layers:
            self.render_plot_layer(a_layer)

        self.canvas.ax.coastlines()
        self._render_grid()

        self.canvas.draw()
        logger.info('plot end: {time}'.format(time=datetime.datetime.utcnow()))

    def render_plot_layer(self, layer: PlotLayer):
        if isinstance(layer, ContourLayer):
            self._render_contour_layer(layer)
        else:
            logger.warn('layer is not supported: {layer}'.format(layer=layer))

    def _render_contour_layer(self, layer: ContourLayer):
        if layer.fill:
            cf = self.canvas.ax.contourf(
                layer.grid_data.lons, layer.grid_data.lats, layer.grid_data.values,
                transform=ccrs.PlateCarree(),
                cmap='rainbow',
                extend='both',
                levels=20
            )
        else:
            cf = self.canvas.ax.contour(
                layer.grid_data.lons, layer.grid_data.lats, layer.grid_data.values,
                transform=ccrs.PlateCarree(),
                cmap='RdBu',
                extend='both',
                levels=20
            )

        self.canvas.fig.colorbar(cf, fraction=0.035, pad=0.04)
        return cf

    def _render_grid(self):
        projection = ccrs.PlateCarree()
        gl = self.canvas.ax.gridlines()
        self.canvas.ax.set_xticks(
            [330, 0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 329.99],
            crs=projection)
        self.canvas.ax.set_yticks(
            [-90, -60, -30, 0, 30, 60, 90],
            crs=projection)

        lon_formatter = LongitudeFormatter(
            zero_direction_label=True,
            number_format='.0f'
        )
        lat_formatter = LatitudeFormatter()
        self.canvas.ax.xaxis.set_major_formatter(lon_formatter)
        gl.xlocator = mticker.FixedLocator([0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 359.99])
        self.canvas.ax.yaxis.set_major_formatter(lat_formatter)
        gl.ylocator = mticker.FixedLocator([-90, -60, -30, 0, 30, 60, 90])
