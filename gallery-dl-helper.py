import os
import time
import subprocess
from subprocess import CREATE_NO_WINDOW
import concurrent.futures

from PyQt5 import QtCore
import PyQt5.QtWidgets as qt


class MainWindow(qt.QMainWindow):
    def __init__(self):
        super().__init__()
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
        self.download_button = qt.QPushButton("Download", clicked=self.download_multi)
        self.download_list = qt.QListWidget()
        self.download_button.setMaximumWidth(100)
        self.download_list.setMinimumSize(400, 400)
        self.delete_button = qt.QPushButton("Delete", clicked=self.delete_link)
        self.delete_field = qt.QLineEdit()
        self.finished_list = qt.QListWidget()
        self.finished_list.setMinimumSize(400, 400)
        self.download_list_label = qt.QLabel("Downloading")
        self.finished_list_label = qt.QLabel("Finished")

        central_widget.layout().addWidget(self.link_label, 0, 1)
        central_widget.layout().addWidget(self.link_field, 0, 2)
        central_widget.layout().addWidget(self.download_button, 0, 0)

        central_widget.layout().addWidget(self.download_list_label, 1, 0)
        central_widget.layout().addWidget(self.download_list, 2, 0, 1, 3)
        central_widget.layout().addWidget(self.finished_list_label, 3, 0)
        central_widget.layout().addWidget(self.finished_list, 4, 0, 1, 3)
        central_widget.layout().addWidget(self.delete_field)
        central_widget.layout().addWidget(self.delete_button)

    # def download_clicked(self):
    #     link = self.link_field.text()
    #     self.link_field.clear()
    #     self.download_list.addItem(link)
    #     self.statusBar().showMessage("Downloading " + link)
    #     p = subprocess.Popen("gallery-dl " + link)
    #     self.finished_list.addItem(link)

    def delete_link(self):
        link = self.delete_field.text()
        delete_item = self.download_list.findItems(link, QtCore.Qt.MatchExactly)
        if len(delete_item) == 0:
            self.statusBar().showMessage(link + " Not found")
        else:
            r = self.download_list.row(delete_item[0])
            self.download_list.takeItem(r)
            self.statusBar().showMessage(delete_item[0].__str__())

    def download_multi(self):
        link = self.link_field.text()
        with concurrent.futures.ProcessPoolExecutor() as executor:
            executor.submit(lambda: os.system("Test"))


app = qt.QApplication([])
main_window = MainWindow()
main_window.show()
app.exec_()
