# Color-Based Tracking with OpenCV

## Overview
**"Color-Based tracking with OpenCV"** is a sophisticated Computer Vision project designed to track the tip of a glowing steel bar as it exits an oven. Utilizing the power of the OpenCV library, the system processes video frames to detect and track the glowing tip of the steel bar, even in the presence of occlusions. The choice of **color-based tracking**, rooted in the steel's distinctive glowing hue, ensures optimal accuracy and efficiency, making it a standout approach compared to other tracking methods.

Below is an output tracking video, generated using the `Input.mp4` video and the settings specified in `config_work_720p.yml`:

<div align="center">
  <img src="https://github.com/javier-marti-isasi/Color-tracking-with-OpenCV/assets/73080100/06c52477-f135-485a-b7fe-c7e594536232" alt="output_frame" width="400">
</div>



## Table of Contents
- [Objectives](#objectives)
- [Why Color-based Tracking?](#why-color-based-tracking)
- [Tracking Methodology](#tracking-methodology)
- [Directory Structure](#directory-structure)
- [Getting Started](#getting-started)
  - [Manual Installation](#manual-installation)
  - [Using Docker](#using-docker)
- [Configuring Tracking Parameters](#configuring-tracking-parameters)
- [Output Examples](#output-examples)
  - [Output Frame Example](#output-frame-example)
  - [Output Masked Frame Example](#output-masked-frame-example)
  - [Output Data Example](#output-data-example)
- [Potential Improvements & Future Work](#potential-improvements--future-work)
- [Contributing](#contributing)
- [License](#license)
  
## Objectives
- **Real-time Tracking**: Achieve seamless real-time processing of video frames, whether sourced from a live camera feed or a pre-recorded video.
- **Robust Detection**: Ensure consistent tracking of the glowing tip, even with challenges like noise, varying lighting or temporary occlusions.
- **High Configurability**: Empower users with the ability to fine-tune tracking parameters for diverse scenarios, user needs and optimal detection accuracy.

## Why Color-based Tracking?
In the realm of computer vision, there's a myriad of tracking methods available, from traditional algorithms implemented in OpenCV to deep learning giants like YOLO. However, when it comes to tracking the glowing tip of a steel bar, the color-based tracking method has proven to be unparalleled in its effectiveness.

Here's why:

1. **Distinctive Color Signature**: The glowing steel possesses a unique and consistent color signature that stands out, even amidst varying lighting conditions. This distinctiveness ensures that the steel tip is always identifiable, making color-based tracking exceptionally reliable.

2. **Simplicity & Efficiency**: Unlike complex algorithms that require extensive computations or deep learning models that demand hefty computational resources, color-based tracking is straightforward. It isolates the desired color range from the frame, making the process both intuitive and computationally light. This simplicity translates to real-time, lag-free tracking, crucial for applications demanding instant feedback.

3. **Robustness Across Scenarios**: While deep learning models like YOLO might be swayed by intricate backgrounds or require retraining for different scenarios, color-based tracking remains steadfast. The glowing steel's color remains a constant beacon, ensuring that the tracking remains robust even in diverse environments.

4. **Ease of Implementation**: Setting up and fine-tuning color-based tracking is a breeze compared to training deep learning models or calibrating other tracking algorithms. This ease of implementation means quicker deployment and adaptability to different use cases.

All things considered, while there's no one-size-fits-all in computer vision, for the specific task of tracking a glowing steel bar, color-based tracking isn't just a method; it's the optimal method. Its combination of reliability, efficiency, and simplicity makes it the gold standard for this application, proving that sometimes, the most straightforward solutions are also the most effective.

## Tracking Methodology
The process of tracking the glowing tip of the steel bar is executed in two primary steps:

1. **Color-based Tracking of the Steel Bar**

    The initial phase involves leveraging color-based tracking to identify and follow the glowing steel bar. To enhance the accuracy and efficiency of this method:

    - An area mask is applied to the image, effectively covering and excluding non-essential parts. This focused approach not only streamlines the tracking process but also minimizes potential distractions or false detections.

    - The masking is highly adaptable, allowing users to configure it based on different scenarios. This ensures that the system remains versatile to various real-life environments.

    To determine the optimal color range for detecting the glowing steel was utilized the `range_detector.py` script. This valuable tool can be located within the `range_detector/` directory.

2. **Calculating the Tip Point**

    Once the bar is effectively tracked, the next step is to pinpoint its tip.

    The definition of the extremity (edge) of the bar considered for point detection is primarily influenced by the specific scenario. Given that the bar consistently moves from right to left, the default setting is oriented towards this movement pattern.

    However, recognizing the diverse needs users might have, this parameter is made configurable. Users can easily adjust the edge of the bar to focus on via the `config_work.yml` files, ensuring that the system remains flexible and user-centric in its approach.

By combining these two steps, the system ensures precise, real-time tracking of the steel bar's glowing tip, adaptable to a range of scenarios and user preferences.

## Directory Structure

All the code files and folders follow the following structure:

```
Color-tracking-with-OpenCV/
│
├── range_detector/
│   ├── original_frame.png
│   └── range_detector.py
│
├── tracking_application/
│   │
│   ├── config_work/
│   │   ├── config_work_240p.yml
│   │   ├── config_work_360p.yml
│   │   └──... (other configurations)
│   │
│   ├── input/
│   │   └── Input.mp4
│   │
│   ├── output/
│   │   ├── data/
│   │   └── video/
│   │
│   ├── scripts/
│   │   ├── tracking_240p.sh
│   │   ├── tracking_360p.sh
│   │   └──... (other configurations)
│   │
│   └── src/
│       ├── utils/
│       │   ├── utils_config.py
│       │   ├── utils_data.py
│       │   └── ... (other utility modules)
│       └── main_track.py
│ 
├── docker-compose.yml
├── Dockerfile
├── LICENSE
├── README.md
└── requirements.txt
```

## Getting Started
### Manual Installation in Linux
1. Prerequisites:

    - Python 3.9+

2. Steps:

    - Clone the repository:
      
        ```
        git clone https://github.com/javier-marti-isasi/Color-tracking-with-OpenCV.git
        ```
        
    - Navigate to the project directory and install the required packages:
      
        ```
        cd Color-tracking-with-OpenCV
        pip install -r requirements.txt
        ```
        
    - Navigate to the scripts directory and execute a tracking script (you may need permissions, see next step):
      
        ```
        cd tracking_application/scripts
        ./tracking_240p.sh
        ./tracking_360p.sh
        ./tracking_480p.sh
        ./tracking_720p.sh
        ```
   - If needed, grant execute permissions to run the scripts:

        ```
        sudo chmod +x tracking_240p.sh
        sudo chmod +x tracking_360p.sh
        sudo chmod +x tracking_480p.sh
        sudo chmod +x tracking_720p.sh
        ```

### Using Docker
1. Prerequisites:
    - Docker

2. Steps:

   - Clone the repository:
     
        ```
        git clone https://github.com/javier-marti-isasi/Color-tracking-with-OpenCV.git
        ```
        
    - Navigate to the project directory, build the Docker image and run the application inside the Docker container:
      
        ```
        cd Color-tracking-with-OpenCV
        docker-compose up --build
        ```
        
    - Open a terminal inside the Docker container:
      
        ```
        docker exec -it tracking_container /bin/bash
        ```
        
    - Navigate to the scripts directory and execute a tracking script:
      
        ```
        cd scripts
        ./tracking_240p.sh
        ./tracking_360p.sh
        ./tracking_480p.sh
        ./tracking_720p.sh
        ```
        
    - (Optional) Copy output directory from the container to host in a new terminal:
      
        ```
        docker cp tracking_container:workspace/tracking_application/output/ ./
        ```

## Configuring Tracking Parameters
The system's behavior is governed by the `config_work.yml` files.

The provided configurations in the YAML file underscore the system's high adaptability to diverse user needs and scenarios. Users can tailor video output settings, fine-tune color-based tracking for different lighting conditions and choose between live camera feeds or pre-recorded videos. The system also offers flexibility in visualizing tracking points, adapting masks for various scenes and overlaying or saving tracking data.

This level of customization ensures that the system can be seamlessly integrated into a wide range of applications, from industrial monitoring to research experiments, catering to specific requirements with ease.

Here's a breakdown of the main configurations:

- **Video Output Configuration**:
Defines the resolution, frame rate, name and format of the output video. Also specifies if the video should be saved.

- **Color Configuration for Tracking Bar**:
Sets the color range in the HSV space to detect the glowing tip of the steel bar and the kernel size for Gaussian blur to reduce noise.

- **Live Camera and Video Display Settings**:
Determines the video source (live camera or video input) and whether to display the processed video and the applied mask in real-time.

- **Video Input Path**:
Specifies the path to the input video file when not using a live camera.

- **Tracking Point Configuration**:
Configures the visual properties of the detected tracking point, such as its color, border and size.

- **Point Detection Configuration**:
Indicates which edge of the bar to consider for point detection based on its movement direction.

- **Scene Configuration for Masking**:
Selects the scene configuration to adapt the mask for different video scenarios.

- **Video Data Settings**:
Defines settings for overlaying data, like frame numbers and detected point coordinates, on the video.

- **Tracking Data Settings**:
Determines if tracking data should be saved as a CSV file and specifies the naming conventions for the saved file.

## Output Examples

### Output Frame Example
Below is a frame from the output video, generated using the `Input.mp4` video and the settings specified in `config_work_720p.yml`:

<div align="center">
  <img src="https://github.com/javier-marti-isasi/Color-tracking-with-OpenCV/assets/73080100/31588bb5-b118-4cc1-b64c-f74c94959ea0" alt="output_frame" width="400">
</div>

Find the output videos in the `tracking_application/output/video` directory.

### Output Masked Frame Example
Below is a frame from the output video displaying the mask used for traking. It is generated using the `Input.mp4` video and the settings specified in `config_work_720p.yml` with `show_mask: True`:

<div align="center">
  <img src="https://github.com/javier-marti-isasi/Color-tracking-with-OpenCV/assets/73080100/ce5261dd-861b-4d40-9810-105ee1174c39" alt="output_frame" width="400">
</div>

### Output Data Example
Below are the tracking coordinates from the 30th frame through the 45th frame, derived from the `Input.mp4` video, using the settings specified in `config_work_720p.yml`:

<div align="center">
  <table>
    <thead>
      <tr>
        <th>frame_number</th>
        <th>x_coordinate</th>
        <th>y_coordinate</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td align="center">30</td>
        <td align="center">N/A</td>
        <td align="center">N/A</td>
      </tr>
      <tr>
        <td align="center">31</td>
        <td align="center">N/A</td>
        <td align="center">N/A</td>
      </tr>
      <tr>
        <td align="center">32</td>
        <td align="center">N/A</td>
        <td align="center">N/A</td>
      </tr>
      <tr>
        <td align="center">33</td>
        <td align="center">N/A</td>
        <td align="center">N/A</td>
      </tr>
      <tr>
        <td align="center">34</td>
        <td align="center">N/A</td>
        <td align="center">N/A</td>
      </tr>
      <tr>
        <td align="center">35</td>
        <td align="center">405</td>
        <td align="center">702</td>
      </tr>
      <tr>
        <td align="center">36</td>
        <td align="center">406</td>
        <td align="center">683</td>
      </tr>
      <tr>
        <td align="center">37</td>
        <td align="center">403</td>
        <td align="center">663</td>
      </tr>
      <tr>
        <td align="center">38</td>
        <td align="center">406</td>
        <td align="center">647</td>
      </tr>
      <tr>
        <td align="center">39</td>
        <td align="center">407</td>
        <td align="center">633</td>
      </tr>
      <tr>
        <td align="center">40</td>
        <td align="center">409</td>
        <td align="center">619</td>
      </tr>
      <tr>
        <td align="center">41</td>
        <td align="center">409</td>
        <td align="center">600</td>
      </tr>
      <tr>
        <td align="center">42</td>
        <td align="center">414</td>
        <td align="center">585</td>
      </tr>
      <tr>
        <td align="center">43</td>
        <td align="center">415</td>
        <td align="center">575</td>
      </tr>
      <tr>
        <td align="center">44</td>
        <td align="center">418</td>
        <td align="center">564</td>
      </tr>
      <tr>
        <td align="center">45</td>
        <td align="center">419</td>
        <td align="center">553</td>
      </tr>
      <tr>
        <td align="center">...</td>
        <td align="center">...</td>
        <td align="center">...</td>
      </tr>
    </tbody>
  </table>
</div>


Find all the output data in the `tracking_application/output/data` directory.


## Potential Improvements & Future Work
1. **Other Tracking Method Integrations**: Compare the solution with other tracking methods like traditional implementations in OpenCV or deep learning detection algorithms like YOLO.
2. **Performance Optimization**: Refine the code for real-time processing, especially for high-resolution or high frame rate videos.
3. **Adaptive Thresholding**: Implement dynamic thresholding to adjust to varying lighting conditions.
4. **User Interface Enhancements**: Develop an intuitive GUI for easy configuration and real-time tracking visualization.
5. **Processing Coordinate Output Data**: Tackle the possble inconsistencies in the input video, where identical consecutive frames may result in the same point detector, causing noticeable jumps between frames. For future enhancements, it's proposed to smooth out these abrupt transitions in the output tracking data, ensuring a more uniform and accurate representation.


## Contributing
I welcome contributions! Please fork the repository and create a pull request with your changes.

## License
This project is licensed under the Apache License 2.0. See the LICENSE file for details.
