import time
import cv2
import tkinter as tk

from PyQt5 import uic, QtGui
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap, QImage, QIcon
from PyQt5.QtWidgets import QWidget, QMessageBox
from tkinter import filedialog


class CameraWidget(QWidget):
    file_path = None
    flag = 1
    image = None
    showImage = None

    def __init__(self, parent=None):
        super(CameraWidget, self).__init__()

        self.ui = uic.loadUi("./UI/CameraUI.ui")
        self.ui.pathBtn.clicked.connect(self.set_path)
        self.ui.takeBtn.clicked.connect(self.capture_image)
        self.ui.startBtn.clicked.connect(self.save_video)

        self.cap = cv2.VideoCapture(0)  # Camera
        self.camera_timer = QTimer()
        self.camera_timer.timeout.connect(self.show_video)

        self.start_video()
        self.photo_flag = 0
        self.ui.camera.setScaledContents(True)  # Image self adaptation
        self.ui.imageShow.setScaledContents(True)  # Image self adaptation
        self.ui.takeBtn.setEnabled(False)
        self.ui.startBtn.setEnabled(False)

    def start_video(self):

        self.camera_timer.start()
        # self.show_video()

    def stop_video(self):
        self.camera_timer.stop()
        # self.cap.release()
        # self.ui.camera.clear()

    def set_path(self):

        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askdirectory()
        print(file_path)
        if file_path == "":
            return

        self.file_path = file_path
        self.ui.pathLabel.setText(self.file_path)
        self.ui.takeBtn.setEnabled(True)
        self.ui.startBtn.setEnabled(True)

    def show_video(self):
        flag, self.image = self.cap.read()  # Read a picture from a video stream
        image_show = cv2.resize(self.image, (1280, 720))  # Reset the size of the read frame to 600 x 360
        width, height = image_show.shape[:2]  # Row: width, column: height
        image_show = cv2.cvtColor(image_show, cv2.COLOR_BGR2RGB)  # Reset the size of the read frame to
        # 600*360opencv. The read channel is BGR and will be converted to RGB
        image_show = cv2.flip(image_show, 1)  # Flip horizontally because the camera is mirrored.
        # Convert the video data read into print master form (picture data, height, width,RGB color space, 3 channels
        # each with 2 * * 8 = 256 colors)
        self.showImage = QtGui.QImage(image_show.data, height, width, QImage.Format_RGB888)
        self.ui.camera.setPixmap(QPixmap.fromImage(self.showImage))  # Displays the QImage on the Label that displays
        # the video

    def capture_image(self):

        if self.file_path is None:
            return

        if self.cap.isOpened():
            FName = fr"cap{time.strftime('%Y%m%d%H%M%S', time.localtime())}"
            print(FName)
            self.ui.imageShow.setPixmap(QtGui.QPixmap.fromImage(self.showImage))
            # self.showImage.save(FName + ".jpg", "JPG", 100)
            self.showImage.save(self.file_path + '/{}.jpg'.format(FName))
        else:
            QMessageBox.critical(self, 'Error', 'camera is not open!')
            return None

    def save_video(self):
        if self.flag == 1:
            self.ui.startBtn.setEnabled(False)
            self.flag = 0
            # print(self.cap.get(cv2.CAP_PROP_FPS))
            # Switching images
            icon_pause = QIcon()
            icon_pause.addFile("C://Users//Oceans//Desktop//DataAcquisition//MyProject//Element//pause.png")
            self.ui.startBtn.setIcon(icon_pause)
            self.ui.startBtn.setFixedSize(70,70)

            self.stop_video()
            # stop previous camera
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # Format for saving

            temp = self.file_path.split("/")
            real_path = ""
            for i in range(0, len(temp)):

                real_path += temp[i]
                if i != len(temp) - 1:
                    real_path += "\\"

            file_name = fr"video{time.strftime('%Y%m%d%H%M%S', time.localtime())}"
            vm = cv2.VideoWriter(real_path + "\\{}.mp4".format(file_name), fourcc, 30,
                                 (640,
                                  480))  # The first parameter is the file name, the second parameter is the file
            # name, the third parameter is the frame rate, and the fourth parameter is the size of the file

            self.ui.startBtn.setEnabled(True)
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    print("camera is not open")

                frame = cv2.flip(frame, 1)
                vm.write(frame)  # Save video
                cv2.imshow("Recording...", frame)
                cv2.waitKey(1)
                # if key == ord("q"):
                #     break
                if self.flag == 1:
                    break

            vm.release()
            # release resources
            cv2.destroyAllWindows()
            self.start_video()

        else:
            self.flag = 1
            icon_record = QIcon()
            icon_record.addFile("C://Users//Oceans//Desktop//DataAcquisition//MyProject//Element//record.png")
            self.ui.startBtn.setIcon(icon_record)
            self.ui.startBtn.setFixedSize(80,50)
