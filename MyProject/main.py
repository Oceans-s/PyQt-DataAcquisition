"""
@author OUYANG CHENGLE
@date 09/11/2022
@participant OUYANG CHENGLE
@latest modification
13/12/2022
Comments were added and the code formatting was optimized
"""

import os
import sys

from PyQt5 import uic
from PyQt5.QtCore import QDir
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog

from MyCamera import CameraWidget
from MyImage import ImageWidget
from MyInternet import InternetWidget
from MyVideo import VideoWidget


class LoginWidget(QWidget):

    def __init__(self, parent=None):
        super(LoginWidget, self).__init__()
        self.ui = uic.loadUi("./UI/LoginUI.ui")  # Loading UI file

        self.ui.ImageBtn.clicked.connect(self.ImageBtnClicked)

    def ImageBtnClicked(self):
        """Select a picture"""

        curPath = QDir.currentPath()
        title = "Select a Image"
        filt = "Image file(*.png *.jpg);;All Documents(*.*)"
        fileName, flt = QFileDialog.getOpenFileName(self, title, curPath, filt)

        if fileName == "":
            return

        command = "F:\Anaconda3\python.exe C:/Users/Oceans/Desktop/DataAcquisition/MyProject/MyImage.py {}".format(
            fileName)
        os.system(command)


if __name__ == '__main__':
    from PyQt5 import QtCore

    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)  # Self adaptive resolution

    myapp = QApplication(sys.argv)

    myLogin = LoginWidget()
    myInternet = InternetWidget()
    myCamera = CameraWidget()
    myVideo = VideoWidget()

    myLogin.ui.show()

    """Jump to the next screen"""
    myLogin.ui.cameraBtn.clicked.connect(myLogin.ui.close)
    myLogin.ui.InternetBtn.clicked.connect(myLogin.ui.close)
    myLogin.ui.videoBtn.clicked.connect(myLogin.ui.close)

    myLogin.ui.cameraBtn.clicked.connect(myCamera.ui.show)
    myLogin.ui.InternetBtn.clicked.connect(myInternet.ui.show)
    myLogin.ui.videoBtn.clicked.connect(myVideo.ui.show)

    """Return to main screen"""
    myInternet.ui.InternetHomeBtn.clicked.connect(myInternet.ui.close)
    myInternet.ui.InternetHomeBtn.clicked.connect(myLogin.ui.show)

    myCamera.ui.cameraHomeBtn.clicked.connect(myCamera.ui.close)
    myCamera.ui.cameraHomeBtn.clicked.connect(myLogin.ui.show)

    myVideo.ui.videoHomeBtn.clicked.connect(myVideo.ui.close)
    myVideo.ui.videoHomeBtn.clicked.connect(myLogin.ui.show)

    sys.exit(myapp.exec_())
