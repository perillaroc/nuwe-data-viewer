# coding: utf-8
import sys
from nuwe_data_viewer.plugin.grib_tool.param_db.grib2_table_database import Grib2TableDatabase

grib_table_db = Grib2TableDatabase()
grib_table_db.read_definition()


def run_app(config_file):
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtCore import Qt

    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)

    from nuwe_data_viewer.lib.plugin_system.manager import PluginManager
    plugin_manager = PluginManager()
    plugin_manager.load_config(config_file)

    plugin_manager.load_plugins()

    sys.exit(app.exec_())
