"""
Utility functions to work with strings.
"""


def as_str_or_none(parameter_value: str) -> str or None:
    """
    Convert a value to lowercase string or None.
    """
    if not parameter_value or parameter_value.lower() == "none":
        return None
    return str(parameter_value)
