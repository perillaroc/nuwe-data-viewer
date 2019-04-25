# coding: utf-8
from nuwe_data_viewer.lib.plugin_system.plugin import PluginBase

plugin_name = "matplotlib_renderer"


class MatplotlibRendererPlugin(PluginBase):
    def __init__(self):
        PluginBase.__init__(self, plugin_name)

    def initialize_plugin(self):
        pass

    def plugin_initialized(self):
        pass

    def plugin_about_to_shutdown(self):
        pass


plugin = MatplotlibRendererPlugin()
