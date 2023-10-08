from PySide2 import QtWidgets
from PySide2 import QtGui
from PySide2 import QtCore

import main, sys

class FileBrowser(main.Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self):
        super(FileBrowser, self).__init__()
        self.setupUi(self)
        self.treeView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeView.customContextMenuRequested.connect(self.context_menu)
        self.populate()

    def populate(self):
        self.model = QtWidgets.QFileSystemModel()
        self.model.setRootPath((QtCore.QDir.rootPath()))
        self.treeView.setModel(self.model)
        self.treeView.setSortingEnabled(True)

    def context_menu(self):
        menu = QtWidgets.QMenu()
        open = menu.addAction("Open")
        open.triggered.connect(self.open_file)
        cursor = QtGui.QCursor()
        menu.exec_(cursor.pos())

    def open_file(self):
        index = self.treeView.currentIndex()
        file_path = self.model.filePath(index)
        f = open("path.txt", 'w')
        f.write(file_path)
        f.close()
        sys.exit()

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    fb = FileBrowser()
    fb.show()
    app.exec_()