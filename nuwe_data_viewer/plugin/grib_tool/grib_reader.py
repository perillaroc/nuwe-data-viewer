# coding: utf-8
from enum import Enum

from nuwe_data_viewer.plugin.project_explorer.model.data_node import GribFileNode
from nuwe_data_viewer.plugin.project_explorer.model.field_node import FieldNode

from nuwe_data_viewer.plugin.grib_data_handler.grib_file_info import GribFileParser, project_file_list
from nuwe_data_viewer.plugin.grib_data_handler.grib_info import GribKeyType, GribKey


class FieldClassifyType(Enum):
    Category = 1
    Vertical = 2
    Unit = 3


class GribReader(object):
    def __init__(self, config):
        self.config = config

    def read(self, data_node: GribFileNode):
        grib_file_parser = GribFileParser(self.config)
        grib_file_parser.set_file_path(data_node.file_info.filePath())

        grib_info = grib_file_parser.get_grib_info(project_file_list)
        data_node.grib_info = grib_info

    def sort_data_node(self, data_node, classify_type):
        extended_key_list = [
            GribKey('No', GribKeyType.Long)
        ]
        extended_key_list.extend(project_file_list)
        data_node.model().setColumnCount(len(extended_key_list))

        cur_index = 1
        for a_message_info in data_node.grib_info.messages:
            message_row = list()
            index_node = FieldNode(str(cur_index))
            index_node.setData(data_node.file_info, FieldNode.FileInfoRole)
            message_row.append(index_node)
            for prop in a_message_info.props:
                value_item = FieldNode(str(prop.value))
                message_row.append(value_item)
            data_node.appendRow(message_row)
            cur_index += 1
