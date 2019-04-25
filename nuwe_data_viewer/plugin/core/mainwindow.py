# coding: utf-8
import yaml
from enum import Enum

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PyQt5.QtCore import Qt, QFileInfo

from nuwe_data_viewer.plugin.core.UI_mainwindow import Ui_MainWindow
from nuwe_data_viewer.plugin.core.widgets.file_content_widget import FileContentWidget
from nuwe_data_viewer.plugin.core.widgets.file_visual_widget import FileVisualWidget

from nuwe_data_viewer.plugin.core.editor_system.editor_window import EditorWindow
from nuwe_data_viewer.plugin.core.editor_system.editor_interface import EditorInterface
from nuwe_data_viewer.plugin.core.editor_system.editor_view import EditorView
from nuwe_data_viewer.plugin.core.editor_system.editor_manager import EditorManager


class FileContentItemModel(Enum):
    MESSAGE_COUNT = Qt.UserRole + 201


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.editor_manager = None

        # ui
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # connection
        self.ui.action_open_grib2_file.triggered.connect(self.on_open_grib2_file)
        self.ui.action_exit.triggered.connect(self.close)

        # variable
        self.config = None

    def load_config(self, config):
        self.config = config

    def set_central_widget(self, widget):
        self.setCentralWidget(widget)

    def set_editor_manager(self, editor_manager: EditorManager):
        self.editor_manager = editor_manager

    @pyqtSlot(bool)
    def on_open_grib2_file(self, checked):
        file_path, file_type = QFileDialog.getOpenFileName(self, "Open a grib2 file")
        print("file path", file_path)
        self.project_view_widget.add_file(file_type, file_path)

    @pyqtSlot(QFileInfo)
    def slot_file_clicked(self, file_info: QFileInfo):

        file_content_widget = FileContentWidget(self.config, self)

        editor = EditorInterface(self)
        editor.widget = file_content_widget

        window = EditorWindow(self)
        window.set_title('Content: {file_name}'.format(
            file_name=file_info.fileName()
        ))

        view = EditorView(window.edit_area, self)
        view.set_editor(editor)

        window.edit_area.set_current_view(view)
        self.editor_manager.add_window(window)
        window.show()
        file_content_widget.set_file_info(file_info)

    @pyqtSlot(QFileInfo)
    def slot_file_show_chart_clicked(self, file_info: QFileInfo):
        file_visual_widget = FileVisualWidget(self.config, self)

        editor = EditorInterface(self)
        editor.widget = file_visual_widget

        window = EditorWindow(self)
        window.set_title('Visual: {file_name}'.format(
            file_name=file_info.fileName()
        ))

        view = EditorView(window.edit_area, self)
        view.set_editor(editor)
        window.edit_area.set_current_view(view)

        self.editor_manager.add_window(window)
        window.show()
        file_visual_widget.set_file_info(file_info)

