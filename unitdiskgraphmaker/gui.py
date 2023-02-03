from PyQt6.QtWidgets import (
    QMainWindow, 
    QToolBar, 
    QFileDialog,
    QApplication,
    QPushButton,
    QLabel,
)
from point import Point
import sys
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import QSize, Qt

from constants import *
from canvas import SmartCanvas


class CircuitGui(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Unit Disk Graph Maker")
        self.setMinimumSize(QSize(round(SCALE*(MAXWIDTH+2)), round(SCALE*(MAXHEIGHT+2))))

        self.canvas = SmartCanvas(self)

        self.init_toolbar()

        self.setCentralWidget(self.canvas)
        self.show()

    def init_toolbar(self):
        self.toolbar = QToolBar(self)

        open_file = QAction("", self)
        open_file.setIcon(QIcon("../icons/open.png"))
        self.toolbar.addAction(open_file)
        open_file.triggered.connect(self.load)

        save = QAction("",self)
        save.setIcon(QIcon("../icons/save.png"))
        self.toolbar.addAction(save)
        save.triggered.connect(self.save)

        clear = QAction("", self)
        clear.setIcon(QIcon("../icons/clear.png"))
        self.toolbar.addAction(clear)
        clear.triggered.connect(self.clear)

        export = QAction("", self)
        export.setIcon(QIcon("../icons/export.png"))
        self.toolbar.addAction(export)
        export.triggered.connect(self.export)
   
        togglePotential = QPushButton("", self)
        togglePotential.setIcon(QIcon("../icons/potential.png"))
        togglePotential.setCheckable(True)
        self.toolbar.addWidget(togglePotential)
        togglePotential.clicked.connect(self.togglePotential)

        toggleLinks = QPushButton("", self)
        toggleLinks.setIcon(QIcon("../icons/links.png"))
        toggleLinks.setCheckable(True)
        self.toolbar.addWidget(toggleLinks)
        toggleLinks.clicked.connect(self.toggleLinks)

        self.toolbar.setContextMenuPolicy(Qt.ContextMenuPolicy.PreventContextMenu)
        self.addToolBar(self.toolbar) 

    def save(self):
        fname = self.fchooser("Save File")
        with open(fname, "w") as f:
            for atom in self.canvas.atoms:
                f.write(str(atom.x)+","+str(atom.y)+"\n")

    def export(self):
        fname = self.fchooser("Export Points")
        with open(fname, "w") as f:
            f.write("x,y\n")
            for atom in self.canvas.atoms:
                f.write(f"{(atom.x-SCALE)/SCALE*RYDBERG_BLOCKADE},{(atom.y-SCALE)/SCALE*RYDBERG_BLOCKADE}\n")
    
    def togglePotential(self):
        self.canvas.toggle_potential()

    def toggleLinks(self):
        self.canvas.toggle_links()
    
    def load(self):
        fname = self.fchooser("Open File") 
        with open(fname, "r") as f:
            atoms = []
            for line in f.readlines():
                x,y = line.split(",")
                atoms.append(Point(float(x), float(y)))
        self.canvas.load(atoms)

    def fchooser(self, message):
        fname,_ = QFileDialog.getSaveFileName(
                self,
                message,
                "./",
                "(*.csv)",
            )
        return fname.split(".")[0]+".csv"

    def clear(self):
        self.canvas.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(open("../stylesheets/pyqt5-dark-theme.stylesheet").read())
    gui = CircuitGui()
    app.exec()