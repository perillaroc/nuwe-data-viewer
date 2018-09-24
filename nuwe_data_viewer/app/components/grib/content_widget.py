# coding: utf-8
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QFileInfo, pyqtSignal, pyqtSlot, QModelIndex

from nuwe_data_viewer.lib.core.file_content_model import FileContentModel
from .UI_content_widget import Ui_ContentWidget


class ContentWidget(QWidget):
    """
    show contents in a GRIB2 file using table view.
    """

    signal_message_clicked = pyqtSignal(QFileInfo, int)

    def __init__(self, config: dict, parent=None):
        super(QWidget, self).__init__(parent)
        self.config = config

        self.file_content_model = None

        self.ui = Ui_ContentWidget()
        self.ui.setupUi(self)
        self.ui.content_view.clicked.connect(self.slot_content_view_clicked)

    def set_file_content_model(self, file_content_model: FileContentModel):
        self.file_content_model = file_content_model
        self.ui.content_view.setModel(self.file_content_model)

    def set_file_info(self, file_info: QFileInfo):
        self.file_content_model.set_file_info(file_info)

    @pyqtSlot(QModelIndex)
    def slot_content_view_clicked(self, model_index: QModelIndex):
        number_item = self.file_content_model.item(model_index.row(), 0)
        message_number = int(number_item.text())
        file_info = self.file_content_model.file_info
        self.signal_message_clicked.emit(file_info, message_number)
