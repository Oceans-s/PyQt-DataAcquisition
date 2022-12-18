"""
@author OUYANG CHENGLE
@date 28/11/2022
@participant OUYANG CHENGLE
@latest modification
13/12/2022
Comments were added and the code formatting was optimized
"""

from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import *


class myVideoWidget(QVideoWidget):
    doubleClickedItem = pyqtSignal(str)  # Creating a double click signal

    def __init__(self, parent=None):
        super(QVideoWidget, self).__init__(parent)

    def mouseDoubleClickEvent(self, QMouseEvent):  # Double click event
        self.doubleClickedItem.emit("double clicked")
