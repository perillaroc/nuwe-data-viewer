# coding: utf-8
import subprocess
import sys
from enum import Enum

import nuwe_pyeccodes

class GribKeyType(Enum):
    Long = 1
    Double = 2
    String = 3
    DoubleArray = 4


class GribKey(object):
    def __init__(self, name: str, key_type: GribKeyType):
        self.name = name
        self.type = key_type


class GribMessageProp(object):
    def __init__(self):
        self.grib_key = None
        self.value = None


class GribMessageInfo(object):
    def __init__(self):
        self.props = []


class GribInfo(object):
    def __init__(self):
        self.messages = []


view_key_list = (
    GribKey('edition', GribKeyType.String),
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
                value = grib_message.getString(a_key.name)
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
