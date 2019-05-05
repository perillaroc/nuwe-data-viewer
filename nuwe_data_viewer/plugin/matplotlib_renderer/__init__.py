# coding: utf-8
from nuwe_data_viewer.lib.plugin_system.plugin import PluginBase
from nuwe_data_viewer.lib.util.logger import get_logger


plugin_name = "matplotlib_renderer"
logger = get_logger(plugin_name)


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
