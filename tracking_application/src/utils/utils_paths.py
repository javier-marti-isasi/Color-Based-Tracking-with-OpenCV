import os

"""
Utility functions for path checks.
"""


def path_exists(path) -> bool:
    """
    Check if the specified path exists in the file system.
    """
    return os.path.exists(path)


def is_inside_docker() -> bool:
    """
    Check if the application is running inside a Docker container.
    """
    return os.path.exists('/.dockerenv')
