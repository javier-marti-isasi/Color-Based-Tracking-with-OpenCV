import cv2

"""
Utility functions to work with video.
"""


def display_frame(frame):
    """
    Display the processed frame.
    """
    cv2.imshow("Frame", frame)
