from typing import NamedTuple
from typing import Optional

import cProfile

import numpy as np

import PIL.ImageGrab

import win32api
import win32gui
import win32con

import pyautogui


def SetDpiAwareness() -> bool:
    import ctypes
    errorCode = ctypes.windll.shcore.SetProcessDpiAwareness(2)
    return errorCode == 0


def FindWindow(title: str) -> Optional[int]:
    handle = win32gui.FindWindow(win32con.NULL, title)
    return None if handle == 0 else handle


class Rect(NamedTuple):
    left: int
    top: int
    right: int
    bottom: int

    @property
    def width(self) -> int:
        return self.right-self.left

    @property
    def height(self) -> int:
        return self.bottom-self.top


def WindowRect(window: int) -> Rect:
    return Rect(*win32gui.GetWindowRect(window))


def GrabScreen(left: int, top: int, right: int, bottom: int) -> PIL.Image.Image:
    return PIL.ImageGrab.grab((left, top, right, bottom))


def GrabScreenRect(rect: Rect) -> PIL.Image.Image:
    return GrabScreen(rect.left, rect.top, rect.right, rect.bottom)


def GrabWindow(window) -> PIL.Image.Image:
    return GrabScreenRect(WindowRect(window))


def Crop(image: PIL.Image, rect: Rect) -> PIL.Image.Image:
    return image.crop((rect.left, rect.top, rect.right, rect.bottom))


def Resize(image: PIL.Image.Image, width: int, height: int) -> PIL.Image.Image:
    return image.resize((width, height))


def PositionToScreen(position: np.array, gameRect: Rect, rows: int, cols: int):
    gridWidth, gridHeight = gameRect.width/cols, gameRect.height/rows
    col, row = position
    x = gameRect.left + (col + 0.5) * gridWidth
    y = gameRect.top + (row + 0.5) * gridHeight
    return x, y


def Click(screenPosition: np.array):
    pyautogui.moveTo(screenPosition)
    pyautogui.click()


def Profile(func):
    profile=cProfile.Profile()
    profile.enable()

    func()

    profile.disable()
    profile.print_stats()
