# coding: utf-8
from PyQt5 import QtWidgets

import numpy as np
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
from matplotlib.figure import Figure
import cartopy.crs as ccrs

import nuwe_pyeccodes


matplotlib.use('Qt5Agg')


class PlotCanvas(Canvas):
    def __init__(self):
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        # self.ax.hold(False)

        Canvas.__init__(self, self.fig)
        Canvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        Canvas.updateGeometry(self)


class PlotWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.canvas = PlotCanvas()
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)

    def plot(self, grib_message: nuwe_pyeccodes.GribMessageHandler):
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

        values = grib_message.getDoubleArray('values')
        grid_values = values.reshape(ny, nx)

        self.canvas.fig.clf()
        self.canvas.ax = self.canvas.fig.add_subplot(111, projection=ccrs.PlateCarree())
        self.canvas.ax.contourf(
            lons, lats, grid_values,
            transform=ccrs.PlateCarree(),
            cmap='rainbow'
        )
        self.canvas.ax.coastlines()
        self.canvas.ax.gridlines()

        self.canvas.draw()
