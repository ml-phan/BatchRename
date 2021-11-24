import PyQt5.QtWidgets as qt


class MainWindow(qt.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("batch-renamer")
        central_widget = qt.QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setLayout(qt.QHBoxLayout())

        self.statusBar().showMessage("Ready")
        self.setGeometry(600, 300, 600, 300)

        # Tree Widget
        self.left_widget = qt.QWidget()
        self.left_widget.setLayout(qt.QVBoxLayout())
        self.right_widget = qt.QWidget()
        self.right_widget.setLayout(qt.QHBoxLayout())

        # QTree to view directory
        self.model = qt.QFileSystemModel()
        self.model.setRootPath("")
        self.tree = qt.QTreeView()
        self.tree.setModel(self.model)
        self.tree.setAnimated(False)
        self.tree.setIndentation(20)
        self.tree.setSortingEnabled(True)
        self.tree.resize(640, 480)
        self.tree.setSelectionMode(qt.QAbstractItemView.MultiSelection)

        self.rename_button = qt.QPushButton("Batch rename button", clicked=self.batch_rename)

        # Add Widget to Central Widget
        self.left_widget.layout().addWidget(self.tree)
        self.right_widget.layout().addWidget(self.rename_button)
        central_widget.layout().addWidget(self.left_widget)
        central_widget.layout().addWidget(self.right_widget)

    def batch_rename(self):
        dialog = qt.QDialog()
        dialog.setMinimumSize(600, 500)
        dialog.setWindowTitle("Batch rename")
        dialog.exec_()


class RenameWindow(qt.QMainWindow):
    def __init__(self):
        super().__init__()


app = qt.QApplication([])
main_window = MainWindow()
main_window.show()
app.exec_()
