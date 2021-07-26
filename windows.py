from typing import Tuple
from typing import NamedTuple
from typing import Optional

import numpy as np

import win32gui
import win32con
import win32process

import pyautogui


def FindWindow(title: str) -> Optional[int]:
    handle = win32gui.FindWindow(win32con.NULL, title)
    return None if handle == 0 else handle


def GetWindowThreadProcessId(window: int) -> Tuple[int, int]:
    return win32process.GetWindowThreadProcessId(window)


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


def PositionToScreen(position: np.array, gameRect: Rect, rows: int, cols: int):
    gridWidth, gridHeight = gameRect.width/cols, gameRect.height/rows
    col, row = position
    x = gameRect.left + (col + 0.5) * gridWidth
    y = gameRect.top + (row + 0.5) * gridHeight
    return x, y


def Click(screenPosition: np.array):
    pyautogui.moveTo(screenPosition)
    pyautogui.click()