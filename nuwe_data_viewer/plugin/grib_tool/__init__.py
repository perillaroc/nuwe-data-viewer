# coding: utf-8
from nuwe_data_viewer.lib.plugin_system.plugin import PluginBase
from nuwe_data_viewer.plugin.grib_tool.param_db.grib2_table_database import Grib2TableDatabase

plugin_name = "grib_tool"


class GribToolPlugin(PluginBase):
    def __init__(self):
        PluginBase.__init__(self, plugin_name)
        self.grib_table_database = None

    def initialize_plugin(self):
        self.grib_table_database = Grib2TableDatabase()
        self.grib_table_database.read_definition()

    def plugin_initialized(self):
        pass

    def plugin_about_to_shutdown(self):
        pass


plugin = GribToolPlugin()
