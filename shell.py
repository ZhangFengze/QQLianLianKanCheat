from board import FixSizeBoard, Grid
from solver import Steps
from memory import GetGridsFromMemory
from screen import GameRegionRect
from windows import PositionToScreen, FindWindow, GetWindowThreadProcessId, Click


def ErrorExit(log):
    print(log)
    exit(-1)


def GetGameWindow():
    windowTitle = "QQ游戏 - 连连看角色版"
    window = FindWindow(windowTitle)
    if window is None:
        ErrorExit(f"can not find window: {windowTitle}")
    return window


def GetGrids():
    window = GetGameWindow()
    _, process = GetWindowThreadProcessId(window)
    return GetGridsFromMemory(process)


def Solve(board):
    for step, board in Steps(board):
        startPosition, endPosition = step
        print(f"from {startPosition} to {endPosition}")
        print(board)

        gameRect = GameRegionRect(GetGameWindow())
        Click(PositionToScreen(startPosition, gameRect, 11, 19))
        Click(PositionToScreen(endPosition, gameRect, 11, 19))


if __name__ == "__main__":
    grids = GetGrids()
    grids = [grid if grid != 0 else Grid.Empty for grid in grids]
    board = FixSizeBoard(19, 11)(list(grids))
    Solve(board)
