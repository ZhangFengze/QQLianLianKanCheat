from board import Grid, Positions
from typing import Iterable
from windows import Rect, WindowRect, GrabScreenRect, Crop
import compare_image
import numpy
import datetime
import PIL


def GameRegionRect(window: int) -> Rect:
    return GameRegionRect_(WindowRect(window))


def GameRegionRect_(windowRect: Rect) -> Rect:
    return Rect(
        windowRect.left + 14.0 / 800.0 * windowRect.width,
        windowRect.top + 181.0 / 600.0 * windowRect.height,
        windowRect.left + 603 / 800.0 * windowRect.width,
        windowRect.top + 566 / 600.0 * windowRect.height)


def GrabGameRegion(window: int) -> PIL.Image.Image:
    return GrabScreenRect(GameRegionRect(window))


def Backup(image: PIL.Image.Image):
    now = str(datetime.datetime.now())
    now = now.replace(" ", "_").replace(":", ";")
    image.save(f"{now}.png")


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


def GetGridsFromScreen(window: int):
    gameRegion = GrabGameRegion(window)
    # Backup(gameRegion)
    grids = SplitIntoGrids(gameRegion, 11, 19)
    return Categorize(grids)
