# coding: utf-8
import nuwe_pyeccodes

from nuwe_data_viewer.lib.plugin_system.plugin import PluginBase
from nuwe_data_viewer.plugin.core.editor_system.editor_window import EditorWindow
from nuwe_data_viewer.plugin.core.editor_system.editor_interface import EditorInterface
from nuwe_data_viewer.plugin.core.editor_system.editor_view import EditorView
from nuwe_data_viewer.plugin.grib_tool.grib_plotter import GribPlotter


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
            self.current_plot_viewer = plot_viewer_widget
            print("set current plot viewer:", self.current_plot_viewer)
        window.window_activated.connect(change_current_plot_viewer)

        def close_plot_viewer():
            if self.current_plot_viewer == plot_viewer_widget:
                self.current_plot_viewer = None
        window.window_closed.connect(close_plot_viewer)

        window.show()

    def add_fill_layer(self, data_node):
        if self.current_plot_viewer is None:
            self.add_new_plot_viewer()

        grid_data = self._get_grid_data_form_node(data_node)
        if grid_data is None:
            print("ERROR when loading data from node: ", data_node)
            return

        from nuwe_data_viewer.plugin.plot_renderer.plot.contour_layer import ContourLayer
        layer = ContourLayer('contour layer', 'contour.1')
        layer.grid_data = grid_data
        self.current_plot_viewer.plot_scene.append_layer(layer)

        self.current_plot_viewer.update_renderer()

    @classmethod
    def _get_grid_data_form_node(cls, data_node):
        file_info = data_node.file_info
        message_number = data_node.message_count

        grib_file = nuwe_pyeccodes.GribFileHandler()
        grib_file.openFile(file_info.absoluteFilePath())
        grib_message = None
        for i in range(0, message_number):
            grib_message = grib_file.next()

        if grib_message is None:
            print("ERROR when loading message: ", message_number)
            return None
        grid_data = GribPlotter.generate_plot_data(grib_message)
        return grid_data


plugin = PlotViewerPlugin()
