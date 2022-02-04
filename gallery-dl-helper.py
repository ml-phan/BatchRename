import os
import time
import subprocess
from subprocess import CREATE_NO_WINDOW
import concurrent.futures

from PyQt5 import QtCore
import PyQt5.QtWidgets as qt
from PyQt5.QtCore import QObject, pyqtSignal, QThread


class WorkerDownloadConsole(QThread):
    link = ""
    img_range = ""

    def __init__(self, link, img_range):
        super().__init__()
        self.link = link
        self.img_range = img_range

    def run(self):
        if not self.img_range:
            self.link = self.link + " --range " + self.img_range
        os.system("gallery-dl " + self.link)


class MainWindow(qt.QMainWindow):
    def __init__(self):
        super().__init__()
        self.download_list = []
        self.finished_list = []
        self.setWindowTitle("gallery-dl-helper")
        self.statusBar().showMessage("Ready")
        self.setGeometry(800, 200, 0, 0)
        central_widget = qt.QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setLayout(qt.QGridLayout())

        self.link_label = qt.QLabel("Link")
        self.link_field = qt.QLineEdit()
        # self.link_field.returnPressed.connect(self.download_clicked)
        self.link_field.setMinimumWidth(300)
        self.download_button = qt.QPushButton("Start Download", clicked=self.worker_download)
        self.download_list_box = qt.QListWidget()
        # self.download_button.setMaximumWidth(100)
        self.download_list_box.setMinimumSize(400, 400)
        # self.delete_button = qt.QPushButton("Delete", clicked=self.delete_link)
        # self.delete_field = qt.QLineEdit()
        self.finished_list_box = qt.QListWidget()
        self.finished_list_box.setMinimumSize(400, 400)
        self.download_list_label = qt.QLabel("Downloading")
        self.finished_list_label = qt.QLabel("Finished")
        self.image_range = qt.QLabel("Images number")
        self.image_range_input = qt.QLineEdit()
        self.image_range_input.setPlaceholderText("e.g : 1-2")
        self.image_range_input.setMaximumWidth(150)

        central_widget.layout().addWidget(self.link_label, 0, 0)
        central_widget.layout().addWidget(self.link_field, 0, 1)
        central_widget.layout().addWidget(self.download_button, 2, 0)
        central_widget.layout().addWidget(self.image_range, 1, 0)
        central_widget.layout().addWidget(self.image_range_input, 1, 1)

        central_widget.layout().addWidget(self.download_list_label, 3, 0)
        central_widget.layout().addWidget(self.download_list_box, 4, 0, 1, 3)
        central_widget.layout().addWidget(self.finished_list_label, 5, 0)
        central_widget.layout().addWidget(self.finished_list_box, 6, 0, 1, 3)
        # central_widget.layout().addWidget(self.delete_field)
        # central_widget.layout().addWidget(self.delete_button)

    def download_console(self):
        link = self.link_field.text()
        self.link_field.clear()
        self.statusBar().showMessage("Downloading " + link)
        self.download_list.append(link)
        p = subprocess.call("gallery-dl " + link)
        self.download_to_finished(link)
        self.update_finished_list()

    def update_download_list(self):
        self.download_list_box.clear()
        self.download_list_box.addItems(self.download_list)

    def update_finished_list(self):
        self.finished_list_box.clear()
        self.finished_list_box.addItems(self.finished_list)

    def download_to_finished(self, link):
        self.download_list.remove(link)
        self.finished_list.append(link)

    def delete_link(self):
        link = self.delete_field.text()
        delete_item = self.download_list_box.findItems(link, QtCore.Qt.MatchExactly)
        if len(delete_item) == 0:
            self.statusBar().showMessage(link + " Not found")
        else:
            r = self.download_list_box.row(delete_item[0])
            self.download_list_box.takeItem(r)
            self.statusBar().showMessage(delete_item[0].__str__())

    def worker_download(self):
        link = self.link_field.text()
        img_range = ""
        if self.image_range_input.text() is not None:
            img_range = self.image_range_input.text()
        self.link_field.clear()
        self.statusBar().showMessage("Downloading " + link)
        self.download_list.append(link)
        self.update_download_list()
        self.worker = WorkerDownloadConsole(link, img_range)
        self.worker.start()
        self.worker.finished.connect(lambda: self.download_worker_finished(link))

    def download_worker_finished(self, link):
        lnk = link
        self.download_to_finished(lnk)
        self.update_download_list()
        self.update_finished_list()


app = qt.QApplication([])
main_window = MainWindow()
main_window.show()
app.exec_()
