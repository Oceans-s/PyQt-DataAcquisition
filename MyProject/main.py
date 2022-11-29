import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget
from MyCamera import CameraWidget
from MyInternet import InternetWidget
from MyVideo import VideoWidget


class LoginWidget(QWidget):

    def __init__(self, parent=None):
        super(LoginWidget, self).__init__()
        self.ui = uic.loadUi("./UI/LoginUI.ui")


if __name__ == '__main__':
    from PyQt5 import QtCore

    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)  # Self adaptive resolution

    myapp = QApplication(sys.argv)

    myLogin = LoginWidget()
    myInternet = InternetWidget()
    myCamera = CameraWidget()
    myVideo = VideoWidget()

    myLogin.ui.show()

    myLogin.ui.cameraBtn.clicked.connect(myLogin.ui.close)
    myLogin.ui.InternetBtn.clicked.connect(myLogin.ui.close)
    myLogin.ui.videoBtn.clicked.connect(myLogin.ui.close)

    myLogin.ui.cameraBtn.clicked.connect(myCamera.ui.show)
    myLogin.ui.InternetBtn.clicked.connect(myInternet.ui.show)
    myLogin.ui.videoBtn.clicked.connect(myVideo.ui.show)

    myInternet.ui.InternetHomeBtn.clicked.connect(myInternet.ui.close)
    myInternet.ui.InternetHomeBtn.clicked.connect(myLogin.ui.show)

    myCamera.ui.cameraHomeBtn.clicked.connect(myCamera.ui.close)
    myCamera.ui.cameraHomeBtn.clicked.connect(myLogin.ui.show)

    myVideo.ui.videoHomeBtn.clicked.connect(myVideo.ui.close)
    myVideo.ui.videoHomeBtn.clicked.connect(myLogin.ui.show)

    sys.exit(myapp.exec_())
