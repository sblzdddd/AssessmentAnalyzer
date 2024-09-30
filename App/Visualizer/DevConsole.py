from PyQt5.QtCore import QUrl, QMetaObject
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QSizePolicy


# chrome devTools window, just for debug
class DevConsole(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(500, 500)
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.devView = QWebEngineView()
        self.devView.setObjectName("devView")
        self.devView.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setCentralWidget(self.devView)
        QMetaObject.connectSlotsByName(self)

        self.setWindowTitle('Dev Console')
        self.setWindowIcon(QIcon("./resource/images/logo.png"))