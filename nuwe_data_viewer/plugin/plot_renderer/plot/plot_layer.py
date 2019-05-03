# coding: utf-8
from nuwe_data_viewer.lib.util.id import Id


class PlotLayer(object):
    def __init__(self, name, core_id=None):
        if core_id is None:
            core_id = Id()
        self.name = name
        self.core_id = core_id
