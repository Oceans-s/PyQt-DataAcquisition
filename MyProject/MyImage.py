import sys
import time

from PyQt5.QtCore import QRectF, QSize, Qt
from PyQt5.QtGui import QPainter, QPixmap, QWheelEvent
from PyQt5.QtWidgets import (QApplication, QGraphicsItem, QGraphicsPixmapItem,
                             QGraphicsScene, QGraphicsView)


def get_filepath():
    sys.argv.pop(0)
    length = len(sys.argv)
    argv = ""
    for i in range(0, length):
        argv += sys.argv[i]
        if i != length - 1:
            argv += " "

    return argv

class ImageWidget(QGraphicsView):
    """ Image viewer """

    file_path = None

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.zoomInTimes = 0
        self.maxZoomInTimes = 22

        # Creating a Scenario
        self.graphicsScene = QGraphicsScene()

        # The picture

        self.file_path = get_filepath()
        self.pixmap = QPixmap(self.file_path)
        self.pixmapItem = QGraphicsPixmapItem(self.pixmap)
        self.displayedImageSize = QSize(0, 0)

        # Initialize the widget
        self.__initWidget()

    def __initWidget(self):
        """ Initialize the widget """
        self.resize(1200, 900)

        # Hide the scroll bar
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Zoom with the mouse as the anchor point
        self.setTransformationAnchor(self.AnchorUnderMouse)

        # Smooth scaling
        self.pixmapItem.setTransformationMode(Qt.SmoothTransformation)
        self.setRenderHints(QPainter.Antialiasing |
                            QPainter.SmoothPixmapTransform)

        # Setting the Scene
        self.graphicsScene.addItem(self.pixmapItem)
        self.setScene(self.graphicsScene)

    def wheelEvent(self, e: QWheelEvent):
        """ Scroll the mouse wheel to zoom in and out of the image """
        if e.angleDelta().y() > 0:
            self.zoomIn()
        else:
            self.zoomOut()

    def resizeEvent(self, e):
        """ Zoom the picture """
        super().resizeEvent(e)

        if self.zoomInTimes > 0:
            return

        # Resize an image
        ratio = self.__getScaleRatio()
        self.displayedImageSize = self.pixmap.size()*ratio
        if ratio < 1:
            self.fitInView(self.pixmapItem, Qt.KeepAspectRatio)
        else:
            self.resetTransform()

    def setImage(self, imagePath: str):
        """ Set the images to display """
        self.resetTransform()

        # Refresh the image
        self.pixmap = QPixmap(imagePath)
        self.pixmapItem.setPixmap(self.pixmap)

        # Resize an image
        self.setSceneRect(QRectF(self.pixmap.rect()))
        ratio = self.__getScaleRatio()
        self.displayedImageSize = self.pixmap.size()*ratio
        if ratio < 1:
            self.fitInView(self.pixmapItem, Qt.KeepAspectRatio)

    def resetTransform(self):
        """ Reset transform """
        super().resetTransform()
        self.zoomInTimes = 0
        self.__setDragEnabled(False)

    def __isEnableDrag(self):
        """ Decide whether to enable drag and drop based on the size of the image """
        v = self.verticalScrollBar().maximum() > 0
        h = self.horizontalScrollBar().maximum() > 0
        return v or h

    def __setDragEnabled(self, isEnabled: bool):
        """ Sets whether to start dragging """
        self.setDragMode(
            self.ScrollHandDrag if isEnabled else self.NoDrag)

    def __getScaleRatio(self):
        """ Gets the zoom ratio of the displayed image to the original image """
        if self.pixmap.isNull():
            return 1

        pw = self.pixmap.width()
        ph = self.pixmap.height()
        rw = min(1, self.width()/pw)
        rh = min(1, self.height()/ph)
        return min(rw, rh)

    def fitInView(self, item: QGraphicsItem, mode=Qt.KeepAspectRatio):
        """ Scale the scene to fit the window size """
        super().fitInView(item, mode)
        self.displayedImageSize = self.__getScaleRatio()*self.pixmap.size()
        self.zoomInTimes = 0

    def zoomIn(self, viewAnchor=QGraphicsView.AnchorUnderMouse):
        """ Enlarge the image """
        if self.zoomInTimes == self.maxZoomInTimes:
            return

        self.setTransformationAnchor(viewAnchor)

        self.zoomInTimes += 1
        self.scale(1.1, 1.1)
        self.__setDragEnabled(self.__isEnableDrag())

        # 还原 anchor
        self.setTransformationAnchor(self.AnchorUnderMouse)

    def zoomOut(self, viewAnchor=QGraphicsView.AnchorUnderMouse):
        """ Zoom out image """
        if self.zoomInTimes == 0 and not self.__isEnableDrag():
            return

        self.setTransformationAnchor(viewAnchor)

        self.zoomInTimes -= 1

        # The size of the original image
        pw = self.pixmap.width()
        ph = self.pixmap.height()

        # The width of the image actually displayed
        w = self.displayedImageSize.width()*1.1**self.zoomInTimes
        h = self.displayedImageSize.height()*1.1**self.zoomInTimes

        if pw > self.width() or ph > self.height():
            # Disallow further shrinking when the window size is smaller than the original image
            if w <= self.width() and h <= self.height():
                self.fitInView(self.pixmapItem)
            else:
                self.scale(1/1.1, 1/1.1)
        else:
            # When the window size is larger than the image, it is not allowed to shrink smaller than the original image
            if w <= pw:
                self.resetTransform()
            else:
                self.scale(1/1.1, 1/1.1)

        self.__setDragEnabled(self.__isEnableDrag())

        # Restoring anchor
        self.setTransformationAnchor(self.AnchorUnderMouse)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = ImageWidget()
    w.show()
    sys.exit(app.exec_())
