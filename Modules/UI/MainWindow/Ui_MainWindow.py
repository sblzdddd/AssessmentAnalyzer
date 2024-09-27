from PyQt5.QtCore import QSize, QMetaObject, Qt, QUrl
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QWidget, QVBoxLayout, QSizePolicy, QLabel, QMainWindow
from qfluentwidgets import setThemeColor, setTheme, Theme, SplitTitleBar, isDarkTheme, ComboBox, FluentIcon
from ..components.ButtonCardView import CardList
from ..stylesheet import StyleSheet

from qframelesswindow import FramelessWindow as Window


class DevConsole(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(500, 500)
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.devView = QWebEngineView()
        url = QUrl("file:///resource/template.html")
        self.devView.load(url)
        self.devView.setObjectName("devView")
        self.devView.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setCentralWidget(self.devView)
        QMetaObject.connectSlotsByName(self)

        self.setWindowTitle('Dev Console')
        self.setWindowIcon(QIcon("./resource/images/logo.png"))

class Ui_MainWindow(Window):
    def __init__(self):
        super().__init__()
        self.resize(1000, 650)
        self.setMinimumSize(QSize(900, 500))
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)

        self.sideBar = QWidget(self)
        self.sideBar.setMinimumSize(QSize(320, 0))
        self.sideBar.setMaximumSize(QSize(320, 16777215))
        self.sideBar.setStyleSheet("QLabel{font: 13px \'Microsoft YaHei\'}")

        self.sideBarVL = QVBoxLayout(self.sideBar)
        self.sideBarVL.setContentsMargins(16, 50, 16, 16)
        self.sideBarVL.setSpacing(16)

        # YEAR SELECTION
        self.yearSelect = ComboBox()

        self.sideBarVL.addWidget(self.yearSelect)

        # SUBJECT SELECTION
        self.subjectList = CardList(self)
        self.sideBarVL.addWidget(self.subjectList)

        self.horizontalLayout.addWidget(self.sideBar)

        # RIGHT CONTENT
        self.content = QWidget(self)
        self.content.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.content.setStyleSheet("QLabel{font: 13px \'Microsoft YaHei\'}")

        self.contentVL = QVBoxLayout(self.content)
        self.contentVL.setContentsMargins(16, 40, 16, 16)
        self.contentVL.setSpacing(16)

        self.horizontalLayout.addWidget(self.content)

        # SUBJECT TITLE
        self.title = QLabel(self)
        self.content.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.title.setObjectName("titleLabel")
        self.contentVL.addWidget(self.title)

        # CHART VIEW
        self.chartView = QWebEngineView()
        self.chartView.setObjectName("chartView")
        self.chartView.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.chartView.setContextMenuPolicy(Qt.NoContextMenu)
        self.contentVL.addWidget(self.chartView)

        QMetaObject.connectSlotsByName(self)

        self.setTitleBar(SplitTitleBar(self))
        self.titleBar.raise_()
        self.setWindowIcon(QIcon("./resource/images/logo.png"))

        self.retranslateUi()
        StyleSheet.HOME_INTERFACE.apply(self.title)

        color = QColor("#202020") if isDarkTheme() else QColor(240, 244, 249)
        self.setStyleSheet(f"background-color: {color.name()}")

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

    def retranslateUi(self):
        self.setWindowTitle('Assessment Analyzer')
        self.title.setText("SubjectName")
