import os

import PyQt5.QtWidgets as qt
from os import listdir, path
import subprocess
from PyQt5 import QtCore


class Window(qt.QMainWindow):
    demo_path = ""
    def __init__(self):
        super().__init__()
        central_widget = qt.QWidget()
        # central_layout = qt.QVBoxLayout()
        central_widget.setLayout(qt.QVBoxLayout())
        self.setCentralWidget(central_widget)
        self.list_of_files = []

        # Initializing main components
        demo_path_segment = qt.QWidget()
        search_segment = qt.QWidget()
        append_segment = qt.QWidget()
        file_list_segment = qt.QWidget()
        file_list_operation_segment = qt.QWidget()
        current_argument = qt.QWidget()
        start_segment = qt.QWidget()

        # Adding main components to central layout
        central_widget.layout().addWidget(demo_path_segment)
        central_widget.layout().addWidget(append_segment)
        central_widget.layout().addWidget(file_list_segment)
        central_widget.layout().addWidget(search_segment)
        central_widget.layout().addWidget(file_list_operation_segment)
        central_widget.layout().addWidget(current_argument)
        central_widget.layout().addWidget(start_segment)

        # Initializing demo path segment components
        demo_path_label = qt.QLabel("Select Demo root folder:")
        self.demo_path_field = qt.QLineEdit()
        self.demo_path_field.setMinimumWidth(700)
        self.demo_path_field.setText(self.demo_path)
        demo_path_search_button = qt.QPushButton("Browse", clicked = self.dir_browse)

        # Adding demo path segment components
        demo_path_segment.setLayout(qt.QHBoxLayout())
        demo_path_segment.layout().addWidget(demo_path_label)
        demo_path_segment.layout().addWidget(self.demo_path_field)
        demo_path_segment.layout().addWidget(demo_path_search_button)
        if os.path.exists("path.txt"):
            with open("path.txt", "r") as f:
                demo_path_file = f.read()
                self.demo_path_field.setText(demo_path_file)
        # Initializing search segment components
        extension_label = qt.QLabel("File type:")
        extension_label.setMaximumWidth(50)
        search_button = qt.QPushButton("Search for files", clicked = self.file_search)
        search_button.setMaximumWidth(100)
        self.search_extension = qt.QLineEdit("avi")
        self.search_extension.setMaximumWidth(40)
        self.search_sub_checkbox = qt.QCheckBox("Includes sub folders")
        self.search_sub_checkbox.setChecked(True)

        # Adding search segment components
        search_segment.setLayout(qt.QHBoxLayout())
        search_segment.setMaximumWidth(400)
        search_segment.layout().addWidget(search_button)
        search_segment.layout().addWidget(extension_label)
        search_segment.layout().addWidget(self.search_extension)
        search_segment.layout().addWidget(self.search_sub_checkbox)
        

        # Initializing append segment components
        append_label = qt.QLabel("Output file names will be appended with")
        append_label.setMaximumWidth(300)
        append_label_outer = qt.QLabel("")
        self.append_field = qt.QLineEdit("annotated")
        self.append_field.setMaximumWidth(100)

        # Adding append segment components
        append_segment.setLayout(qt.QHBoxLayout())
        append_segment.layout().addWidget(append_label, 0, QtCore.Qt.AlignLeft)
        append_segment.layout().addWidget(self.append_field, 0, QtCore.Qt.AlignLeft)
        append_segment.layout().addWidget(append_label_outer)

        # Initializing file list segment components
        self.file_list = qt.QListWidget()
        self.file_list.setSelectionMode(qt.QAbstractItemView.ExtendedSelection)

        # Adding file list components
        file_list_segment.setLayout(qt.QVBoxLayout())
        file_list_segment.layout().addWidget(self.file_list)
        # self.file_list.addItem("C:/Videos/20210629_93ab407c_182711.avi")

        # Initializing file list operation components
        self.list_add_button = qt.QPushButton("Add file(s) manually", clicked = self.list_add)
        self.list_add_button.setMaximumWidth(150)
        self.list_delete_button = qt.QPushButton("Delete file(s) from list", clicked = self.list_delete)
        self.list_delete_button.setMaximumWidth(150)
        self.number_of_files_1 = qt.QLabel(" " + str(self.file_list.count()))
        self.number_of_files_1.setMaximumWidth(20)
        self.number_of_files_2 = qt.QLabel("files")

        # Adding file list operation components
        file_list_operation_segment.setLayout(qt.QHBoxLayout())
        file_list_operation_segment.layout().addWidget(self.list_add_button)
        file_list_operation_segment.layout().addWidget(self.list_delete_button)
        file_list_operation_segment.layout().addWidget(self.number_of_files_1)
        file_list_operation_segment.layout().addWidget(self.number_of_files_2)

        # Initializing argument segment
        self.default_parameter = "-config ../data/configuration_c151201NarrowGen3B0.2_B02#33LHD_demo_bclass.json -showLogo -numEmptyCircles 4 -drawIconOnFace FacialExpression,UseOfMobileDevice,Glasses,Mask -charts combined=1,addToVideo=0.75"
        self.arguments = qt.QPlainTextEdit(self.default_parameter)
        self.arguments_label = qt.QLabel("Current parameters:")

        # Adding argument segment
        current_argument.setLayout(qt.QVBoxLayout())
        current_argument.layout().addWidget(self.arguments_label)
        current_argument.layout().addWidget(self.arguments)

        # Initializing start segment components
        self.start_button = qt.QPushButton("Start", clicked = self.start_annotation)
        # self.stop_button = qt.QPushButton("Stop", )
        self.quit_button = qt.QPushButton("Quit", clicked = self.close)

        # Adding start segment components
        start_segment.setLayout(qt.QHBoxLayout())
        start_segment.layout().addWidget(self.start_button)
        # start_segment.layout().addWidget(self.stop_button)
        start_segment.layout().addWidget(self.quit_button)

    def dir_browse(self):
        dialog = qt.QFileDialog()
        dialog.setDirectory("C:/")
        folder_path = dialog.getExistingDirectory(None, "Select Demo's bin folder")
        self.demo_path_field.setText(folder_path)
        self.demo_path = folder_path
        with open("path.txt", "w+") as f:
            f.write(folder_path)

    def list_delete(self):
        if self.file_list.selectedItems():
            for i in self.file_list.selectedItems():
                self.file_list.takeItem(self.file_list.row(i))
        else:
            pass
        self.number_of_files_1.setText(" " + str(self.file_list.count()))

    def list_add(self):
        dialog = qt.QFileDialog()
        file_path = dialog.getOpenFileNames(self, "Select file to add to list")
        for i in file_path[0]:
            self.file_list.addItem(i)

    def file_search(self):
        dialog = qt.QFileDialog()
        dialog.setDirectory("C:/")
        folder_path = dialog.getExistingDirectory(self, "Select folder to search for video files")
        if self.search_sub_checkbox.isChecked():
            for i in self.sub_search(folder_path):
                self.file_list.addItem(i)
        else:
            self.root_search(folder_path)

    def sub_search(self, folder_path):
        list_of_files = listdir(folder_path)
        all_files = list()
        for i in list_of_files:
            full_path = path.join(folder_path, i)
            if path.isdir(full_path):
                all_files = all_files + self.sub_search(full_path)
            else:
                file_size = os.stat(full_path).st_size
                if full_path.endswith(self.search_extension.text()) and file_size > 52428800:
                    all_files.append(full_path)
        self.number_of_files_1.setText(" " + str(self.file_list.count()))
        return all_files

    def root_search(self, folder_path):
        list_of_files = listdir(folder_path)
        for i in list_of_files:
            full_path = path.join(folder_path, i)
            if full_path.endswith(self.search_extension.text()):
                self.file_list.addItem(full_path)
        self.number_of_files_1.setText(" " + str(self.file_list.count()))

    def start_annotation(self):
        if self.demo_path_field.text():
            all_files = self.file_list.findItems('*', QtCore.Qt.MatchWildcard)
            for i in all_files:
                final_command = "FrontendBinary.exe {} -cam \"{}\" -capture \"{}_{}.avi\"".format(self.arguments, i.text(), i.text()[:-4], self.append_field.text())
                if self.demo_path_field.text():
                    os.chdir(self.demo_path_field.text()+"/bin")
                subprocess.run(final_command)
                print(final_command)
        else:
            dialog = qt.QDialog()
            dialog.setLayout(qt.QVBoxLayout())
            dialog.setWindowTitle("Demo not found")
            label = qt.QLabel("Please specify path to the demo")
            button = qt.QPushButton("OK")
            dialog.layout().addWidget(label)
            dialog.layout().addWidget(button)
            dialog.exec_()


app = qt.QApplication([])
main_window = Window()
main_window.show()
app.exec_()
