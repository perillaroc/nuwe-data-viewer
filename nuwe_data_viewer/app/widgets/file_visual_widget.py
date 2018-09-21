# coding: utf-8
from PyQt5.QtCore import pyqtSlot, QModelIndex, QFileInfo
from PyQt5.QtWidgets import QWidget, QVBoxLayout
import numpy as np
import cartopy.crs as ccrs

from nuwe_data_viewer.lib.core.file_content_model import FileContentModel
from nuwe_data_viewer.app.components.plot_widget import ChartWidget
from .UI_file_visual_widget import Ui_FileVisualWidget


class FileVisualWidget(QWidget):
    def __init__(self, config, parent=None):
        super(QWidget, self).__init__(parent)
        self.config = config

        self.file_content_model = FileContentModel(self.config, self)

        self.ui = Ui_FileVisualWidget()
        self.ui.setupUi(self)
        self.ui.splitter.setStretchFactor(0, 1)
        self.ui.splitter.setStretchFactor(1, 3)

        layout = QVBoxLayout(self.ui.chart_frame)
        self.chart_widget = ChartWidget(self)
        layout.addWidget(self.chart_widget)

        self.ui.file_content_widget.setModel(self.file_content_model)
        self.ui.file_content_widget.clicked.connect(self.slot_file_content_view_clicked)

    def set_file_content_model(self, file_content_model: FileContentModel):
        self.file_content_model = file_content_model
        self.ui.file_content_widget.setModel(self.file_content_model)

    def set_file_info(self, file_info: QFileInfo):
        self.file_content_model.set_file_info(file_info)

    @pyqtSlot(QModelIndex)
    def slot_file_content_view_clicked(self, model_index):
        number_item = self.file_content_model.item(model_index.row(), 0)
        message_number = number_item.text()

        x = range(0, 10)
        y = range(0, 20, 2)
        self.chart_widget.canvas.fig.clf()
        self.chart_widget.canvas.ax = self.chart_widget.canvas.fig.add_subplot(111, projection=ccrs.PlateCarree())
        self.chart_widget.canvas.ax.coastlines()
        self.chart_widget.canvas.draw()
