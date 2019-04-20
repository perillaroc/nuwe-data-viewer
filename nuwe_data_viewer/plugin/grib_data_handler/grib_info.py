from enum import Enum


class GribKeyType(Enum):
    Long = 1
    Double = 2
    String = 3
    DoubleArray = 4


class GribPropKey(object):
    def __init__(self, name: str, key_type: GribKeyType):
        self.name = name
        self.type = key_type

    def __eq__(self, other):
        return self.name == other.name and self.type == other.type


class GribMessageProp(object):
    def __init__(self):
        self.grib_key = None
        self.value = None


class GribMessageInfo(object):
    def __init__(self):
        self.props = []

    def get_prop(self, key: GribPropKey):
        for prop in self.props:
            if prop.grib_key == key:
                return prop
        return None


class GribInfo(object):
    def __init__(self):
        self.messages = []
