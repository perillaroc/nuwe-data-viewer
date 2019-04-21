# coding: utf-8
from nuwe_data_viewer.lib.plugin_system.plugin import PluginBase
from nuwe_data_viewer.plugin.core.mainwindow import MainWindow

plugin_name = "core"


class CorePlugin(PluginBase):
    def __init__(self, plugin_manager):
        PluginBase.__init__(self, plugin_manager, plugin_name)
        self.main_window = None

    def initialize_plugin(self):
        self.main_window = MainWindow()
        self.main_window.load_config(self.plugin_manager.config)

        from nuwe_data_viewer.plugin.core.editor_system.editor_manager import EditorManager
        editor_manager = EditorManager(self.main_window)
        self.main_window.set_editor_manager(editor_manager)

    def plugin_initialized(self):
        self.main_window.show()

    def plugin_about_to_shutdown(self):
        pass


plugin_class = CorePlugin
