from PyQt6.QtWidgets import (
    QMainWindow, 
    QToolBar, 
    QFileDialog,
    QApplication
)

import sys
from PyQt6.QtGui import QAction
from PyQt6.QtCore import QSize

from constants import *
from canvas import SmartCanvas


class CircuitGui(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Unitgraph Maker")
        self.setMinimumSize(QSize(round(SCALE*(MAXWIDTH+2)), round(SCALE*(MAXHEIGHT+2))))

        self.canvas = SmartCanvas(self)

        self.init_toolbar()

        self.setCentralWidget(self.canvas)
        self.show()

    def init_toolbar(self):
        self.toolbar = QToolBar(self)

        open_file = QAction("open", self)
        self.toolbar.addAction(open_file)
        open_file.triggered.connect(self.open_file)

        save = QAction("save", self)
        self.toolbar.addAction(save)
        save.triggered.connect(self.save)

        export = QAction("export", self)
        self.toolbar.addAction(export)
        export.triggered.connect(self.export)
        
        undo = QAction("undo", self)
        self.toolbar.addAction(undo)
        undo.triggered.connect(self.undo)

        redo = QAction("redo", self)
        self.toolbar.addAction(redo)
        redo.triggered.connect(self.redo)

        clear = QAction("clear", self)
        self.toolbar.addAction(clear)
        clear.triggered.connect(self.clear)

        self.addToolBar(self.toolbar) 
    
    def save(self):
        raise NotImplementedError
    
    def open(self, fname):
        raise NotImplementedError

    def take_snapshot(self):
        raise NotImplementedError
        self.caretaker.add_snapshot(Circuit.CircuitMemento(self.canvas.objects))

    def redo(self):
        raise NotImplementedError
        snapshot = self.caretaker.redo()
        self.canvas.restore(snapshot)
    
    def undo(self):
        raise NotImplementedError
        snapshot = self.caretaker.undo()
        self.canvas.restore(snapshot)

    def save_dialogue(self):
        fname,_ = QFileDialog.getSaveFileName(
                self,
                "Save File",
                "./",
                "Circuits (*.circuit)",
            )
        self.save(fname+".circuit")
    
    def open_file(self):
        fname,_ = QFileDialog.getOpenFileName(
                self,
                "Open File",
                "./",
                "Circuits (*.circuit)"
            )
        self.open(fname)
    
    def export(self):
        fname,_ = QFileDialog.getSaveFileName(
                self,
                "Save File",
                "./",
                "ScQubits circuit (*.yml)",
            )
        with open(fname+".yml", "w") as f:
            f.write(str(self.canvas.objects))

    def import_dialogue(self):
        fname,_ = QFileDialog.getOpenFileName(
                self,
                "Import File",
                "./",
                "Circuits (*.circuit)"
            )
        self.import_circuit(fname)

    def clear(self):
        self.canvas.atoms.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = CircuitGui()
    app.exec()