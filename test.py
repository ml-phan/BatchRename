import PyQt5.QtWidgets as qt


class MainWindow(qt.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("batch-renamer")
        central_widget = qt.QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setLayout(qt.QHBoxLayout())

        self.statusBar().showMessage("Ready")
        self.setGeometry(600, 300, 1200, 600)

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
        self.tree.setIndentation(10)
        self.tree.setSortingEnabled(True)
        self.tree.resize(1240, 980)
        self.tree.setSelectionMode(qt.QAbstractItemView.ExtendedSelection)
        self.tree.setColumnWidth(0, 300)
        self.tree.setColumnWidth(1, 100)

        # Add Widget to Central Widget
        self.left_widget.layout().addWidget(self.tree)
        central_widget.layout().addWidget(self.left_widget)
        central_widget.layout().addWidget(self.right_widget)


app = qt.QApplication([])
main_window = MainWindow()
main_window.show()
app.exec_()