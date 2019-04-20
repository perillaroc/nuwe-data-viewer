# coding: utf-8
import uuid


class Id(object):
    def __init__(self, name=None):
        if name is None:
            name = uuid.uuid4()
        self.name = name
