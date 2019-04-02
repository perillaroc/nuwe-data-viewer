# coding: utf-8

from PyQt5.QtCore import QFileInfo
from PyQt5.QtGui import QStandardItemModel

from nuwe_data_viewer.plugin.grib_data_handler.grib_file_info import GribFileInfo


class MessageContentModel(QStandardItemModel):
    def __init__(self, config, parent=None):
        super(QStandardItemModel, self).__init__(parent)
        self.config = config
        self.file_info = None

    def set_message(self, file_info: QFileInfo, message_index: int):
        self.file_info = file_info
        grib_file_info = GribFileInfo(self.config)
        grib_file_info.set_file_path(self.file_info.filePath())
        stdout, stderr = grib_file_info.get_grib_dump_output(message_index)
        return stdout
