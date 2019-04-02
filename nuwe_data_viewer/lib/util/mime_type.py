# coding: utf-8


class MimeType(object):
    def __init__(self, name: str = ""):
        self._name = name

    def valid(self) -> bool:
        return self._name != ''

    def name(self) -> str:
        return self._name

    def __eq__(self, other):
        return self._name == other.name

    def __hash__(self):
        return hash(self._name)
