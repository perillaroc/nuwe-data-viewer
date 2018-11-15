# coding: utf-8
import subprocess
import sys

import nuwe_pyeccodes

from nuwe_data_viewer.lib.core.grib_data_handler.grib_info import (
    GribKeyType, GribKey, GribMessageProp, GribMessageInfo, GribInfo)

view_key_list = (
    GribKey('edition', GribKeyType.Long),
    GribKey('date', GribKeyType.String),
    GribKey('dataType', GribKeyType.String),
    GribKey('stepRange', GribKeyType.String),
    GribKey('typeOfLevel', GribKeyType.String),
    GribKey('level', GribKeyType.String),
    GribKey('shortName', GribKeyType.String),
)


plot_key_list = (
    GribKey('shortName', GribKeyType.String),
    GribKey('typeOfLevel', GribKeyType.String),
    GribKey('level', GribKeyType.String),
    GribKey('date', GribKeyType.String),
    GribKey('stepRange', GribKeyType.String),
)


class GribFileInfo(object):
    def __init__(self, config):
        self.file_path = None
        self.config = config

    def set_file_path(self, file_path):
        self.file_path = file_path

    def get_grib_info(self, key_list: list or set = view_key_list) -> GribInfo:
        grib_file = nuwe_pyeccodes.GribFileHandler()
        grib_file.openFile(self.file_path)
        grib_message = grib_file.next()
        grib_info = GribInfo()
        while grib_message:
            message_info = GribMessageInfo()
            for a_key in key_list:
                key_name = a_key.name
                key_type = a_key.type
                if key_type == GribKeyType.Long:
                    value = grib_message.getLong(key_name)
                elif key_type == GribKeyType.Double:
                    value = grib_message.getDouble(key_name)
                else:
                    value = grib_message.getString(key_name)
                prop = GribMessageProp()
                prop.grib_key = a_key
                prop.value = value
                message_info.props.append(prop)
            grib_info.messages.append(message_info)
            grib_message = grib_file.next()
        return grib_info

    def get_grib_ls_output(self):
        grib_ls_bin = self.config['program']['grib_ls']
        result = subprocess.run(
            [grib_ls_bin, self.file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        stdout = result.stdout
        stderr = result.stderr
        print(stdout.decode('gbk'))
        print(stderr.decode('gbk'))

    def get_grib_dump_output(self, message_number):
        grib_dump_bin = self.config['program']['grib_dump']
        result = subprocess.run(
            [grib_dump_bin,
             "-O",
             "-w",
             "count={message_number}".format(message_number=message_number),
             "{file_path}".format(
                 file_path=self.file_path
             )],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        stdout = result.stdout.decode(sys.stdout.encoding)
        stderr = result.stderr.decode(sys.stderr.encoding)
        # print(stdout)
        print(stderr)
        return stdout, stderr
