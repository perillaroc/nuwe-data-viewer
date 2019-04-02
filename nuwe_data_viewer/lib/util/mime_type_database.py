# coding: utf-8

from nuwe_data_viewer.lib.util.mime_type import MimeType


class MimeTypeDatabase(object):
    def __init__(self):
        self.mime_type_map = dict()

    def register_mime_type(self, mime_type: MimeType):
        self.mime_type_map[mime_type.name()] = mime_type
