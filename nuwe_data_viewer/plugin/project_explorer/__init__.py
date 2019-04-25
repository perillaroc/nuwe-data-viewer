# coding: utf-8
from PyQt5.QtCore import Qt

from nuwe_data_viewer.lib.plugin_system.plugin import PluginBase

from nuwe_data_viewer.plugin.project_explorer.model.project_model import ProjectModel
from nuwe_data_viewer.plugin.project_explorer.project_view_widget import ProjectViewWidget

plugin_name = "project_explorer"


class ProjectExplorerPlugin(PluginBase):
    def __init__(self):
        PluginBase.__init__(self, plugin_name)
        self.project_view_widget = None
        self.project_model = None

    def initialize_plugin(self):
        self.project_view_widget = ProjectViewWidget()
        self.project_model = ProjectModel(config=self.plugin_manager.config, parent=self.project_view_widget)
        self.project_view_widget.set_project_model(self.project_model)

        from nuwe_data_viewer.plugin.core import plugin as core_plugin
        main_window = core_plugin.main_window
        main_window.addDockWidget(Qt.LeftDockWidgetArea, self.project_view_widget)
        self.project_view_widget.signal_grib_file_clicked.connect(main_window.slot_file_clicked)
        self.project_view_widget.signal_grib_file_show_chart_clicked.connect(main_window.slot_file_show_chart_clicked)

    def plugin_initialized(self):
        pass

    def plugin_about_to_shutdown(self):
        pass


plugin = ProjectExplorerPlugin()
