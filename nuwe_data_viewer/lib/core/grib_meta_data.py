# coding: utf-8
import subprocess
import nuwe_pyeccodes

key_list = [
    'edition',
    'centre',
    'date',
    'dataType',
    'gridType',
    'typeOfLevel',
    'level',
    'stepRange',
    'shortName',
    'packingType'
]


class GribMetaData(object):
    def __init__(self, config):
        self.file_path = None
        self.config = config

    def set_file_path(self, file_path):
        self.file_path = file_path

    def get_grib_info(self):
        grib_file = nuwe_pyeccodes.GribFileHandler()
        grib_file.openFile(self.file_path)
        grib_message = grib_file.next()
        grib_info = []
        while grib_message:
            message_info = []
            for a_key in key_list:
                value = grib_message.getString(a_key)
                message_info.append({
                    'key': a_key,
                    'value': value
                })
            grib_info.append(message_info)
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

        stdout = result.stdout.decode('gbk')
        stderr = result.stderr.decode('gbk')
        print(stdout)
        print(stderr)
        return stdout, stderr
