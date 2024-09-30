from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication
from qfluentwidgets import InfoBar, InfoBarPosition

from .Ui_LoginWindow import Ui_Login
from ..MainWindow import MainWindow
from App.CMS import CMSClient

client = CMSClient()


class LoginWindow(Ui_Login):
    def __init__(self):
        super().__init__()
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

        # successfully logged in
        if login_success:
            InfoBar.success(
                title='Login Success!', content="",
                position=InfoBarPosition.TOP, parent=self
            )
            self.timer = QTimer()
            self.timer.setSingleShot(True)  # This timer will only fire once
            self.timer.timeout.connect(self.open_main_window)
            self.timer.start(1000)
        else:
            # pop up login failure notification
            InfoBar.error(
                title='Login Failed!', content=message,
                position=InfoBarPosition.TOP, parent=self
            )
            self.login_btn.setText('Login')
            self.login_btn.setEnabled(True)

    def validate_sid(self, sid):
        """
        check whether sid from user input is valid
        :param sid: user id from input
        :return: boolean
        """
        invalidMsg = None
        # length of sid = 6
        if len(sid) != 6:
            invalidMsg = "length of sid is not 6!"
        # sid should start with an alpha char
        elif not sid[0].isalpha():
            invalidMsg = "input sid not started with alphabet character!"
        else:
            # sid should end with digits
            for char in sid[1:]:
                if not char.isdigit():
                    invalidMsg = "input sid contains non-digit character after first letter!"
        # all check passed
        if not invalidMsg:
            return True
        # throw an error to GUI
        InfoBar.error(
            title='Login Format Error',
            content=invalidMsg, orient=Qt.Horizontal,
            position=InfoBarPosition.TOP, parent=self
        )
        return False

    # open main window and close this login window
    def open_main_window(self):
        # Create and show the main window
        self.main_window = MainWindow(client)
        self.main_window.show()
        # Hide the login window
        self.hide()
