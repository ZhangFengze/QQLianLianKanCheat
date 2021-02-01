from enum import Enum
from typing import Union
import numpy as np
import itertools


class Grid(Enum):
    Invalid = -1
    Empty = 0


def Positions(rows: int, cols: int):
    return [np.array((col, row)) for row in range(rows) for col in range(cols)]


def FixSizeBoard(cols: int, rows: int):
    class Board:
        def __init__(self, raw: np.array = np.array([Grid.Empty for position in Positions(rows, cols)])):
            self.raw = raw

        def At(self, x: int, y: int) -> Union[Grid, int]:
            if x in range(cols) and y in range(rows):
                return self.raw[y*cols+x]
            return Grid.Invalid

        def Set(self, x: int, y: int, v: int):
            return Board(np.array([v if ((x, y) == position).all() else self.At(*position) for position in Board.Positions()]))

        def __str__(self):
            result = ""
            for y in range(rows):
                line = "|"
                for x in range(cols):
                    grid = self.At(x, y)
                    line = line+"    |" if grid == Grid.Empty else line+" %02d |" % grid
                result = result+line+"\n"
            return result

        @staticmethod
        def Positions():
            return Positions(rows, cols)

    return Board


if __name__ == '__main__':
    Board = FixSizeBoard(3, 5)
    assert(Board().Set(0, 4, 3).At(0, 4) == 3)
    assert(Board().At(-1, 5) == Grid.Invalid)
    print(Board().Set(0, 1, 5).Set(1, 4, 1))
