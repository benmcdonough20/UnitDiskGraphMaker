import numpy as np
from constants import SCALE, MIN_YSPACING, MAXHEIGHT, MAXWIDTH

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __mul__(self, other):
        if type(other) is list or type(other) is np.ndarray:
            x,y = np.array([self.x, self.y]) @ other
            return Point(x,y)
        elif type(other) is int or type(other) is float:
            return Point(self.x*other, self.y*other)
        else:
            raise Exception("Type", str(type(other)))
    
    def moveto(self, point):
        self.x = point.x
        self.y = point.y

    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __sub__(self, other):
        return Point(self.x-other.x, self.y-other.y)

    def __add__(self, other):
        return Point(self.x+other.x, self.y+other.y)
    
    def snap(self):
        self.y = np.max([
            np.min(
                [int((round(MAXHEIGHT/MIN_YSPACING))*MIN_YSPACING*SCALE+SCALE-SCALE*MIN_YSPACING),
                 round((self.y-SCALE)/(SCALE*MIN_YSPACING))*SCALE*MIN_YSPACING+SCALE]),
            SCALE])
        self.x = np.max([
            np.min([
                (MAXWIDTH+1)*SCALE,
                self.x
            ]),
            SCALE 
        ])

    def norm(self):
        return np.sqrt(self.x**2 + self.y**2)

    def dist(self, other):
        return (self-other).norm()

    def __str__(self):
        return str((self.x, self.y))