# coding: utf-8
import datetime

from PyQt5 import QtWidgets
import matplotlib
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as Canvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

from nuwe_data_viewer.lib.core.plotter.grid_data import GridData

from .UI_plot_widget import Ui_PlotWidget


matplotlib.use('Qt5Agg')


class PlotCanvas(Canvas):
    def __init__(self):
        # self.fig = Figure(tight_layout=True)
        self.fig = Figure()
        super(PlotCanvas, self).__init__(self.fig)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.updateGeometry()


class PlotWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(PlotWidget, self).__init__(parent)
        self.ui = Ui_PlotWidget()

        self.ui.setupUi(self)

        self.canvas = PlotCanvas()
        self.navigation_tool_bar = NavigationToolbar(self.canvas, self)

        self.ui.navi_bar_layout.addWidget(self.navigation_tool_bar)
        self.ui.canvas_layout.addWidget(self.canvas)

    def plot(self, grid_data: GridData):
        print('plot begin:', datetime.datetime.utcnow())
        self.canvas.fig.clf()
        self.canvas.ax = self.canvas.fig.add_subplot(
            111,
            projection=ccrs.PlateCarree(central_longitude=180))

        self.canvas.ax.contourf(
            grid_data.lons, grid_data.lats, grid_data.values,
            transform=ccrs.PlateCarree(),
            cmap='rainbow'
        )

        gl = self.canvas.ax.gridlines(
            crs=ccrs.PlateCarree(), draw_labels=True, linewidth=2, color='gray', alpha=0.5, linestyle='--')
        gl.xformatter = LONGITUDE_FORMATTER
        gl.yformatter = LATITUDE_FORMATTER

        self.canvas.ax.coastlines()
        self.canvas.ax.gridlines()

        self.canvas.draw()
        print('plot end:', datetime.datetime.utcnow())
