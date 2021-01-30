from enum import Enum
import numpy as np


class Grid(Enum):
    Invalid = -1
    Empty = 0


def FixSizeBoard(width, height):
    class Board:
        @staticmethod
        def Width():
            return width

        @staticmethod
        def Height():
            return height

        @staticmethod
        def Positions():
            return [np.array((x, y)) for y in range(height) for x in range(width)]

        def __init__(self, raw: np.array = None):
            self.raw = raw
            if self.raw is None:
                self.raw = np.array(
                    [Grid.Empty for position in Board.Positions()])

        def At(self, x, y):
            if x in range(width) and y in range(height):
                return self.raw[y*width+x]
            return Grid.Invalid

        def Set(self, x, y, v):
            return Board(np.array([v if ((x, y) == position).all() else self.At(*position) for position in Board.Positions()]))

    return Board


def PrintBoard(board):
    for y in range(board.Height()):
        line = "|"
        for x in range(board.Width()):
            grid = board.At(x, y)
            line = line+"    |" if grid == Grid.Empty else line+" %02d |" % grid
        print(line)


if __name__ == '__main__':
    Board = FixSizeBoard(3, 5)
    assert(Board().Set(0, 4, 3).At(0, 4) == 3)
    assert(Board().At(-1, 5) == Grid.Invalid)
    PrintBoard(Board().Set(0, 1, 5).Set(1, 4, 1))
