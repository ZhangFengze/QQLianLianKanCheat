from windows import Rect, WindowRect


def GameRegionRect(window: int) -> Rect:
    return GameRegionRect_(WindowRect(window))


def GameRegionRect_(windowRect: Rect) -> Rect:
    return Rect(
        windowRect.left + 14.0 / 800.0 * windowRect.width,
        windowRect.top + 181.0 / 600.0 * windowRect.height,
        windowRect.left + 603 / 800.0 * windowRect.width,
        windowRect.top + 566 / 600.0 * windowRect.height)