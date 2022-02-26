import os
import PyQt5.QtWidgets as qt
from PyQt5.QtCore import QObject, pyqtSignal, QThread
import win32clipboard as wc


class WorkerDownloadConsole(QThread):
    link = ""
    img_range = ""

    def __init__(self, link):
        super().__init__()
        self.link = link

    def run(self):
        self.link = self.link
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
        self.link_input_field = qt.QLineEdit()
        self.link_input_field.returnPressed.connect(self.worker_download)
        self.link_input_field.setMinimumWidth(300)
        self.download_button = qt.QPushButton("Start Download", clicked=self.worker_download)
        self.download_list_box = qt.QListWidget()
        self.download_list_box.setMinimumSize(400, 200)
        self.finished_list_box = qt.QListWidget()
        self.finished_list_box.setMinimumSize(400, 200)
        self.download_list_label = qt.QLabel("Downloading")
        self.finished_list_label = qt.QLabel("Finished")
        self.image_range = qt.QLabel("Images number")
        self.image_range_input = qt.QLineEdit()
        self.image_range_input.returnPressed.connect(self.worker_download)
        self.image_range_input.setPlaceholderText("e.g : 1-2")
        self.image_range_input.setMaximumWidth(150)
        self.batch_download_button = qt.QPushButton("Batch download from file")
        # self.batch_download_button.setMaximumWidth(152)
        self.clipboard_download_button = qt.QPushButton("Download from Clipboard")

        central_widget.layout().addWidget(self.link_label, 0, 0)
        central_widget.layout().addWidget(self.link_input_field, 0, 1, 1, 2)
        central_widget.layout().addWidget(self.image_range, 1, 0)
        central_widget.layout().addWidget(self.image_range_input, 1, 1)
        central_widget.layout().addWidget(self.download_button, 2, 0)
        central_widget.layout().addWidget(self.batch_download_button, 2, 1)
        central_widget.layout().addWidget(self.clipboard_download_button, 2, 2)

        central_widget.layout().addWidget(self.download_list_label, 3, 0)
        central_widget.layout().addWidget(self.download_list_box, 4, 0, 1, 3)
        central_widget.layout().addWidget(self.finished_list_label, 5, 0)
        central_widget.layout().addWidget(self.finished_list_box, 6, 0, 1, 3)

    def update_download_list(self):
        self.download_list_box.clear()
        self.download_list_box.addItems(self.download_list)

    def update_finished_list(self):
        self.finished_list_box.clear()
        self.finished_list_box.addItems(self.finished_list)

    def download_to_finished(self, link):
        self.download_list.remove(link)
        self.finished_list.append(link)

    # def delete_link(self):
    #     link = self.delete_field.text()
    #     delete_item = self.download_list_box.findItems(link, QtCore.Qt.MatchExactly)
    #     if len(delete_item) == 0:
    #         self.statusBar().showMessage(link + " Not found")
    #     else:
    #         r = self.download_list_box.row(delete_item[0])
    #         self.download_list_box.takeItem(r)
    #         self.statusBar().showMessage(delete_item[0].__str__())

    def worker_download(self):
        link = ""
        if "." not in self.link_input_field.text() and "/" not in self.link_input_field.text():
            wc.OpenClipboard()
            data = wc.GetClipboardData()
            wc.CloseClipboard()
            if "." not in data:
                qt.QMessageBox.information(self, "Done", "A valid link must be in the input field or system clipboard")
                return
            else:
                link = data
        else:
            link = self.link_input_field.text()
        if self.image_range_input.text():
            link = link + " --range " + self.image_range_input.text()
        if "." in link and "/" in link:
            self.link_input_field.clear()
            self.statusBar().showMessage("Downloading " + link)
            self.download_list.append(link)
            self.update_download_list()
            self.worker = WorkerDownloadConsole(link)
            self.worker.start()
            self.worker.finished.connect(lambda: self.download_worker_finished(link))
        else:
            qt.QMessageBox.information(self, "Done", "A valid link must be in the input field or system clipboard")
    def download_worker_finished(self, link):
        lnk = link
        self.statusBar().showMessage("Finished downloading: " + link)
        self.download_to_finished(lnk)
        self.update_download_list()
        self.update_finished_list()


app = qt.QApplication([])
main_window = MainWindow()
main_window.show()
app.exec_()
