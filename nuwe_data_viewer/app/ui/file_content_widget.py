# coding: utf-8

from PyQt5.QtCore import pyqtSlot, pyqtSignal, QModelIndex, QFileInfo
from PyQt5.QtWidgets import QWidget


from .UI_file_content_widget import Ui_FileContentWidget

from nuwe_data_viewer.lib.core.file_content_model import FileContentModel
from nuwe_data_viewer.lib.core.message_content_model import MessageContentModel


class FileContentWidget(QWidget):
    def __init__(self, config, parent=None):
        super(QWidget, self).__init__(parent)
        self.config = config

        self.file_content_model = FileContentModel(self.config, self)
        self.message_content_model = MessageContentModel(self.config, self)

        self.ui = Ui_FileContentWidget()
        self.ui.setupUi(self)
        self.ui.splitter.setStretchFactor(0, 1)
        self.ui.splitter.setStretchFactor(1, 3)

        self.ui.file_content_widget.setModel(self.file_content_model)

        self.ui.file_content_widget.clicked.connect(self.slot_file_content_view_clicked)

    def set_file_content_model(self, file_content_model: FileContentModel):
        self.file_content_model = file_content_model
        self.ui.file_content_widget.setModel(self.file_content_model)

    def set_message_content_model(self, message_content_model: MessageContentModel):
        self.message_content_model = message_content_model

    def set_file_info(self, file_info: QFileInfo):
        self.file_content_model.set_file_info(file_info)

    @pyqtSlot(QModelIndex)
    def slot_file_content_view_clicked(self, model_index):
        number_item = self.file_content_model.item(model_index.row(), 0)
        message_number = number_item.text()

        stdout = self.message_content_model.set_message(self.file_content_model.file_info, message_number)
        self.ui.message_content_widget.setText(stdout)
