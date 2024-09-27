import os
import sys

from PyQt5.QtCore import Qt, QLocale
from PyQt5.QtWidgets import QApplication
from qfluentwidgets import FluentTranslator, setTheme, Theme, setThemeColor

from Modules.CMS.CMSClient import CMSClient
from Modules.UI import LoginWindow, MainWindow

# ensure correct working directory
os.chdir(
    os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__)))

if __name__ == '__main__':
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    cmsClient = CMSClient()
    app = QApplication(sys.argv)
    setTheme(Theme.DARK)
    setThemeColor('#e92828')

    if cmsClient.get_user_info() is None:
        loginWindow = LoginWindow()
        loginWindow.show()
    else:
        mainWindow = MainWindow(cmsClient)
        mainWindow.show()
    sys.exit(app.exec_())
