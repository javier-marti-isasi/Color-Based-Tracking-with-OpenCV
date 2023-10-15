"""
This module provides functions to modify masks based on specific scenes or conditions.
The primary function, `modify_mask`, determines the scene and applies the appropriate mask modification.
"""


def modify_mask(mask, scene):
    """
    Modify the mask based on specific conditions.
    """
    if scene == "glowing_bar_01":
        return modify_mask_glowing_bar_scene_01(mask)
    elif scene == "glowing_bar_02":
        return modify_mask_glowing_bar_scene_02(mask)
    else:
        return mask


def modify_mask_glowing_bar_scene_01(mask):
    """
    Modify the mask based on specific scene of the glowing bar coming out of the oven.
    WARNING! THIS FUNCTION MASKS THE INPUT BASED ON THE REGION OF THIS PARTICULAR SCENE
    FOR DIFFERENT SCENE, CREATE A NEW FUNCTION
    """
    # Constants used for mask modification to cover areas of non-interest
    mask_value = 150
    mask_ratio = 0.9
    mask_offset = 0.03

    rows, columns = mask.shape
    for row in range(rows):
        for column in range(columns):
            if row / rows > column / columns * mask_ratio - mask_offset:
                mask[row, column] = mask_value

    return mask


def modify_mask_glowing_bar_scene_02(mask):
    """
    Modify the mask based on specific scene of the glowing bar coming out of the oven.
    WARNING! THIS FUNCTION MASKS THE INPUT BASED ON THE REGION OF THIS PARTICULAR SCENE
    FOR DIFFERENT SCENE, CREATE A NEW FUNCTION
    """
    # Constants used for mask modification to cover areas of non-interest
    mask_value = 150
    mask_ratio = 3.5
    mask_offset = 1

    rows, columns = mask.shape
    for row in range(rows):
        for column in range(columns):
            if row / rows < column / columns * mask_ratio - mask_offset:
                mask[row, column] = mask_value

    return mask
