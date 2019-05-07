# coding: utf-8
from PyQt5.QtCore import Qt

from nuwe_data_viewer.lib.plugin_system.plugin import PluginBase
from nuwe_data_viewer.lib.util.logger import get_logger


plugin_name = "project_explorer"
logger = get_logger(plugin_name)


class ProjectExplorerPlugin(PluginBase):
    def __init__(self):
        PluginBase.__init__(self, plugin_name)
        self.project_view_widget = None
        self.project_model = None
        self.core_plugin = None

    def initialize_plugin(self):
        from nuwe_data_viewer.plugin.project_explorer.model.project_model import ProjectModel
        from nuwe_data_viewer.plugin.project_explorer.project_view_widget import ProjectViewWidget
        from nuwe_data_viewer.plugin.core import plugin as core_plugin
        self.core_plugin = core_plugin

        self.project_view_widget = ProjectViewWidget()
        self.project_model = ProjectModel(config=self.plugin_manager.config, parent=self.project_view_widget)
        self.project_view_widget.set_project_model(self.project_model)

        main_window = self.core_plugin.main_window
        main_window.addDockWidget(Qt.LeftDockWidgetArea, self.project_view_widget)

        main_window.ui.action_open_grib2_file.triggered.connect(
            self.project_view_widget.slot_open_grib2_file)

    def plugin_initialized(self):
        pass

    def plugin_about_to_shutdown(self):
        pass


plugin = ProjectExplorerPlugin()
