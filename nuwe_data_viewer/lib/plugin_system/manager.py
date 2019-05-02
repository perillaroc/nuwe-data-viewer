# coding: utf-8
import yaml


class PluginManager(object):
    def __init__(self):
        self.plugins = []
        self.config_file = None
        self.config = None

    def load_config(self, config_file):
        self.config_file = config_file
        with open(config_file) as f:
            config = yaml.safe_load(f)
            self.config = config

    def find_plugin(self, name):
        for plugin in self.plugins:
            if plugin.name == name:
                return plugin
        return None

    def load_plugins(self):
        queue = self.load_queue()
        for plugin in queue:
            plugin.set_plugin_manager(self)

        for plugin in queue:
            plugin.initialize_plugin()

        for plugin in reversed(queue):
            plugin.plugin_initialized()

    def load_queue(self):
        # need to be changed
        import nuwe_data_viewer.plugin.core
        import nuwe_data_viewer.plugin.grib_data_handler
        import nuwe_data_viewer.plugin.grib_tool
        import nuwe_data_viewer.plugin.plot_renderer
        import nuwe_data_viewer.plugin.matplotlib_renderer
        import nuwe_data_viewer.plugin.project_explorer
        import nuwe_data_viewer.plugin.data_viewer
        import nuwe_data_viewer.plugin.plot_viewer

        queue = [
            nuwe_data_viewer.plugin.core.plugin,
            nuwe_data_viewer.plugin.grib_data_handler.plugin,
            nuwe_data_viewer.plugin.grib_tool.plugin,
            nuwe_data_viewer.plugin.plot_renderer.plugin,
            nuwe_data_viewer.plugin.matplotlib_renderer.plugin,
            nuwe_data_viewer.plugin.data_viewer.plugin,
            nuwe_data_viewer.plugin.plot_viewer.plugin,
            nuwe_data_viewer.plugin.project_explorer.plugin
        ]
        return queue
