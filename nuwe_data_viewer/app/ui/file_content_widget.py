# coding: utf-8

from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QWidget


from .UI_file_content_widget import Ui_FileContentWidget

from nuwe_data_viewer.lib.core.file_content_model import FileContentModel
from nuwe_data_viewer.lib.core.message_content_model import MessageContentModel


class FileContentWidget(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)

        self.ui = Ui_FileContentWidget()
        self.ui.splitter.setStretchFactor(0, 1)
        self.ui.splitter.setStretchFactor(1, 3)

        self.file_content_model = None
        self.message_content_model = None

    def set_file_content_model(self, file_content_model: FileContentModel):
        self.file_content_model = file_content_model

    def set_message_content_model(self, message_content_model: MessageContentModel):
        self.message_content_model = message_content_model
