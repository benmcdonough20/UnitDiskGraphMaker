from PyQt6.QtWidgets import QFrame, QApplication
from PyQt6.QtGui import QColorConstants, QTransform, QPen, QPainter, QBrush, QAction, QIcon, QLinearGradient, QImage
from PyQt6.QtCore import Qt
from point import Point

from constants import *

class SmartCanvas(QFrame):
    
    def __init__(self, gui):
        super().__init__()

        self.painter = QPainter()
        self.gui = gui

        self.atoms = [] #list of objects that can be clicked
        self.selected_atom = None #object that is currently selected
        self.dragging_atom = None #object that is currently selected

        self._dragging = False
        self._mouse_button = None

        self.background = QImage("./background.png")

    
    def atom_under(self, point, exclude = None):
        for atom in self.atoms:
            if atom == exclude:
                continue
            if atom.dist(point) < SCALE*MIN_YSPACING:
                return atom
        return None
    
    def world_point(self, event):
        return Point(event.position().x(), event.position().y())

    def paintEvent(self, event):
        self.painter.begin(self)
        self.painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        self._background()

        for atom in self.atoms:
            gradient = QLinearGradient(
                int(atom.x-ATOM_SIZE/2),
                int(atom.y-ATOM_SIZE/2),
                int(atom.x+ATOM_SIZE/2),
                int(atom.y+ATOM_SIZE/2)
            )
            gradient.setColorAt(0, ACCENT1)
            gradient.setColorAt(1, ACCENT2)
            self.painter.setBrush(QBrush(gradient))
            self.painter.drawEllipse(
                int(atom.x-ATOM_SIZE/2), 
                int(atom.y-ATOM_SIZE/2), 
                ATOM_SIZE,
                ATOM_SIZE
            )

        self.painter.end()

    def _background(self): #solid background with grid
        painter = self.painter

        width = self.width()
        height = self.height()

        painter.fillRect(0, 0, width, height, BGCOLOR)
        painter.drawImage(0, 0, self.background)

        for i in range(round(MAXHEIGHT/MIN_YSPACING)):
            self._bar(SCALE+SHADOW_WIDTH,
                SCALE+i*MIN_YSPACING*SCALE+SHADOW_WIDTH,
                MAXWIDTH*SCALE,
                ATOM_SIZE,
                SHADOWCOLOR
                )
            self._bar(SCALE,
                SCALE+i*MIN_YSPACING*SCALE,
                MAXWIDTH*SCALE,
                ATOM_SIZE,
                FGCOLOR
            )

    def _bar(self, x, y, width, size, color):
        brush = QBrush(color)
        self.painter.setBrush(brush)
        self.painter.setPen(color)
        self.painter.drawEllipse(
                int(x-size/2), 
                int(y-size/2), 
                int(size),
                int(size)
            )
        self.painter.drawEllipse(
                int(x+width-size/2), 
                int(y-size/2), 
                int(size),
                int(size)
            )
        self.painter.drawRect(
            int(x),
            int(y-size/2),
            int(width),
            int(size)
        )
        
    def mouseMoveEvent(self, event) -> None:
        mouseloc = self.world_point(event) 
        if event.buttons() == Qt.MouseButton.LeftButton: #left button drag
            if self.dragging_atom:
                self._dragging = True
                self._drag(mouseloc)

        self.update()
    
    def _drag(self, point):
        point.snap()
        atom = self.atom_under(point, exclude=self.dragging_atom)
        if self.dragging_atom and not atom:
            self.dragging_atom.moveto(point)
            self.dragging_atom.snap()

    def mousePressEvent(self, event) -> None:
        mouseloc = self.world_point(event) 
        if event.buttons() == Qt.MouseButton.LeftButton: #select object under mouse
            self.leftButtonPress(mouseloc)
        self._mouse_button = event.buttons()
    
    def leftButtonPress(self, mouseloc):
        atom = self.atom_under(mouseloc)
        if atom:
            self.dragging_atom = atom
        else:
            self.dragging_atom = None

    def mouseReleaseEvent(self,event):
        mouseloc = self.world_point(event)
        if self._mouse_button == Qt.MouseButton.LeftButton:
            self.leftButtonRelease(mouseloc)
        elif self._mouse_button == Qt.MouseButton.RightButton:
            self.rightButtonRelease(mouseloc)
        self.update()
    
    def leftButtonRelease(self, mouseloc):
        if not self._dragging:
            self.leftclick(mouseloc)
        self._dragging = False

    def leftclick(self, mouseloc):
        atom = self.atom_under(mouseloc)
        if atom:
            return
        new_atom = Point(mouseloc.x, mouseloc.y)
        new_atom.snap()
        self.atoms.append(new_atom)

    def delete_selected(self):
        raise NotImplementedError
