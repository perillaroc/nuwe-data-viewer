# coding: utf-8
import sys
from nuwe_data_viewer.plugin.grib_tool.param_db.grib2_table_database import Grib2TableDatabase

grib_table_db = Grib2TableDatabase()
grib_table_db.read_definition()


def run_app(config_file):
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtCore import Qt
    from .mainwindow import MainWindow

    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.load_config(config_file)

    from nuwe_data_viewer.plugin.core.editor_system.editor_manager import EditorManager
    editor_manager = EditorManager(main_window)
    main_window.set_editor_manager(editor_manager)

    main_window.show()

    sys.exit(app.exec_())
