# coding: utf-8
import datetime
from PyQt5 import QtWidgets

import numpy as np
import matplotlib
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as Canvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
import cartopy.crs as ccrs

import nuwe_pyeccodes

from .UI_plot_widget import Ui_PlotWidget


matplotlib.use('Qt5Agg')


class PlotCanvas(Canvas):
    def __init__(self):
        self.fig = Figure(tight_layout=True)
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

    def plot(self, grib_message: nuwe_pyeccodes.GribMessageHandler):
        print('get lon/lat begin:', datetime.datetime.utcnow())
        left_lon = grib_message.getDouble('longitudeOfFirstGridPointInDegrees')
        right_lon = grib_message.getDouble('longitudeOfLastGridPointInDegrees')
        lon_step = grib_message.getDouble('iDirectionIncrementInDegrees')
        nx = grib_message.getLong('Ni')
        lon_array = np.arange(left_lon, right_lon + lon_step / 2, lon_step)

        top_lat = grib_message.getDouble('latitudeOfFirstGridPointInDegrees')
        bottom_lat = grib_message.getDouble('latitudeOfLastGridPointInDegrees')
        lat_step = grib_message.getDouble('jDirectionIncrementInDegrees')
        ny = grib_message.getLong('Nj')
        lat_array = np.arange(top_lat, bottom_lat - lat_step / 2, -lat_step)

        lons, lats = np.meshgrid(lon_array, lat_array)

        print('get values begin:', datetime.datetime.utcnow())

        values = grib_message.getDoubleArray('values')
        grid_values = values.reshape(ny, nx)

        print('plot begin:', datetime.datetime.utcnow())
        self.canvas.fig.clf()
        self.canvas.ax = self.canvas.fig.add_subplot(
            111,
            projection=ccrs.PlateCarree(central_longitude=180))

        self.canvas.ax.contourf(
            lons, lats, grid_values,
            transform=ccrs.PlateCarree(),
            cmap='rainbow'
        )

        self.canvas.ax.coastlines()
        self.canvas.ax.gridlines()

        self.canvas.draw()
        print('plot end:', datetime.datetime.utcnow())
