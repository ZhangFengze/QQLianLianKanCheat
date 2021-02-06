from __future__ import annotations
import numpy as np
from enum import Enum
from typing import NamedTuple
from typing import Optional
from itertools import count
from board import Grid

Direction = Enum('Direction', zip(
    ["Null", "Up", "Down", "Left", "Right"], count(1)))


def Offset(direction: Direction):
    return {
        Direction.Null: (0, 0),
        Direction.Up: (0, -1),
        Direction.Down: (0, 1),
        Direction.Left: (-1, 0),
        Direction.Right: (1, 0),
    }[direction]


class Plan(NamedTuple):
    direction: Direction
    cost: int


def PossiblePlans(direction: Direction):
    return {
        Direction.Null: (Plan(Direction.Up, 0),
                         Plan(Direction.Down, 0),
                         Plan(Direction.Left, 0),
                         Plan(Direction.Right, 0)),

        Direction.Up: (Plan(Direction.Up, 0),
                       Plan(Direction.Left, 1),
                       Plan(Direction.Right, 1)),

        Direction.Down: (Plan(Direction.Down, 0),
                         Plan(Direction.Left, 1),
                         Plan(Direction.Right, 1)),

        Direction.Left: (Plan(Direction.Left, 0),
                         Plan(Direction.Up, 1),
                         Plan(Direction.Down, 1)),

        Direction.Right: (Plan(Direction.Right, 0),
                          Plan(Direction.Up, 1),
                          Plan(Direction.Down, 1)),
    }[direction]


def Evaluate(board, targetGrid: int, nowPosition: np.array, lastTimeDirection: Direction, turnCountLeft: int) -> Optional(np.array):
    if turnCountLeft < 0:
        return None

    nowGrid = board.At(*nowPosition)
    if nowGrid == Grid.Invalid:
        return None

    if lastTimeDirection != Direction.Null and nowGrid != Grid.Empty:
        if nowGrid == targetGrid:
            return nowPosition
        else:
            return None

    for plan in PossiblePlans(lastTimeDirection):
        result = Evaluate(board, targetGrid, nowPosition +
                          Offset(plan.direction), plan.direction, turnCountLeft-plan.cost)
        if result is not None:
            return result
    return None


def FindOneStep(board):
    for position in board.Positions():
        thisGrid = board.At(*position)
        if thisGrid != Grid.Empty:
            result = Evaluate(board, thisGrid, np.array(
                position), Direction.Null, 2)
            if result is not None:
                return position, result
    return None


def Steps(board):
    while True:
        step = FindOneStep(board)
        if step is None:
            break

        startPosition, endPosition = step
        board = board.Set(*startPosition, Grid.Empty)
        board = board.Set(*endPosition, Grid.Empty)
        yield step, board


if __name__ == '__main__':
    from board import FixSizeBoard
    grids = (
        0,   0,   0,   0,   0,   0,   0,   0,   0,  11,   0,   0,   0,   0,   0,   3,   0,   0,   0,
        0,   0,  17,   5, 243,   0,   0,   0,   0,  17, 245,   0,   0,   0,  13,  14,   6,   0,   0,
        0,   6,  18,   7, 246,   3,   0,  11,   4,  11,  12,   8,   0,  14,   8,   7,   5,  11,   0,
        0,   0,  16,   9,   2,   0,   0,   0,  18,   5,  17,   0,   0,   0,  14,   8, 243,   0,   0,
        0,   0,   0,  18,   0,   0,   0,   0,   0,   7,   0,   0,   0,   0,   0,  13,   0,   0,   0,
        0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
        0,  18,   9,   0, 246,  13,   0,   4,  14,   0,   9,   4,   0,  15,   8,   0,  17,  15,   0,
        0,   4,   0,   0,   0, 245,   0,  13,   0,   0,   0,  10,   0,  12,   0,   0,   0,  16,   0,
        0,   0,   0, 243,   0,   0,   0,   0,   0,   3,   0,   0,   0,   0,   0,  10,   0,   0,   0,
        0,  15,   0,   0,   0,   9,   0,  16,   0,   0,   0, 243,   0,   2,   0,   0,   0,  10,   0,
        0,   6,   2,   0,   2,  10,   0,  16,   3,   0,   5, 247,   0,   7, 247,   0,   6,  15,   0,
    )
    grids = [grid if grid != 0 else Grid.Empty for grid in grids]
    board = FixSizeBoard(19, 11)(grids)
    for _, nowBoard in Steps(board):
        board = nowBoard
    assert(
        all([board.At(*position) == Grid.Empty for position in board.Positions()]))
