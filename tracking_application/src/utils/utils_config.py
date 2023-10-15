import sys
import yaml
import logging
from . import utils_paths, utils_strings

"""
This script provides a structured way to handle configurations for the video tracking application.
Configurations are read from a YAML file and are used to define various parameters like video output settings,
color thresholds for tracking, and more.
"""


class Config:
    """
    Handles configurations for video tracking settings.
    This class reads configurations from a YAML file and provides methods to retrieve specific configuration values.

    Basic Usage:
        config = Config("path_to_yaml")
        value = config.get(<parameter_name>)
    """
    # Define output directory
    OUTPUT_DIRECTORY = "../output"

    # Define supported output formats for clarity
    OUTPUT_FORMATS = {"mp4", "avi", "mov"}

    # Define configured scenes
    CONFIGURED_SCENES = {"glowing_bar_01", "glowing_bar_02"}

    # Define configured values for location_most
    LOCATIONS_MOST = {"left", "right", "top", "bottom"}

    # Define necessary parameters
    EXPECTED_PARAMETERS = ["output_width", "output_height", "lower_color", "upper_color",
                           "point_color", "point_border_color", "point_radius",
                           "point_border_thickness", "blur_ksize", "output_fps",
                           "use_livecam", "save_video", "show_video", "show_mask",
                           "video_input_path", "output_format", "location_most", "scene",
                           "show_frame_number", "show_coordinates", "save_data",
                           "text_color", "output_name", "data_file_name"]

    def __init__(self, config_file_path: str):
        """
        Initialize the configuration from the provided file path.
        """
        self.config_file = config_file_path
        self._arguments_dict = {}

        # Categorize configuration parameters by their expected data type for ease of validation and parsing.
        self._path_keywords = ["video_input_path"]
        self._int_keywords = ["output_width", "output_height", "lower_color", "upper_color",
                              "point_color", "point_border_color", "point_radius",
                              "point_border_thickness", "blur_ksize", "output_fps",
                              "text_color"]
        self._bool_keywords = ["use_livecam", "save_video", "show_video", "show_mask",
                               "show_frame_number", "show_coordinates", "save_data"]
        self._str_keywords = ["output_format", "location_most", "scene", "output_name",
                              "data_file_name"]

        # Load configurations on instantiation.
        self.load()

    def _load_yaml_arguments(self):
        """
        Load configurations from the provided YAML file.
        """
        with open(self.config_file, 'r') as file:
            yaml_arguments = yaml.safe_load(file)

        for parameter_name, parameter_value in yaml_arguments.items():
            self.set(parameter_name, parameter_value)

        self._check_constraints()

    def load(self):
        """
        Public method to load configurations.
        """
        self._load_yaml_arguments()
        self._arguments_dict["output_directory"] = self.OUTPUT_DIRECTORY

    def _check_constraints(self):
        """
        Enforce specific constraints on the configuration parameters.
        """
        self._check_all_parameters_present()
        self._check_livecam_constraints()
        if not self._arguments_dict.get("use_livecam"):
            self._check_output_format()
            self._check_scenes()
        self._check_livecam_inside_docker()
        self._check_show_video_inside_docker()
        self._check_location_most()

    def _check_all_parameters_present(self):
        """
        Ensure that all expected parameters are set in the configuration.
        """
        missing_parameters = [param for param in self.EXPECTED_PARAMETERS if param not in self._arguments_dict]

        if missing_parameters:
            raise ValueError(f"Missing parameters in the configuration: {', '.join(missing_parameters)}")

    def _check_output_format(self):
        """
        Validate the output format against the supported formats.
        If the specified format is not supported, default to 'mp4'.
        """
        if self._arguments_dict.get("output_format") not in self.OUTPUT_FORMATS:
            logging.warning(
                f"Output format {self._arguments_dict.get('output_format')} is not supported. Defaulting to 'mp4'.")
            self._arguments_dict["output_format"] = "mp4"

    def _check_scenes(self):
        """
        Validate the camera scene against the configured scenes.
        If the specified scene is not configured, set to None.
        """
        if self._arguments_dict.get("scene") not in self.CONFIGURED_SCENES:
            logging.warning(f"Scene {self._arguments_dict.get('scene')} is not configured.")
            logging.warning("The mask will not be modified based on the specific scene.")
            self._arguments_dict["scene"] = None

    def _check_location_most(self):
        """
        Validate the location_most against the configuration.
        The location_most defines the extremity (edge) of the bar to consider in the image for the point detection.
        If the location_most is not configured, default to 'left'.
        """
        if self._arguments_dict.get("location_most") not in self.LOCATIONS_MOST:
            logging.warning(
                f"Location most {self._arguments_dict.get('location_most')} is not configured. Defaulting location most to 'left'.")
            self._arguments_dict["location_most"] = "left"

    def _check_livecam_inside_docker(self):
        """
        Check if the application is running inside a Docker container and if the live camera is being used.
        If so, disable the live camera as it's not supported inside Docker.
        """
        if utils_paths.is_inside_docker() and self._arguments_dict.get("use_livecam"):
            logging.warning("Live camera feed is not supported inside a Docker container. Disabling 'use_livecam'.")
            self._arguments_dict["use_livecam"] = False

    def _check_show_video_inside_docker(self):
        """
        Check if the application is running inside a Docker container and if video display is enabled.
        If so, disable the video display as it's not supported inside Docker.
        """
        if utils_paths.is_inside_docker() and self._arguments_dict.get("show_video"):
            logging.warning("Displaying video is not supported inside a Docker container. Disabling 'show_video'.")
            self._arguments_dict["show_video"] = False

    def _check_livecam_constraints(self):
        """
        Check constraints related to the use of a live camera.
        """
        if self._arguments_dict.get("use_livecam") and self._arguments_dict.get("save_video"):
            logging.warning("Saving video is not supported when 'use_livecam' is set to True. Disabling 'save_video'.")
            self._arguments_dict["save_video"] = False

    def set(self, parameter_name: str, parameter_value=None):
        """
        Set a specific configuration parameter.
        """
        parameter_value = self._fix_type_and_value_of_non_dict_param(parameter_name, parameter_value)
        self._arguments_dict[parameter_name] = parameter_value

    def _fix_type_and_value_of_non_dict_param(self, parameter_name, parameter_value):
        """
        Convert and validate the type of configuration parameters.
        This method ensures that each parameter is of the correct type and format.
        """
        # Dict
        if isinstance(parameter_value, dict):
            logging.error("Specified parameter {} cannot be dict in _fix_type_and_value_of_non_dict_param.".format(
                parameter_name)
            )
            raise ValueError

        # Path
        if parameter_name in self._path_keywords:
            if (parameter_value == "") or (parameter_value is None):
                return None
            assert utils_paths.path_exists(parameter_value), \
                f"{parameter_value} path does not exist."
            return str(parameter_value)

        # Int, or list of int
        if parameter_name in self._int_keywords:
            if isinstance(parameter_value, list):
                return [int(v) for v in parameter_value]
            else:
                return int(parameter_value)

        # Str or list of str
        if parameter_name in self._str_keywords:
            if isinstance(parameter_value, list):
                return [utils_strings.as_str_or_none(v) for v in parameter_value]
            else:
                return utils_strings.as_str_or_none(parameter_value)
        return parameter_value

    def get(self, argument_name: str):
        """
        Retrieve the value of a specific configuration parameter.
        """
        return self._arguments_dict.get(argument_name)


def load_config_from_files() -> Config:
    """
    Load configurations from a file provided as a command line argument.
    """
    if len(sys.argv) != 2:
        raise ValueError("Usage: python main_track.py <config_file>")

    config_file_path = sys.argv[1]
    return Config(config_file_path)
