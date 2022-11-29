from PyQt5.QtCore import *
from PyQt5.QtWidgets import QSlider


class myVideoSlider(QSlider):
    ClickedValue = pyqtSignal(int)

    def __init__(self, father):
        super().__init__(Qt.Horizontal, father)

    def mousePressEvent(self, QMouseEvent):     # Click Event
        super().mousePressEvent(QMouseEvent)
        value = QMouseEvent.localPos().x()
        # self.setValue(int(value)/9)
        value = round(value/self.width()*self.maximum())  # Calculate the percentage based on the position of the mouse click and the length of the slider
        self.ClickedValue.emit(value)