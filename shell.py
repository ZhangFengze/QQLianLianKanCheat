from board import FixSizeBoard, Grid
from solver import Steps
from memory_scan import GetGridsFromMemory
from screen_scan import GameRegionRect
from windows import PositionToScreen, SetDpiAwareness, FindWindow, GetWindowThreadProcessId, WindowRect, Click


def ErrorExit(log):
    print(log)
    exit(-1)


if __name__ == "__main__":
    # fix screen-capture in different dpi
    SetDpiAwareness()

    windowTitle = "QQ游戏 - 连连看角色版"
    window = FindWindow(windowTitle)
    if window is None:
        ErrorExit(f"can not find window: {windowTitle}")

    thread, process = GetWindowThreadProcessId(window)
    grids = GetGridsFromMemory(process)
    grids = [grid if grid != 0 else Grid.Empty for grid in grids]
    board = FixSizeBoard(19, 11)(list(grids))

    for step, board in Steps(board):
        startPosition, endPosition = step
        print(f"from {startPosition} to {endPosition}")
        print(board)

        gameRect = GameRegionRect(WindowRect(window))
        Click(PositionToScreen(startPosition, gameRect, 11, 19))
        Click(PositionToScreen(endPosition, gameRect, 11, 19))
