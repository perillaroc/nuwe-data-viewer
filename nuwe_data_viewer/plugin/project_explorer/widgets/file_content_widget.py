# coding: utf-8
"""
View Grib2 File contents in a table view.
"""

from PyQt5.QtCore import pyqtSlot, QFileInfo
from PyQt5.QtWidgets import QWidget, QVBoxLayout

from nuwe_data_viewer.plugin.project_explorer.widgets.UI_file_content_widget import Ui_FileContentWidget
from nuwe_data_viewer.plugin.project_explorer.components.grib.content_widget import ContentWidget
from nuwe_data_viewer.plugin.project_explorer.widgets.file_content_model import FileContentModel
from nuwe_data_viewer.plugin.project_explorer.widgets.message_content_model import MessageContentModel


class FileContentWidget(QWidget):
    def __init__(self, config, parent=None):
        super(QWidget, self).__init__(parent)
        self.config = config

        self.file_content_model = FileContentModel(self.config, self)
        self.message_content_model = MessageContentModel(self.config, self)

        self.ui = Ui_FileContentWidget()
        self.ui.setupUi(self)
        self.ui.splitter.setStretchFactor(0, 1)
        self.ui.splitter.setStretchFactor(1, 2)

        content_layout = QVBoxLayout(self.ui.content_frame)
        self.content_widget = ContentWidget(self.config, self)
        content_layout.addWidget(self.content_widget)

        self.content_widget.set_file_content_model(self.file_content_model)
        self.content_widget.signal_message_clicked.connect(self.slot_file_content_view_clicked)

    def set_file_content_model(self, file_content_model: FileContentModel):
        self.file_content_model = file_content_model
        self.content_widget.set_file_content_model(self.file_content_model)

    def set_message_content_model(self, message_content_model: MessageContentModel):
        self.message_content_model = message_content_model

    def set_file_info(self, file_info: QFileInfo):
        self.file_content_model.set_file_info(file_info)

    @pyqtSlot(QFileInfo, int)
    def slot_file_content_view_clicked(self, file_info: QFileInfo, message_number: int):
        stdout = self.message_content_model.set_message(file_info, message_number)
        self.ui.message_content_widget.setText(stdout)
