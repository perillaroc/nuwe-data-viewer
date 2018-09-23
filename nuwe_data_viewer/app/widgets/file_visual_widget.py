# coding: utf-8
from PyQt5.QtCore import pyqtSlot, QModelIndex, QFileInfo
from PyQt5.QtWidgets import QWidget, QVBoxLayout
import nuwe_pyeccodes

from nuwe_data_viewer.lib.core.file_content_model import FileContentModel
from nuwe_data_viewer.app.components.plot_widget import PlotWidget
from .UI_file_visual_widget import Ui_FileVisualWidget


class FileVisualWidget(QWidget):
    def __init__(self, config, parent=None):
        super(QWidget, self).__init__(parent)
        self.config = config

        self.file_content_model = FileContentModel(self.config, self)

        self.ui = Ui_FileVisualWidget()
        self.ui.setupUi(self)
        self.ui.splitter.setStretchFactor(0, 3)
        self.ui.splitter.setStretchFactor(1, 1)

        layout = QVBoxLayout(self.ui.chart_frame)
        self.plot_widget = PlotWidget(self)
        layout.addWidget(self.plot_widget)

        self.ui.file_content_widget.setModel(self.file_content_model)
        self.ui.file_content_widget.clicked.connect(self.slot_file_content_view_clicked)

    def set_file_content_model(self, file_content_model: FileContentModel):
        self.file_content_model = file_content_model
        self.ui.file_content_widget.setModel(self.file_content_model)

    def set_file_info(self, file_info: QFileInfo):
        self.file_content_model.set_file_info(file_info)

    @pyqtSlot(QModelIndex)
    def slot_file_content_view_clicked(self, model_index: QModelIndex):
        number_item = self.file_content_model.item(model_index.row(), 0)
        message_number = int(number_item.text())

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
        self.plot_widget.plot(grib_message)
