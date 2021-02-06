from board import FixSizeBoard, Grid, Positions
from solver import FindOneStep
from typing import Iterable
from windows import *
import compare_image
import numpy
import datetime


def ErrorExit(log):
    print(log)
    exit(-1)


def GameRegionRect(windowRect: Rect) -> Rect:
    return Rect(
        windowRect.left + 14.0 / 800.0 * windowRect.width,
        windowRect.top + 181.0 / 600.0 * windowRect.height,
        windowRect.left + 603 / 800.0 * windowRect.width,
        windowRect.top + 566 / 600.0 * windowRect.height)


def GrabGameRegion(window: int) -> PIL.Image.Image:
    windowRect = WindowRect(window)
    gameRect = GameRegionRect(windowRect)
    return GrabScreenRect(gameRect)


def SplitIntoGrids(image: PIL.Image.Image, rows: int, cols: int):
    gridWidth, gridHeight = image.width/cols, image.height/rows
    for x, y in Positions(rows, cols):
        gridRect = Rect(x*gridWidth, y*gridHeight, (x+1)
                        * gridWidth, (y+1)*gridHeight)
        yield Crop(image, gridRect)


def Similarity(imageA: PIL.Image.Image, imageB: PIL.Image.Image) -> float:
    return compare_image.classify_hist_with_split(numpy.array(imageA), numpy.array(imageB),
                                                  size=imageA.size)


def EmptyGridImage(width: int, height: int) -> PIL.Image.Image:
    return PIL.Image.new("RGB", (width, height), (48, 76, 112))


def Categorize(images: Iterable[PIL.Image.Image]):
    known = [(0, EmptyGridImage(10, 10))]
    for image in images:
        similarities = [(id, Similarity(image, knownImage))
                        for id, knownImage in known]
        bestID, bestSimilarity = max(
            similarities, key=lambda x: x[1])
        if bestSimilarity > 0.95:
            yield bestID
        else:
            id = len(known)
            known.append((id, image))
            yield id


def Backup(image: PIL.Image.Image):
    now = str(datetime.datetime.now())
    now = now.replace(" ", "_").replace(":", ";")
    image.save(f"{now}.png")


def Steps(board):
    while True:
        step = FindOneStep(board)
        if step is None:
            break

        startPosition, endPosition = step
        board = board.Set(*startPosition, Grid.Empty)
        board = board.Set(*endPosition, Grid.Empty)
        yield step, board


def GetGridsFromMemory(processID):
    from ReadWriteMemory import ReadWriteMemory

    rwm = ReadWriteMemory()
    process = rwm.get_process_by_id(processID)
    process.open()

    '''
    player = [0x00181c88+0x000187f4+playerID*0x04]
    playerGrids = [player+0x04]+0x08
    '''

    for index in range(19*11):
        pointer = process.get_pointer(
            0x00181c88+0x000187f4, offsets=(0x04, 0x08+index))
        grid = process.read(pointer)
        yield grid & 0xff

    process.close()


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
