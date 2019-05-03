# coding: utf-8
from PyQt5.QtCore import QObject, pyqtSlot, Qt
from PyQt5.QtWidgets import QTabWidget, QLabel
from .editor_window import EditorWindow


class EditorManager(QObject):
    def __init__(self, main_window, parent: QObject = None):
        QObject.__init__(self, parent)
        self.main_window = main_window
        self.windows = list()
        self.tab_widget = None
        self.empty_label_content = (
            "<html><body style=\"color:#909090; font-size:14px\">"
            "<div align='center'>"
            "<div style=\"font-size:20px\">Open a document</div></body></html>")
        self.empty_label = QLabel()
        self.empty_label.setTextFormat(Qt.RichText)
        self.empty_label.setText(self.empty_label_content)
        self.main_window.set_central_widget(self.empty_label)

    def add_window(self, window: EditorWindow):
        self.windows.append(window)

        if self.tab_widget is None:
            self._create_tab()

        last_window = window
        self.tab_widget.addTab(last_window, last_window.windowTitle())

    def remove_window(self, index):
        window = self.tab_widget.widget(index)
        self.tab_widget.removeTab(index)
        self.windows.remove(window)

        if len(self.windows) == 0:
            self._remove_tab()

        window.window_closed.emit()

    def slot_tab_activated(self, index):
        if index == -1:
            return
        window = self.tab_widget.widget(index)
        window.window_activated.emit()

    @pyqtSlot(int)
    def slot_tab_close(self, index):
        self.remove_window(index)

    def _create_tab(self):
        self.tab_widget = QTabWidget(self.main_window)
        self.tab_widget.setTabsClosable(True)
        self.main_window.set_central_widget(self.tab_widget)
        self.empty_label = None
        self.tab_widget.tabCloseRequested.connect(self.slot_tab_close)
        self.tab_widget.currentChanged.connect(self.slot_tab_activated)

    def _remove_tab(self):
        self.empty_label = QLabel()
        self.empty_label.setTextFormat(Qt.RichText)
        self.empty_label.setText(self.empty_label_content)
        self.main_window.set_central_widget(self.empty_label)
        self.tab_widget = None
