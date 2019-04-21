# coding: utf-8


class PluginBase(object):
    def __init__(self, plugin_manager, plugin_name):
        self.plugin_manager = plugin_manager
        self.plugin_name = plugin_name

    def initialize_plugin(self):
        pass

    def plugin_initialized(self):
        pass

    def plugin_about_to_shutdown(self):
        pass
