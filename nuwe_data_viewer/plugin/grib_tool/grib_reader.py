# coding: utf-8
from enum import Enum

from nuwe_data_viewer.lib.util.id import Id
from nuwe_data_viewer.plugin.project_explorer.model.data_node import GribFileNode
from nuwe_data_viewer.plugin.project_explorer.model.field_node import FieldNode, FieldCategoryNode

from nuwe_data_viewer.plugin.grib_data_handler.grib_file_info import GribFileParser
from nuwe_data_viewer.plugin.grib_data_handler.grib_info import GribKeyType, GribPropKey
from nuwe_data_viewer.plugin.project_explorer.model.model_util import find_node_by_path


class FieldClassifyType(Enum):
    Category = 1
    Vertical = 2
    Unit = 3


reader_key_list = (
    GribPropKey('edition', GribKeyType.Long),
    GribPropKey('date', GribKeyType.String),
    GribPropKey('dataType', GribKeyType.String),
    GribPropKey('stepRange', GribKeyType.String),
    GribPropKey('shortName', GribKeyType.String),
    GribPropKey('typeOfFirstFixedSurface', GribKeyType.Long),
    GribPropKey('typeOfLevel', GribKeyType.String),
    GribPropKey('typeOfLevel', GribKeyType.Long),
    GribPropKey('level', GribKeyType.String),
    GribPropKey('level', GribKeyType.Long),
    GribPropKey('discipline', GribKeyType.Long),
    GribPropKey('parameterCategory', GribKeyType.Long),
    GribPropKey('parameterNumber', GribKeyType.Long),
    GribPropKey('tablesVersion', GribKeyType.Long),
    GribPropKey('units', GribKeyType.Long),
)


class GribReader(object):
    def __init__(self, config):
        self.config = config

    def read(self, data_node: GribFileNode):
        grib_file_parser = GribFileParser(self.config)
        grib_file_parser.set_file_path(data_node.file_info.filePath())

        grib_info = grib_file_parser.get_grib_info(reader_key_list)
        data_node.grib_info = grib_info

    def sort_data_node(self, data_node, classify_type):
        self._update_data_node_by_category(data_node)

    def _update_data_node_by_category(self, data_node):
        discipline_key = GribPropKey("discipline", GribKeyType.Long)
        parameter_category_key = GribPropKey("parameterCategory", GribKeyType.Long)
        parameter_number_key = GribPropKey("parameterNumber", GribKeyType.Long)
        level_type_key = GribPropKey("typeOfFirstFixedSurface", GribKeyType.Long)
        level_type_value_key = GribPropKey("typeOfLevel", GribKeyType.String)
        level_key = GribPropKey("level", GribKeyType.Long)

        grib_info = data_node.grib_info
        cur_index = 1
        for message_info in grib_info.messages:
            discipline_prop = message_info.get_prop(discipline_key)
            parameter_category_prop = message_info.get_prop(parameter_category_key)
            parameter_number_prop = message_info.get_prop(parameter_number_key)
            level_type_prop = message_info.get_prop(level_type_key)
            level_type_value_prop = message_info.get_prop(level_type_value_key)
            level_prop = message_info.get_prop(level_key)

            root_node = data_node

            from nuwe_data_viewer.app import grib_table_db

            # category
            category_id = Id("{discipline}.{category}".format(
                discipline=discipline_prop.value,
                category=parameter_category_prop.value))

            category_node = find_node_by_path(root_node, [category_id])
            if category_node is None:
                category_record = grib_table_db.categories.get(category_id, None)
                if category_record is not None:
                    category_node = FieldCategoryNode(category_record.description, category_id)
                else:
                    category_node = FieldCategoryNode(category_id.name, category_id)
                root_node.appendRow(category_node)

            # number
            number_id = Id("{discipline}.{category}.{number}".format(
                discipline=discipline_prop.value,
                category=parameter_category_prop.value,
                number=parameter_number_prop.value
            ))
            number_node = find_node_by_path(root_node, [category_id, number_id])
            if number_node is None:
                number_record = grib_table_db.numbers.get(number_id, None)
                if number_record is not None:
                    number_node = FieldCategoryNode(number_record.description, number_id)
                else:
                    number_node = FieldCategoryNode(number_id.name, number_id)
                category_node.appendRow(number_node)

            # level
            level_type_id = Id(str(level_type_prop.value))
            level_type_node = find_node_by_path(root_node, [category_id, number_id, level_type_id])
            if level_type_node is None:
                level_type_node = FieldCategoryNode(str(level_type_value_prop.value), level_type_id)
                number_node.appendRow(level_type_node)

            # field
            field_node = FieldNode(str(level_prop.value), Id(str(cur_index)))
            field_node.message_count = cur_index
            field_node.file_info = data_node.file_info
            level_type_node.appendRow(field_node)

            cur_index += 1
