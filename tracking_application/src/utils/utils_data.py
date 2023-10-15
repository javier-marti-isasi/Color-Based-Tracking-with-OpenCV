import os

"""
Utility functions to work with data.
"""


def save_coordinates(frame_number: int, point: tuple, output_directory: str, data_file_name: str) -> None:
    """
    Save the point's coordinates to a .csv file.
    """
    with open(os.path.join(output_directory, 'data', f'{data_file_name}.csv'), "a") as file:
        if point is None:
            file.write(f"{frame_number},N/A,N/A\n")
        else:
            file.write(f"{frame_number},{point[0]},{point[1]}\n")
