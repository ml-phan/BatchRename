import os
import time
import validators

import PyQt5.QtWidgets as qt
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot


class MainWindow(qt.QMainWindow):
    def __init__(self):
        super().__init__()
        self.standby_list = []
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
        self.link_input_field.setMinimumWidth(500)
        self.download_button = qt.QPushButton("Start Download", clicked=self.worker_download)
        self.standby_label = qt.QLabel("Stand by list")
        self.standby_list_box = qt.QListWidget()
        self.standby_list_box.setSelectionMode(qt.QAbstractItemView.ExtendedSelection)
        self.standby_list_box.setMinimumSize(400, 200)
        self.standby_download_one = qt.QPushButton("Download selected items")
        self.standby_download_all = qt.QPushButton("Download all")
        self.standby_delete = qt.QPushButton("Delete selected items", clicked=self.delete_item_standby_list)
        self.standby_clear = qt.QPushButton("Delete all", clicked=self.clear_standby_list)
        self.standby_clear.setMinimumWidth(150)
        self.standby_delete.setMinimumWidth(150)
        self.standby_download_one.setMinimumWidth(150)
        self.standby_download_all.setMinimumWidth(150)
        self.download_list_box = qt.QListWidget()
        self.download_list_box.setMinimumSize(400, 200)
        self.finished_list_box = qt.QListWidget()
        self.finished_list_box.setMinimumSize(400, 200)
        self.download_list_label = qt.QLabel("Downloading list")
        self.finished_list_label = qt.QLabel("Finished list")
        self.image_range = qt.QLabel("Images number")
        self.image_range_input = qt.QLineEdit()
        self.image_range_input.returnPressed.connect(self.worker_download)
        self.image_range_input.setPlaceholderText("e.g : 1-2")
        self.batch_download_button = qt.QPushButton("Batch download from file")
        self.clipboard_download_button = qt.QPushButton("Download from Clipboard")

        central_widget.layout().addWidget(self.link_label, 0, 0)
        central_widget.layout().addWidget(self.link_input_field, 0, 1, 1, 3)
        central_widget.layout().addWidget(self.image_range, 1, 0)
        central_widget.layout().addWidget(self.image_range_input, 1, 1)
        central_widget.layout().addWidget(self.download_button, 2, 0)
        central_widget.layout().addWidget(self.batch_download_button, 2, 1)
        central_widget.layout().addWidget(self.clipboard_download_button, 2, 2)

        central_widget.layout().addWidget(self.standby_label, 3, 0)
        central_widget.layout().addWidget(self.standby_list_box, 4, 0, 1, 4)
        central_widget.layout().addWidget(self.standby_download_one, 5, 0)
        central_widget.layout().addWidget(self.standby_download_all, 5, 1)
        central_widget.layout().addWidget(self.standby_delete, 5, 2)
        central_widget.layout().addWidget(self.standby_clear, 5, 3)

        central_widget.layout().addWidget(self.download_list_label, 6, 0)
        central_widget.layout().addWidget(self.download_list_box, 7, 0, 1, 4)
        central_widget.layout().addWidget(self.finished_list_label, 8, 0)
        central_widget.layout().addWidget(self.finished_list_box, 9, 0, 1, 4)

        # self.clipboard_monitor = ClipboardMonitorWorker()
        # self.clipboard_monitor.start()
        # self.clipboard_monitor.link.connect(self.clipboard_copy)

    def update_standby_list(self):
        self.standby_list_box.clear()
        self.standby_list_box.addItems(self.standby_list)

    def update_download_list(self):
        self.download_list_box.clear()
        self.download_list_box.addItems(self.download_list)

    def update_finished_list(self):
        self.finished_list_box.clear()
        self.finished_list_box.addItems(self.finished_list)

    def delete_item_standby_list(self):
        if self.standby_list_box.selectedItems():
            for i in self.standby_list_box.selectedItems():
                self.standby_list_box.takeItem(self.standby_list_box.row(i))
        else:
            pass

    def clear_standby_list(self):
        self.standby_list_box.clear()

    def download_to_finished(self, link):
        self.download_list.remove(link)
        self.finished_list.append(link)

    def clipboard_copy(self, link):
        if link not in self.standby_list and "." in link and "/" in link:
            self.standby_list.append(link)
            self.update_standby_list()

    def worker_download(self):
        link = ""
        if "." not in self.link_input_field.text() and "/" not in self.link_input_field.text():
            data = clipboard.text()
            if "." not in data and "/" not in data:
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
        self.statusBar().showMessage("Finished downloading: " + link)
        self.download_to_finished(link)
        self.update_download_list()
        self.update_finished_list()

    def clipboard_change(self):
        link = clipboard.text()
        if link not in self.standby_list and "." in link and "/" in link:
            self.standby_list.append(link)
            self.update_standby_list()


# class ClipboardMonitorWorker(QThread):
#     link = pyqtSignal(str)
#
#     def run(self):
#         while True:
#             if clipboard.dataChanged():
#                 self.link.emit(clipboard.text())
#             wc.OpenClipboard()
#             if wc.GetClipboardData(wc.CF_TEXT):
#                 data = str(wc.GetClipboardData())
#                 self.link.emit(data)
#             wc.CloseClipboard()
#             time.sleep(0.5)


class WorkerDownloadConsole(QThread):
    link = ""
    img_range = ""

    def __init__(self, link):
        super().__init__()
        self.link = link

    def run(self):
        self.link = self.link
        os.system("gallery-dl " + self.link)


app = qt.QApplication([])
clipboard = app.clipboard()
main_window = MainWindow()
clipboard.dataChanged.connect(main_window.clipboard_change)
main_window.show()
app.exec_()
