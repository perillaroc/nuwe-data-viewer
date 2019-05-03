# coding: utf-8
from nuwe_data_viewer.lib.plugin_system.plugin import PluginBase
from nuwe_data_viewer.plugin.core.editor_system.editor_window import EditorWindow
from nuwe_data_viewer.plugin.core.editor_system.editor_interface import EditorInterface
from nuwe_data_viewer.plugin.core.editor_system.editor_view import EditorView


plugin_name = "plot_viewer"


class PlotViewerPlugin(PluginBase):
    def __init__(self):
        PluginBase.__init__(self, plugin_name)
        self.current_plot_viewer = None
        self.core_plugin = None
        self.main_window = None

    def initialize_plugin(self):
        from nuwe_data_viewer.plugin.core import plugin as core_plugin
        self.core_plugin = core_plugin

        self.main_window = self.core_plugin.main_window
        self.main_window.ui.action_new_plot.triggered.connect(self.add_new_plot_viewer)

    def plugin_initialized(self):
        pass

    def plugin_about_to_shutdown(self):
        pass

    def add_new_plot_viewer(self):
        from .plot_viewer_widget import PlotViewerWidget
        plot_viewer_widget = PlotViewerWidget()

        editor = EditorInterface()
        editor.widget = plot_viewer_widget

        window = EditorWindow()
        window.set_title('Plot')

        view = EditorView(window.edit_area)
        view.set_editor(editor)
        window.edit_area.set_current_view(view)

        self.main_window.editor_manager.add_window(window)

        self.current_plot_viewer = window.edit_area.view.editor.widget

        def change_current_plot_viewer():
            self.current_plot_viewer = window.edit_area.view.editor.widget
            print("set current plot viewer:", self.current_plot_viewer)

        window.window_activated.connect(change_current_plot_viewer)

        window.show()


plugin = PlotViewerPlugin()
