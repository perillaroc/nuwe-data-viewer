# coding: utf-8
import datetime

from PyQt5 import QtWidgets
import matplotlib
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as Canvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
import matplotlib.ticker as mticker
import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

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
            projection=ccrs.PlateCarree(central_longitude=150)
        )

        cf = self.canvas.ax.contourf(
            grid_data.lons, grid_data.lats, grid_data.values,
            transform=ccrs.PlateCarree(),
            cmap='rainbow',
            extend='both'
        )

        self.canvas.ax.coastlines()
        gl = self.canvas.ax.gridlines()
        self.canvas.ax.set_xticks([330, 0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 329.99], crs=ccrs.PlateCarree())
        self.canvas.ax.set_yticks([-90, -60, -30, 0, 30, 60, 90], crs=ccrs.PlateCarree())

        lon_formatter = LongitudeFormatter(
            zero_direction_label=True,
            number_format='.0f'
        )
        lat_formatter = LatitudeFormatter()
        self.canvas.ax.xaxis.set_major_formatter(lon_formatter)
        gl.xlocator = mticker.FixedLocator([0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 360])
        self.canvas.ax.yaxis.set_major_formatter(lat_formatter)
        gl.ylocator = mticker.FixedLocator([-90, -60, -30, 0, 30, 60, 90])

        self.canvas.fig.colorbar(cf, orientation='horizontal')

        self.canvas.draw()
        print('plot end:', datetime.datetime.utcnow())
