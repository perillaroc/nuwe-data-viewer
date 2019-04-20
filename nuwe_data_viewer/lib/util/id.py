# coding: utf-8
import uuid


class Id(object):
    def __init__(self, name=None):
        if name is None:
            name = uuid.uuid4()
        self.name = name

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)
