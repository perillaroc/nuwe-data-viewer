# coding: utf-8
import subprocess


class GribMetaData(object):
    def __init__(self, config):
        self.file_path = None
        self.config = config

    def set_file_path(self, file_path):
        self.file_path = file_path

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
