# coding: utf-8
from PyQt5.QtCore import pyqtSlot, QFileInfo
from PyQt5.QtWidgets import QWidget, QVBoxLayout
import nuwe_pyeccodes

from nuwe_data_viewer.plugin.data_viewer.components.grib.content_widget import ContentWidget

from nuwe_data_viewer.plugin.data_viewer.file_content_model import FileContentModel
from nuwe_data_viewer.plugin.plot_renderer.plot.contour_layer import ContourLayer
from nuwe_data_viewer.plugin.grib_tool.grib_plotter import GribPlotter

from nuwe_data_viewer.plugin.grib_data_handler.grib_file_info import plot_key_list
from nuwe_data_viewer.plugin.matplotlib_renderer.matplotlib_renderer_widget import MatplotlibRendererWidget

from .UI_file_visual_widget import Ui_FileVisualWidget


class FileVisualWidget(QWidget):
    def __init__(self, config, parent=None):
        super(QWidget, self).__init__(parent)
        self.config = config

        self.file_content_model = FileContentModel(config=self.config, parent=self, key_list=plot_key_list)

        self.ui = Ui_FileVisualWidget()
        self.ui.setupUi(self)
        self.ui.splitter.setStretchFactor(0, 2)
        self.ui.splitter.setStretchFactor(1, 1)

        plot_layout = QVBoxLayout(self.ui.chart_frame)
        self.plot_widget = MatplotlibRendererWidget(self)
        plot_layout.addWidget(self.plot_widget)

        content_layout = QVBoxLayout(self.ui.content_frame)
        self.content_widget = ContentWidget(self.config, self)
        content_layout.addWidget(self.content_widget)

        self.content_widget.set_file_content_model(self.file_content_model)
        self.content_widget.signal_message_clicked.connect(self.slot_file_content_view_clicked)

    # def set_file_content_model(self, file_content_model: FileContentModel):
    #     self.file_content_model = file_content_model
    #     self.content_widget.set_file_content_model(self.file_content_model)

    def set_file_info(self, file_info: QFileInfo):
        self.file_content_model.set_file_info(file_info)

    @pyqtSlot(QFileInfo, int)
    def slot_file_content_view_clicked(self, file_info: QFileInfo, message_number: int):
        # get grib message from file
        file_info = self.file_content_model.file_info
        grib_file = nuwe_pyeccodes.GribFileHandler()
        grib_file.openFile(file_info.absoluteFilePath())
        grib_message = None
        for i in range(0, message_number):
            grib_message = grib_file.next()

        if grib_message is None:
            print("ERROR when loading message: ", message_number)
            return

        # plot message
        grid_data = GribPlotter.generate_plot_data(grib_message)
        layer = ContourLayer('contour layer', 'contour.1')
        layer.grid_data = grid_data
        self.plot_widget.clear_layers()
        self.plot_widget.add_plot_layer(layer)
