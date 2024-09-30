from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
from qfluentwidgets import BodyLabel, CheckBox, HyperlinkButton, LineEdit, PrimaryPushButton, SplitTitleBar, \
    isDarkTheme, setTheme, setThemeColor, Theme
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon, QColor

from App.common import isWin11

if isWin11():
    from qframelesswindow import AcrylicWindow as Window
else:
    from qframelesswindow import FramelessWindow as Window


class Ui_Login(Window):
    def __init__(self):
        super().__init__()
        setTheme(Theme.DARK)
        setThemeColor('#e92828')
        self.resize(1250, 500)
        self.setMinimumSize(QtCore.QSize(900, 500))
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)

        self.widget = QtWidgets.QWidget(self)
        self.widget.setMinimumSize(QtCore.QSize(400, 0))
        self.widget.setMaximumSize(QtCore.QSize(400, 16777215))
        self.widget.setStyleSheet("QLabel{font: 13px \'Microsoft YaHei\'}")

        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(24, 50, 24, 24)
        self.verticalLayout_2.setSpacing(16)

        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)

        self.logo = QtWidgets.QLabel(self.widget)
        self.logo.setFixedSize(QtCore.QSize(300, 75))
        self.logo.setPixmap(QtGui.QPixmap("./resource/images/scie_logo_2.png"))
        self.logo.setScaledContents(True)
        self.verticalLayout_2.addWidget(self.logo, 0, QtCore.Qt.AlignHCenter)

        self.space = QtWidgets.QLabel(self)
        self.space.setFixedSize(QtCore.QSize(300, 6))
        self.verticalLayout_2.addWidget(self.space, 0, QtCore.Qt.AlignHCenter)

        spacerItem1 = QtWidgets.QSpacerItem(20, 15, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_2.addItem(spacerItem1)

        self.sid_label = BodyLabel(self.widget)
        self.verticalLayout_2.addWidget(self.sid_label)

        self.sid_input = LineEdit(self.widget)
        self.sid_input.setClearButtonEnabled(True)
        self.verticalLayout_2.addWidget(self.sid_input)

        self.pwd_label = BodyLabel(self.widget)
        self.verticalLayout_2.addWidget(self.pwd_label)

        self.pwd_input = LineEdit(self.widget)
        self.pwd_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pwd_input.setClearButtonEnabled(True)
        self.verticalLayout_2.addWidget(self.pwd_input)

        spacerItem2 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_2.addItem(spacerItem2)

        self.remember_me = CheckBox(self.widget)
        self.remember_me.setChecked(True)
        self.verticalLayout_2.addWidget(self.remember_me)

        spacerItem3 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_2.addItem(spacerItem3)

        self.login_btn = PrimaryPushButton(self.widget)
        self.verticalLayout_2.addWidget(self.login_btn)
        spacerItem4 = QtWidgets.QSpacerItem(20, 6, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_2.addItem(spacerItem4)

        self.link_btn = HyperlinkButton(self.widget)
        self.verticalLayout_2.addWidget(self.link_btn)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem5)
        self.horizontalLayout.addWidget(self.widget)

        self.label = QtWidgets.QLabel(self)
        self.label.setPixmap(QtGui.QPixmap("./resource/images/background.jpg"))
        self.label.setScaledContents(True)
        self.horizontalLayout.addWidget(self.label)

        QtCore.QMetaObject.connectSlotsByName(self)

        self.setTitleBar(SplitTitleBar(self))
        self.titleBar.raise_()

        self.label.setScaledContents(False)
        self.setWindowIcon(QIcon("./resource/images/logo.png"))
        self.resize(1000, 650)

        self.retranslateUi()
        self.windowEffect.setMicaEffect(self.winId(), isDarkMode=isDarkTheme())
        if not isWin11():
            color = QColor("#202020") if isDarkTheme() else QColor(240, 244, 249)
            self.setStyleSheet(f"LoginWindow{{background: {color.name()}}}")

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)

    def retranslateUi(self):
        self.setWindowTitle('CMS Login - Assessment Analyzer')
        self.sid_label.setText("User ID")
        self.sid_input.setPlaceholderText("s00000")
        self.pwd_label.setText("Password")
        self.pwd_input.setPlaceholderText("••••••••••••")
        self.remember_me.setText("Remember me")
        self.login_btn.setText("Login")
        self.link_btn.setText("Powered by SCIE CMS")

    def resizeEvent(self, e):
        super().resizeEvent(e)
        pixmap = QPixmap("./resource/images/background.jpg").scaled(
            self.label.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        self.label.setPixmap(pixmap)
