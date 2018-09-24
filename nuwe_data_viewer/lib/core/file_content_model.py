# coding: utf-8

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem

from .grib_meta_data import GribMetaData, view_key_list


class FileContentModel(QStandardItemModel):
    def __init__(self, config, parent=None, key_list=view_key_list):
        super(QStandardItemModel, self).__init__(parent)
        self.config = config
        self.key_list = key_list
        self.file_info = None

    def set_file_info(self, file_info):
        self.file_info = file_info
        print(file_info.fileName())
        self._update_model()

    def _update_model(self):
        grib_meta_data = GribMetaData(self.config)
        grib_meta_data.set_file_path(self.file_info.filePath())
        grib_info = grib_meta_data.get_grib_info(self.key_list)

        self.clear()

        cur_index = 0
        extended_key_list = ['No']
        extended_key_list.extend(self.key_list)
        self.setColumnCount(len(extended_key_list))
        for a_key in extended_key_list:
            self.setHeaderData(cur_index, Qt.Horizontal, a_key)
            cur_index += 1

        cur_index = 1
        for a_message_info in grib_info:
            message_row = [QStandardItem(str(cur_index))]
            for prop in a_message_info:
                value_item = QStandardItem(prop['value'])
                message_row.append(value_item)
            self.appendRow(message_row)
            cur_index += 1
