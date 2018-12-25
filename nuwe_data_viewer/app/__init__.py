# coding: utf-8
import sys


def run_app(config_file):
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtCore import Qt
    from .mainwindow import MainWindow

    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.load_config(config_file)

    from nuwe_data_viewer.lib.core.editor_system.editor_manager import EditorManager
    editor_manager = EditorManager(main_window)
    main_window.set_editor_manager(editor_manager)

    main_window.show()

    sys.exit(app.exec_())
