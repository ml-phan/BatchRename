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

        #QTree to view directory
        self.model = qt.QFileSystemModel()
        self.model.setRootPath("")
        self.tree = qt.QTreeView()
        self.tree.setModel(self.model)
        self.tree.setAnimated(False)
        self.tree.setIndentation(20)
        self.tree.setSortingEnabled(True)
        self.tree.resize(640, 480)
        self.tree.setSelectionMode(qt.QAbstractItemView.MultiSelection)
        central_widget.layout().addWidget(self.tree)

app = qt.QApplication([])
main_window = MainWindow()
main_window.show()
app.exec_()