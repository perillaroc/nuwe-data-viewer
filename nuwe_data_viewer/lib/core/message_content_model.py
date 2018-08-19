# coding: utf-8

from PyQt5.QtCore import Qt, QFileInfo
from PyQt5.QtGui import QStandardItemModel, QStandardItem

from .grib_meta_data import GribMetaData, key_list


class MessageContentModel(QStandardItemModel):
    def __init__(self, config, parent=None):
        super(QStandardItemModel, self).__init__(parent)
        self.config = config
        self.file_info = None

    def set_message(self, file_info: QFileInfo, message_index: str):
        self.file_info = file_info
        grib_meta_data = GribMetaData(self.config)
        grib_meta_data.set_file_path(self.file_info.filePath())
        stdout, stderr = grib_meta_data.get_grib_dump_output(message_index)
        return stdout
