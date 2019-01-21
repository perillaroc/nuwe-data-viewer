from enum import Enum


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
