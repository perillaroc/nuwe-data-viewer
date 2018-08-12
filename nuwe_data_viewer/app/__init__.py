# coding: utf-8
import sys


def run_app():
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtCore import Qt
    from .mainwindow import MainWindow

    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec_())
