import os
import PyQt5.QtWidgets as qt
from PyQt5.QtCore import QThread


class WorkerDownloadConsole(QThread):

    def run(self):
        for i in range(1000000000):
            print(i)


class MainWindow(qt.QMainWindow):
    def __init__(self):
        super().__init__()
        central_widget = qt.QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setLayout(qt.QVBoxLayout())

        self.download_button = qt.QPushButton("Download", clicked=self.worker_download)
        central_widget.layout().addWidget(self.download_button)

    def worker_download(self):
        # self.link_field.clear()
        # self.statusBar().showMessage("Downloading " + link)
        # self.download_list.append(link)
        worker = WorkerDownloadConsole()
        worker.start()
        worker.finished.connect(self.download_worker_finished)


app = qt.QApplication([])
main_window = MainWindow()
main_window.show()
app.exec_()
