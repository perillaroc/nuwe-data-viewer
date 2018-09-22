# coding: utf-8
from PyQt5 import QtWidgets
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
from matplotlib.figure import Figure
import cartopy.crs as ccrs
from cartopy.examples.waves import sample_data


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

    def plot(self):
        lons, lats, data = sample_data(shape=(20, 40))

        self.canvas.fig.clf()
        self.canvas.ax = self.canvas.fig.add_subplot(111, projection=ccrs.PlateCarree())
        self.canvas.ax.contourf(lons, lats, data, transform=ccrs.PlateCarree())
        self.canvas.ax.coastlines()
        self.canvas.ax.gridlines()

        self.canvas.draw()
