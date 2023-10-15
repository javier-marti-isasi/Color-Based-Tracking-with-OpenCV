import logging
import sys
from utils import utils_config, utils_track


"""
This script serves as the main entry point for the video tracking application. It is responsible for:
- Setting up the logging configuration.
- Loading the tracking configurations from a provided YAML file.
- Initiating the video tracking process based on the loaded configurations.
"""

# Set up basic logging configuration
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


def main():
    """
    Main function to execute the video tracking process.
    Loads configurations from a YAML file and initiates the tracking.

    Usage:
        python main_track.py <path-to-yaml-config-file>
    """
    # Ensure the correct number of arguments are provided
    if len(sys.argv) != 2:
        logging.error("Incorrect number of arguments.")
        logging.info("Usage: python main_track.py <path-to-yaml-config-file>")
        return 1

    try:
        # Load the configuration of the tracking
        config = utils_config.load_config_from_files()

        # Track
        utils_track.track(config)

    except FileNotFoundError:
        logging.error("Config file not found. Please provide a valid path.")
        return 1
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
