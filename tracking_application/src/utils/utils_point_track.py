import numpy as np

"""
Utility functions to detect the point of interest.
"""


def detect_point(mask: np.ndarray, location_most: str) -> tuple or None:
    """
    Detect the point of interest in the mask based on the specified location.
    """
    if location_most == "left":
        return detect_leftmost_point(mask)
    elif location_most == "right":
        return detect_rightmost_point(mask)
    elif location_most == "top":
        return detect_topmost_point(mask)
    elif location_most == "bottom":
        return detect_bottommost_point(mask)
    else:
        return None


def detect_leftmost_point(mask: np.ndarray) -> tuple or None:
    """
    Detect the leftmost point in the mask with a value of 255.
    """
    if mask.max() == 255:
        points = np.argwhere(mask == 255)
        leftmost_point = points[np.argmin(points[:, 1])]
        return tuple(leftmost_point[::-1])
    return None


def detect_rightmost_point(mask: np.ndarray) -> tuple or None:
    """
    Detect the rightmost point in the mask with a value of 255.
    """
    if mask.max() == 255:
        points = np.argwhere(mask == 255)
        rightmost_point = points[np.argmax(points[:, 1])]
        return tuple(rightmost_point[::-1])
    return None


def detect_topmost_point(mask: np.ndarray) -> tuple or None:
    """
    Detect the topmost point in the mask with a value of 255.
    """
    if mask.max() == 255:
        points = np.argwhere(mask == 255)
        topmost_point = points[np.argmin(points[:, 0])]
        return tuple(topmost_point[::-1])
    return None


def detect_bottommost_point(mask: np.ndarray) -> tuple or None:
    """
    Detect the bottommost point in the mask with a value of 255.
    """
    if mask.max() == 255:
        points = np.argwhere(mask == 255)
        bottommost_point = points[np.argmax(points[:, 0])]
        return tuple(bottommost_point[::-1])
    return None
