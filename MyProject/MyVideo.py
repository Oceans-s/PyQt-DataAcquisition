import tkinter as tk

from tkinter import filedialog
from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QFileDialog
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from MyVideoSurface import myVideoSurface
from MyVideoWidget import myVideoWidget


class VideoWidget(QWidget):

    flag = 1

    def __init__(self):
        super(VideoWidget, self).__init__()
        # self.setupUi(self)

        self.ui = uic.loadUi("./UI/VideoUI.ui")

        self.grab_player_position = 0  # Where the video is playing when the screenshot is taken
        self.grab_player_state = QMediaPlayer.StoppedState  # Video playback status when taking a screenshot
        self.sld_video_pressed = False    # Check whether the current progress bar is clicked
        self.videoFullScreen = False  # Determines whether the current widget is full screen
        self.videoFullScreenWidget = myVideoWidget()  # Create a full screen widget
        self.VideoSurface = myVideoSurface()

        self.player = QMediaPlayer()
        self.player.setVideoOutput(self.ui.wgt_video)  # Video playback output to videosurface

        self.ui.btn_open.clicked.connect(self.openVideoFile)  # Open video file button
        self.ui.btn_play.clicked.connect(self.playVideo)  # play
        # self.ui.btn_stop.clicked.connect(self.pauseVideo)  # pause
        self.ui.btn_cast.clicked.connect(self.start_grab_video)  # Screenshot of video
        self.ui.btn_path.clicked.connect(self.set_path)

        self.VideoSurface.FinishGrab.connect(self.finish_grab_video)
        self.player.positionChanged.connect(self.changeSlide)  # change Slide
        self.videoFullScreenWidget.doubleClickedItem.connect(self.videoDoubleClicked)  # Double click response

        self.ui.wgt_video.doubleClickedItem.connect(self.videoDoubleClicked)  # Double click response
        self.ui.sld_video.setTracking(False)
        self.ui.sld_video.sliderReleased.connect(self.releaseSlider)
        self.ui.sld_video.sliderPressed.connect(self.pressSlider)
        self.ui.sld_video.sliderMoved.connect(self.moveSlider)  # Progress bar drag-and-drop jump
        self.ui.sld_video.ClickedValue.connect(self.clickedSlider)  # Progress bar click jump
        self.ui.sld_audio.valueChanged.connect(self.volumeChange)  # Control sound playback

    def set_path(self):

        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askdirectory()
        print(file_path)
        if file_path == "":
            return

        self.VideoSurface.file_path = file_path
        self.ui.btn_cast.setEnabled(True)

    def start_grab_video(self):
        # Record the current playback information for the convenience of resuming playback
        if self.player.state() != QMediaPlayer.StoppedState:
            self.grab_player_state = self.player.state()
            self.grab_player_position = self.player.position()
            self.player.pause()  # Pause the current playback
            self.player.setVideoOutput(self.VideoSurface)  # Set the output to frame capture
            self.player.setPosition(self.grab_player_position)
            self.player.play()

    def finish_grab_video(self):
        # After the video capture is complete, the original playback status is restored
        self.player.stop()
        self.player.setVideoOutput(self.ui.wgt_video)
        self.player.setPosition(self.grab_player_position)
        if self.grab_player_state == QMediaPlayer.PlayingState:
            self.player.play()

    def volumeChange(self, position):
        volume = round(position / self.ui.sld_audio.maximum() * 100)
        print("vlume %f" % volume)
        self.player.setVolume(volume)
        self.ui.lab_audio.setText(str(volume) + "%")

    def clickedSlider(self, position):
        if self.player.duration() > 0:  # The jump is not allowed until it starts playing
            video_position = int((position / 100) * self.player.duration())
            self.player.setPosition(video_position)
            # self.ui.lab_video.setText("%.2f%%" % position)
        else:
            self.ui.sld_video.setValue(0)

    def moveSlider(self, position):
        self.sld_video_pressed = True
        if self.player.duration() > 0:  # The jump is not allowed until it starts playing
            video_position = int((position / 100) * self.player.duration())
            self.player.setPosition(video_position)
            # self.ui.lab_video.setText("%.2f%%" % position)

    def pressSlider(self):
        self.sld_video_pressed = True
        print("pressed")

    def releaseSlider(self):
        self.sld_video_pressed = False

    def changeSlide(self, position):
        if not self.sld_video_pressed:  # The progress bar does not update when clicked
            self.vidoeLength = self.player.duration() + 0.1
            self.ui.sld_video.setValue(round((position / self.vidoeLength) * 100))
            # self.ui.lab_video.setText("%.2f%%" % ((position / self.vidoeLength) * 100))

    def openVideoFile(self):
        self.player.setMedia(QMediaContent(QFileDialog.getOpenFileUrl()[0]))  # Selecting a Video file
        self.player.play()  # Play Video
        icon_pause = QIcon()
        icon_pause.addFile("C://Users//Oceans//Desktop//DataAcquisition//MyProject//Element//pause.png")
        self.ui.btn_play.setIcon(icon_pause)
        self.ui.btn_play.setEnabled(True)

    def playVideo(self):
        if self.flag == 1:
            self.flag = 0
            self.player.pause()
            icon_pause = QIcon()
            icon_pause.addFile("C://Users//Oceans//Desktop//DataAcquisition//MyProject//Element//play.png")
            self.ui.btn_play.setIcon(icon_pause)
        else:
            self.flag = 1
            self.player.play()
            icon_play = QIcon()
            icon_play.addFile("C://Users//Oceans//Desktop//DataAcquisition//MyProject//Element//pause.png")
            self.ui.btn_play.setIcon(icon_play)

    def videoDoubleClicked(self, text):

        if self.player.duration() > 0:  # The full screen operation is not allowed until the playback starts
            if self.videoFullScreen:
                self.player.setVideoOutput(self.ui.wgt_video)
                self.videoFullScreenWidget.hide()
                self.videoFullScreen = False
            else:
                self.videoFullScreenWidget.show()
                self.player.setVideoOutput(self.videoFullScreenWidget)
                self.videoFullScreenWidget.setFullScreen(1)
                self.videoFullScreen = True
