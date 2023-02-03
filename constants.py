from collections import namedtuple
from PyQt6.QtCore import QSize 
from PyQt6.QtGui import QColorConstants, QColor
import numpy as np

BGCOLOR = QColor("#333333")
FGCOLOR = QColor("#444444")
SHADOWCOLOR = QColor("#555555")
ACCENT1 = QColorConstants.White #QColor("#FF505D")
ACCENT2 = QColor("#6437FF")
ALERT = QColorConstants.Red
LINECOLOR = QColorConstants.Black

ATOM_SIZE = 30
WIRE_SIZE = 3

RYDGERG_BLOCKADE = 6.1e-6 #in m
SCALE = 60
MIN_YSPACING = .66
MIN_SPACING = .66

MAXHEIGHT = 12.46 #in diskgraph units
MAXWIDTH = 12.3

SHADOW_WIDTH = 2