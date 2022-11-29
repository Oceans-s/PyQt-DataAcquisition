import os
import time
import tkinter as tk

from PyQt5.QtCore import QThread, pyqtSignal
from selenium.webdriver.common.by import By
from selenium import webdriver
from PyQt5 import uic, QtGui
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget
from tkinter import filedialog


class InternetWidget(QWidget):
    text = None
    total = None
    num = None

    def __init__(self, parent=None):
        super(InternetWidget, self).__init__(parent)

        self.ui = uic.loadUi("./UI/InternetUI.ui")

        self.thread = MyThread(self)

        self.timer = QTimer(self)
        self.count = 0

        self.ui.searchBtn.clicked.connect(self.search_click)
        self.ui.downBtn.clicked.connect(self.download_click)
        self.thread.signal_1.connect(self.receive_msg)
        self.thread.signal_2.connect(self.receive_str)
        self.timer.timeout.connect(self.operate)

    def operate(self):

        self.count += 1

        str_time = str(self.count)

        self.ui.timeLabel.setText("Running time: " + str_time + " Seconds")

    def search_click(self):
        self.timer.start(1000)
        self.ui.textEdit.clear()
        self.ui.searchBtn.setEnabled(False)
        input_edit = self.ui.inputEdit.text()
        print(input_edit)
        if input_edit != "" and input_edit.isspace() is False:
            self.text = self.ui.inputEdit.text()
            self.ui.textEdit.setText("Search: {}".format(self.text))
            self.ui.textEdit.append("Loading...")
            self.thread.get_total(self.text)
            self.thread.start()

        else:
            self.ui.downBtn.setEnabled(False)
            self.ui.textEdit.setText("Please enter content")

    def receive_msg(self, msg):
        self.timer.stop()
        self.count = 0
        if msg.isnumeric():
            self.ui.downBtn.setEnabled(True)
            self.ui.textEdit.setText("Search: {}".format(self.text))
            self.ui.textEdit.append("Results: {}".format(msg))
            self.total = int(msg)
            self.ui.searchBtn.setEnabled(True)
        else:
            self.ui.downBtn.setEnabled(False)
            self.ui.searchBtn.setEnabled(True)
            self.ui.textEdit.setText('Search: "{}"'.format(self.text))
            self.ui.textEdit.append(msg)

    def download_click(self):
        self.timer.start(1000)
        self.ui.downBtn.setEnabled(False)
        num_edit = self.ui.numEdit.text()
        print(num_edit)

        if num_edit.isnumeric():
            if int(num_edit) > self.total:
                self.ui.textEdit.append("Cannot exceed the total")
                self.ui.downBtn.setEnabled(True)
                return
            elif int(num_edit) > 100:
                self.ui.textEdit.append("Up to 100")
                self.ui.downBtn.setEnabled(True)
                return
            root = tk.Tk()
            root.withdraw()
            file_path = filedialog.askdirectory()
            print(file_path)
            if file_path == "":
                self.ui.downBtn.setEnabled(True)
                return
            self.ui.textEdit.setText(file_path)
            self.num = int(num_edit)
            self.ui.textEdit.append("Start crawling images...")

            self.thread.get_img(self.num, file_path)
            self.thread.start()

        else:
            self.ui.textEdit.append("Please enter a positive integer")
            self.ui.downBtn.setEnabled(True)

    def receive_str(self, text):
        self.timer.stop()
        self.count = 0
        self.ui.textEdit.append(text)
        self.ui.downBtn.setEnabled(True)


class MyThread(QThread):
    signal_1 = pyqtSignal(str)
    signal_2 = pyqtSignal(str)
    flag = None
    text = None
    num = None
    total = None
    file_path = None

    def __init__(self, main_form):
        super(MyThread, self).__init__()
        self.main_form = main_form

    def get_total(self, text):
        self.text = text
        self.flag = 0

    def get_img(self, num, file_path):
        self.num = num
        self.file_path = file_path
        self.flag = 1

    def run(self):
        if self.flag == 0:
            driver = webdriver.Chrome()
            driver.get("https://openi.nlm.nih.gov/gridquery?q={}".format(self.text))
            time.sleep(3)
            try:
                total = driver.find_element(By.CLASS_NAME, "regular.ng-binding").text.split()[5]
                self.total = total
                self.signal_1.emit(total)
            except:
                message = driver.find_element(By.CLASS_NAME, "no-results.ng-scope").text
                self.signal_1.emit(message)
            driver.quit()

        elif self.flag == 1:
            try:
                command = "F:\Anaconda3\python.exe C:/Users/Oceans/Desktop/DataAcquisition/MyProject/MyUrl.py {} {} {} {}".format(
                    self.text, self.num, self.total, self.file_path)
                with os.popen(command, "r") as p:
                    r = p.read().split("\n")
                    r.remove('')
                    print(r)
                    self.signal_2.emit(r[-1])

            except:
                self.signal_2.emit("Something went wrong...[main.py]")
