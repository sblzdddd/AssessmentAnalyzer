from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication
from qfluentwidgets import InfoBar, InfoBarPosition

from .Ui_LoginWindow import Ui_Login
from Modules.CMS.CMSClient import CMSClient
from Modules.UI.MainWindow import MainWindow

client = CMSClient()

class LoginWindow(Ui_Login):
    def __init__(self):
        super().__init__()
        s = self
        self.sid_input.returnPressed.connect(self.pwd_input.setFocus)
        self.pwd_input.returnPressed.connect(self.login)
        self.login_btn.clicked.connect(self.login)

    def login(self):
        self.login_btn.setText('Logging In...')
        self.login_btn.setEnabled(False)
        sid = self.sid_input.text()
        password = self.pwd_input.text()
        remember = self.remember_me.checkState() == 2
        if not self.validate_sid(sid):
            self.login_btn.setText('Login')
            self.login_btn.setEnabled(True)
            return

        # Update last frame of GUI
        QApplication.processEvents()
        # Do Login
        login_success, message = client.login(sid, password, remember)

        if login_success:
            InfoBar.success(
                title='Login Success!', content="",
                position=InfoBarPosition.TOP, parent=self
            )
            self.timer = QTimer()
            self.timer.setSingleShot(True)  # This timer will only fire once
            self.timer.timeout.connect(self.open_main_window)
            self.timer.start(1000)  # 3000 milliseconds = 3 seconds
        else:
            InfoBar.success(
                title='Login Failed!', content=message,
                position=InfoBarPosition.TOP, parent=self
            )
            self.login_btn.setText('Login')
            self.login_btn.setEnabled(True)

    def validate_sid(self, sid):
        invalid = None
        if len(sid) != 6:
            invalid = "length of sid is not 6!"
        elif not sid[0].isalpha():
            invalid = "input sid not started with alphabet character!"
        else:
            for char in sid[1:]:
                if not char.isdigit():
                    invalid = "input sid contains non-digit character after first letter!"
        if not invalid:
            return True
        InfoBar.error(
            title='Login Format Error',
            content=invalid, orient=Qt.Horizontal,
            position=InfoBarPosition.TOP, parent=self
        )
        return False

    def open_main_window(self):
        # Hide the login window
        self.hide()
        # Create and show the main window
        self.main_window = MainWindow()
        self.main_window.show()
