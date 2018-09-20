# coding: utf-8
from PyQt5.QtCore import pyqtSlot, QModelIndex, QFileInfo, QPoint
from PyQt5.QtWidgets import QWidget, QAction, QMenu, QGridLayout, QVBoxLayout
import numpy as np

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQT
from matplotlib.figure import Figure

from nuwe_data_viewer.lib.core.file_content_model import FileContentModel
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
        self.canvas = FigureCanvasQT(Figure(figsize=(5, 3)))
        layout.addWidget(self.canvas)

        self._static_ax = self.canvas.figure.subplots()
        t = np.linspace(0, 10, 501)
        self._static_ax.plot(t, np.tan(t), ".")

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

        # stdout = self.message_content_model.set_message(self.file_content_model.file_info, message_number)
        # self.ui.message_content_widget.setText(stdout)
