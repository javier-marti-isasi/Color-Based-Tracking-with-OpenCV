import cv2
import imutils
import logging
from imutils.video import VideoStream
import time
import os
from . import utils_config, utils_video, utils_point_track, utils_mask, utils_data

"""
This module provides functionalities to track specific points in a video stream based on the provided configurations.
The main class, `RunTrack`, handles the video tracking process, including setting up the video stream, processing each frame,
detecting the point of interest, and saving or displaying the results.
"""


class RunTrack:
    """
    Class to handle video tracking based on provided configurations.
    """

    def __init__(self, config: utils_config.Config):
        """
        Initialize the tracker with the given configuration.
        """
        self._extract_config_values(config)

    def _extract_config_values(self, config):
        """
        Extract configuration values and set them as instance attributes.
        """
        attributes = [
            "use_livecam", "video_input_path", "output_width", "output_height", "lower_color",
            "upper_color", "blur_ksize", "save_video", "show_video", "point_color",
            "point_border_color", "point_radius", "point_border_thickness", "show_mask",
            "output_format", "output_fps", "location_most", "scene", "show_frame_number",
            "show_coordinates", "save_data", "text_color", "output_directory", "output_name",
            "data_file_name"
        ]
        for attr in attributes:
            setattr(self, attr, config.get(attr))

    def _get_fourcc(self):
        """
        Get the FourCC code for the specified video format.
        """
        format_to_fourcc = {
            "avi": "XVID",
            "mp4": "MP4V",
            "mov": "MJPG"
            # add more format-to-FourCC mappings as needed
        }
        return cv2.VideoWriter_fourcc(*str(format_to_fourcc.get(self.output_format.lower(), "XVID")))

    def _setup_video_stream(self):
        """
        Set up the video stream based on the configuration.
        """
        if not self.use_livecam:
            self.video_source_type = "video_file"
            return cv2.VideoCapture(self.video_input_path)
        else:
            logging.info("Live camera turning on...")
            logging.info("TO STOP LIVE CAMERA, PRESS 'q'.")
            self.video_source_type = "webcam"
            return VideoStream(src=0).start()

    def _setup_video_writer(self):
        """
        Set up the video writer based on the configuration.
        """
        fourcc = self._get_fourcc()
        return cv2.VideoWriter(os.path.join(self.output_directory, 'video', f'{self.output_name}.{self.output_format}'),
                               fourcc, self.output_fps, (self.output_width, self.output_height))

    def _get_frame(self, vs):
        """
        Retrieve a frame from the video source.
        """
        frame = vs.read()
        return frame[1] if not self.use_livecam else frame

    def _process_frame(self, frame, frame_number):
        """
        Process the frame and apply the necessary transformations.
        """
        frame = imutils.resize(frame, width=self.output_width)
        blurred = cv2.GaussianBlur(frame, self.blur_ksize, sigmaX=0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, tuple(self.lower_color), tuple(self.upper_color))
        mask = utils_mask.modify_mask(mask, self.scene)

        point = utils_point_track.detect_point(mask, self.location_most)
        img_to_show = mask if self.show_mask else frame

        if point:
            self._draw_point(img_to_show, point)
            if self.show_coordinates:
                self._display_coordinates(img_to_show, point)

        if self.save_data:
            utils_data.save_coordinates(frame_number, point, self.output_directory, self.data_file_name)
        return img_to_show

    def _draw_point(self, img, point):
        """
        Draw the detected point on the image.
        """
        cv2.circle(img, point, self.point_radius, self.point_border_color, self.point_border_thickness)
        cv2.circle(img, point, self.point_radius - self.point_border_thickness, self.point_color, -1)

    def _display_coordinates(self, img, point):
        """
        Display the point's coordinates
        """
        x_coord_text = "X coordinate: {}".format(point[0])
        y_coord_text = "Y coordinate: {}".format(point[1])
        cv2.putText(img, x_coord_text, (self.output_width - 210, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, self.text_color, 2)
        cv2.putText(img, y_coord_text, (self.output_width - 210, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, self.text_color, 2)

    def _display_frame_number(self, img, frame_number):
        """
        Display frame number
        """
        fps_text = "Frame number: {}".format(frame_number)
        cv2.putText(img, fps_text, (self.output_width - 210, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, self.text_color, 2)

    def run(self):
        """
        Start the tracking process.
        """
        vs = self._setup_video_stream()
        if self.video_source_type == "video_file" and not vs.isOpened():
            logging.error("Error: Couldn't open video source.")
            return

        time.sleep(2.0)  # Allow the camera or video file to warm up

        # Initialize the writer with the first frame to get correct dimensions
        frame = self._get_frame(vs)
        out = self._setup_video_writer() if self.save_video else None

        # Clear the .csv file before starting the tracking and write the headers
        if self.save_data:
            with open(os.path.join(self.output_directory, 'data', f'{self.data_file_name}.csv'), "w") as file:
                file.write("frame_number,x_coordinate,y_coordinate\n")

        frame_number = 0
        while True:
            if frame is None:
                break

            frame_number += 1
            img_to_show = self._process_frame(frame, frame_number)

            if self.show_frame_number:
                self._display_frame_number(img_to_show, frame_number)

            if self.save_video and out:
                out.write(img_to_show)
            if self.show_video:
                utils_video.display_frame(img_to_show)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

            frame = self._get_frame(vs)

        if self.video_source_type == "webcam":
            vs.stop()
        else:
            vs.release()

        if out:
            out.release()
        cv2.destroyAllWindows()


def track(config: utils_config.Config):
    """
    Utility function to initiate the tracking process.
    """
    tracker = RunTrack(config)
    tracker.run()
