from PySide2.QtWidgets import QFrame
from PySide2.QtGui import (
    QColorConstants,
    QPen,
    QPainter,
    QBrush,
    QLinearGradient,
    QImage,
    QGradient,
)
from PySide2.QtCore import Qt
from point import Point

import numpy as np

from constants import *


class SmartCanvas(QFrame):
    def __init__(self, gui):
        super().__init__()

        self.painter = QPainter()
        self.gui = gui

        self.atoms = []  # list of objects that can be clicked
        self.selected_atom = None  # object that is currently selected
        self.dragging_atom = None  # object that is currently selected

        self._dragging = False
        self._mouse_button = None

        self.potential = np.zeros(
            (round(SCALE * (MAXWIDTH + 2)), round(SCALE * (MAXHEIGHT + 2)))
        )

        self.background = QImage("../images/background.png")
        self.old_pos = Point(0, 0)

        self.draw_potential = True
        self.draw_links = True

    def atom_under(self, point, exclude=None):
        for atom in self.atoms:
            if atom == exclude:
                continue
            if atom.dist(point) < ATOM_SIZE/2:
                return atom
        return None

    def world_point(self, event):
        return Point(event.pos().x(), event.pos().y())

    def toggle_potential(self):
        if self.draw_potential:
            self.potential = np.zeros(
                (round(SCALE * (MAXWIDTH + 2)), round(SCALE * (MAXHEIGHT + 2)))
            )
            self.draw_potential = False
        else:
            self.draw_potential = True
            for atom in self.atoms:
                self.updatePotential(atom)
        self.update()

    def toggle_links(self):
        self.draw_links = not self.draw_links
        self.update()

    def clear(self):
        self.potential = np.zeros(
            (round(SCALE * (MAXWIDTH + 2)), round(SCALE * (MAXHEIGHT + 2)))
        )
        self.atoms.clear()
        self.update()

    def load(self, atoms):
        self.potential = np.zeros(
            (round(SCALE * (MAXWIDTH + 2)), round(SCALE * (MAXHEIGHT + 2)))
        )
        self.atoms = atoms
        for atom in self.atoms:
            self.updatePotential(atom)
        self.update()

    def paintEvent(self, event):
        self.painter.begin(self)
        self.painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        self._background()

        if self.draw_potential:
            self.drawPotential()

        if self.draw_links:
            self.drawLinks()

        for atom in self.atoms:
            gradient = QLinearGradient(
                int(atom.x - ATOM_SIZE / 2),
                int(atom.y - ATOM_SIZE / 2),
                int(atom.x + ATOM_SIZE / 2),
                int(atom.y + ATOM_SIZE / 2),
            )
            gradient.setColorAt(0, ACCENT1)
            gradient.setColorAt(1, ACCENT2)
            self.painter.setBrush(QBrush(gradient))
            self.painter.setPen(Qt.PenStyle.NoPen)
            self.painter.drawEllipse(
                int(atom.x - ATOM_SIZE / 2),
                int(atom.y - ATOM_SIZE / 2),
                ATOM_SIZE,
                ATOM_SIZE,
            )

        if self._dragging:
            self.painter.setBrush(Qt.BrushStyle.NoBrush)
            self.painter.setPen(QPen(QColorConstants.White))
            self.painter.drawEllipse(
                int(self.dragging_atom.x - SCALE),
                int(self.dragging_atom.y - SCALE),
                SCALE * 2,
                SCALE * 2,
            )
            self.painter.setPen(QPen(ALERT))
            self.painter.drawEllipse(
                int(self.dragging_atom.x - MIN_SPACING * SCALE),
                int(self.dragging_atom.y - MIN_SPACING * SCALE),
                int(MIN_SPACING * SCALE * 2),
                int(MIN_SPACING * SCALE * 2),
            )
        self.painter.end()

    def drawLinks(self):
        connection = QPen(CONNECTION)
        connection.setWidth(ATOM_SIZE)
        connection.setCapStyle(Qt.PenCapStyle.RoundCap)
        self.painter.setPen(connection)
        for i in range(len(self.atoms)):
            for j in range(i):
                if self.atoms[i].dist(self.atoms[j]) < SCALE:
                    self.painter.drawLine(
                        int(self.atoms[i].x),
                        int(self.atoms[i].y),
                        int(self.atoms[j].x),
                        int(self.atoms[j].y),
                    )

    def drawPotential(self):
        self.painter.setPen(QPen(POTENTIAL))
        for atom in self.atoms:
            for x in range(round(atom.x - SCALE), round(atom.x + SCALE)):
                for y in range(round(atom.y - SCALE), round(atom.y + SCALE)):
                    if self.potential[x][y] > 128 / (SCALE**6):
                        self.painter.drawPoint(x, y)

    def _background(self):  # solid background with grid
        painter = self.painter

        width = self.width()
        height = self.height()

        painter.fillRect(0, 0, width, height, BGCOLOR)
        painter.drawImage(0, 0, self.background)

        for i in range(round(MAXHEIGHT / MIN_YSPACING)):
            self._bar(
                SCALE + SHADOW_WIDTH,
                SCALE + i * MIN_YSPACING * SCALE + SHADOW_WIDTH,
                MAXWIDTH * SCALE,
                ATOM_SIZE,
                SHADOWCOLOR,
            )
            self._bar(
                SCALE,
                SCALE + i * MIN_YSPACING * SCALE,
                MAXWIDTH * SCALE,
                ATOM_SIZE,
                FGCOLOR,
            )

    def _bar(self, x, y, width, size, color):
        brush = QBrush(color)
        self.painter.setBrush(brush)
        self.painter.setPen(color)
        self.painter.drawEllipse(
            int(x - size / 2), int(y - size / 2), int(size), int(size)
        )
        self.painter.drawEllipse(
            int(x + width - size / 2), int(y - size / 2), int(size), int(size)
        )
        self.painter.drawRect(int(x), int(y - size / 2), int(width), int(size))

    def mouseMoveEvent(self, event) -> None:
        mouseloc = self.world_point(event)
        if event.buttons() == Qt.MouseButton.LeftButton:  # left button drag
            if not self._dragging and self.dragging_atom:
                self.updatePotential(self.dragging_atom, remove=True)
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
        if event.buttons() == Qt.MouseButton.LeftButton:  # select object under mouse
            self.leftButtonPress(mouseloc)
        self._mouse_button = event.buttons()

    def leftButtonPress(self, mouseloc):
        atom = self.atom_under(mouseloc)
        if atom:
            self.dragging_atom = atom
            self.old_pos.x = atom.x
            self.old_pos.y = atom.y
        else:
            self.dragging_atom = None

    def mouseReleaseEvent(self, event):
        mouseloc = self.world_point(event)
        if self._mouse_button == Qt.MouseButton.LeftButton:
            self.leftButtonRelease(mouseloc)
        elif self._mouse_button == Qt.MouseButton.RightButton:
            self.rightButtonRelease(mouseloc)
        self.update()

    def rightButtonRelease(self, mouseloc):
        atom = self.atom_under(mouseloc)
        if atom:
            self.atoms.remove(atom)
            self.updatePotential(atom, remove=True)

    def leftButtonRelease(self, mouseloc):
        if not self._dragging:
            self.leftclick(mouseloc)
        else:
            self.updatePotential(self.dragging_atom)

        self._dragging = False

    def leftclick(self, mouseloc):
        atom = self.atom_under(mouseloc)
        if atom:
            return
        new_atom = Point(mouseloc.x, mouseloc.y)
        new_atom.snap()
        self.atoms.append(new_atom)
        self.updatePotential(new_atom)
        self.update()

    def updatePotential(self, loc, remove=False):
        if not self.draw_potential:
            return
        if remove:
            sgn = -1
        else:
            sgn = 1
        for x in range(round(loc.x - SCALE), round(loc.x + SCALE)):
            for y in range(round(loc.y - SCALE), round(loc.y + SCALE)):
                if loc.dist(Point(x, y)) > ATOM_SIZE / 2 - 1:
                    self.potential[x, y] += sgn / loc.dist(Point(x, y)) ** 6

    def delete_selected(self):
        raise NotImplementedError
