# Hailo RPi5 Basic Pipelines
This repository contains examples of basic pipelines using Hailo's H8 and H8L accelerators. The examples demonstrate object detection, human pose estimation, instance segmentation, and face recognition, providing a solid foundation for your own projects.
This repo is using our [Hailo Apps Infra](https://github.com/hailo-ai/hailo-apps-infra) repo as a dependency.
See our Development Guide for more information on how to use the pipelines to create your own custom pipelines.

## Installation
See the [Installation Guide](../README.md#installation) in the main README for detailed instructions on setting up your environment.

# Development Guide

This guide provides an overview of how to develop custom applications using the basic pipelines provided in this repository. The examples demonstrate object detection, human pose estimation, instance segmentation, and face recognition using Hailo's H8 and H8L accelerators.

## Understanding the Callback Method

Each example in this repository uses a callback method to process the data from the GStreamer pipeline. The callback method is defined as a function that is called whenever data is available from the pipeline. This function processes the data, extracts relevant information, and performs any necessary actions, such as drawing on a frame or printing information to the terminal.

### User App Callback Class

The `user_app_callback_class` is a custom class that inherits from the `app_callback_class` provided by the `hailo_apps_infra` package. This class is used to manage user-specific data and state across multiple frames. It typically includes methods to increment frame counts, manage frame data, and handle any additional user-specific logic.

### Note on Callback Function

The callback function is blocking and cannot take too long to execute; otherwise, the pipeline will get stuck. If you need a long processing time per frame, send the data to another process. For example, see the `WLEDDisplay` class in the `community_projects/wled_display/wled_display.py` file and the callbacks using it, such as in `community_projects/wled_display/wled_pose_estimation.py`. The `WLEDDisplay` class runs its own process, which gets data from the application callback and processes it in the background, allowing the pipeline to continue.

## Available Pipelines

The basic pipelines examples use the

hailo-apps-infra

 package, which provides common utilities and the actual pipelines. You can import and use these pipelines in your applications. Below are some of the available pipelines:


# Detection Example
![Banner](images/detection.gif)

This example demonstrates object detection using the YOLOv8s model for Hailo-8L (13 TOPS) and the YOLOv8m model for Hailo-8 (26 TOPS) by default. It also supports all models compiled with HailoRT NMS post process. Hailo's Non-Maximum Suppression (NMS) layer is integrated into the HEF file, allowing any detection network compiled with NMS to function with the same post process.
All "persons" are tracked.

## What’s in This Example:

### Custom Callback Class
An example of a custom callback class that sends user-defined data to the callback function. Inherits from `app_callback_class` and can be extended with custom variables and functions. This example adds a variable and a function used when the `--use-frame` flag is active, displaying these values on the user frame.

### Application Callback Function
Demonstrates parsing `HAILO_DETECTION` metadata. Each GStreamer buffer contains a `HAILO_ROI` object, serving as the root for all Hailo metadata attached to the buffer. The function extracts the label, bounding box, confidence and tracking ID for each 'Person' detection. It counts and prints the number of persons detected. With the `--use-frame` flag, it also displays the frame with the number of detected persons and user-defined data.Most detection networks

### Additional Features
Shows how to add more command-line options using the `argparse` library. For instance, the added flag in this example allows changing the model used.

### Using Retrained Models
Supports using retrained detection models compiled with HailoRT NMS Post Process (`HailortPP`). Load a custom model’s HEF using the `--hef-path` flag. Default labels are COCO labels ([80 classes](https://github.com/hailo-ai/tappas/blob/4341aa360b7f8b9eac9b2d3b26f79fca562b34e4/core/hailo/libs/postprocesses/common/labels/coco_eighty.hpp)). For custom models with different labels, use the `--labels-path` flag to load your labels file (e.g., `resources/barcode-labels.json`).

The `download_resources.sh` script downloads the network trained in the [Retraining Example](retraining-example.md#using-yolov8-retraining-docker), which can be used as a reference.

To download all models , You should use the `--all` with the ./download_resources.sh

**Example:**These scripts are importing the application code from the 'pipelines' scripts.

**Example Output:**
![Barcode Detection Example](images/barcode-example.png)

# Pose Estimation Example
![Banner](images/pose_estimation.gif)

This example demonstrates human pose estimation using the `yolov8s_pose` model for Hailo-8l (13 TOPS) and the `yolov8m_pose` model for Hailo-8 (26 TOPS).

## What’s in This Example:

### Pose Estimation Callback Class
The callback function retrieves pose estimation metadata from the network output. Each person is represented as a `HAILO_DETECTION` with 17 keypoints (`HAILO_LANDMARKS` objects). The function parses the landmarks to extract the left and right eye coordinates, printing them to the terminal. If the `--use-frame` flag is set, the eyes are drawn on the user frame. Obtain the keypoints dictionary using the `get_keypoints` function.

### Keypoints Dictionary
The `get_keypoints` function provides a dictionary mapping keypoint names to their corresponding indices. This dictionary includes keypoints for the nose, eyes, ears, shoulders, elbows, wrists, hips, knees, and ankles.

### Frame Processing
If the `--use-frame` flag is set, the callback function retrieves the video frame from the buffer and processes it to draw the detected keypoints (left and right eyes) on the frame. The processed frame is then displayed.

## What’s in This Example:

### Instance Segmentation Callback Class
The callback function processes instance segmentation metadata from the network output. Each instance is represented as a `HAILO_DETECTION` with a mask (`HAILO_CONF_CLASS_MASK` object). The function parses, resizes, and reshapes the masks according to the frame coordinates, and overlays the masks on the frame if the `--use-frame` flag is set. The function also prints the detection details, including the track ID, label, and confidence, to the terminal.

### Key Features
- **Frame Skipping**: Processes every 2nd frame to reduce computational load.
- **Color Coding**: Uses predefined colors to differentiate between tracked instances.
- **Mask Overlay**: Resizes and overlays the segmentation masks on the frame.
- **Boundary Handling**: Ensures the ROI dimensions are within the frame boundaries and handles negative values.

# Face Recognition Example
![Banner](images/face_recogntion.gif)

This example demonstrates face recognition using the `scrfd_2.5g` and `arcface_mobilenet` modes for Hailo-8l (13 TOPS) and the `scrfd_10g` and `arcface_mobilenet`models for Hailo-8 (26 TOPS).

## What’s in This Example:

### Face Recognition Callback Class
The callback function retrieves face recognition metadata from the network output. Each face is represented as a `HAILO_DETECTION` and every recognized face is represented as `HAILO_CLASSIFICATION`. 

### Running Few Models
This example demonstraite a usage of 2 models, using Hailo cropper element.
The first model run face detection, then using hailo cropper we run face recognition for each cropped face.


## Development Recommendations

- **Start Simple**: If you're new to the pipeline, begin with the basic scripts to familiarize yourself with the workflow.
- **Minimal Setup**: Simply run the script and focus on editing the callback function to customize how the output is processed.
- **Customize Callbacks**: Modify the `app_callback` function within each script to handle the pipeline output according to your specific requirements.
- **Incremental Complexity**: Gradually move to more complex pipelines as you gain confidence and require more advanced features.
- **Leverage Documentation**: Refer to the [TAPPAS Documentation](https://github.com/hailo-ai/tappas/blob/4341aa360b7f8b9eac9b2d3b26f79fca562b34e4/docs/TAPPAS_architecture.rst) and [Hailo Objects API](https://github.com/hailo-ai/tappas/blob/4341aa360b7f8b9eac9b2d3b26f79fca562b34e4/docs/write_your_own_application/hailo-objects-api.rst#L4) for deeper insights and advanced customization options.
- **Hailo Apps Infra Package** - The pipelines used in the basic pipelines examples are using the hailo-app-infra package. This package provides common utilities and the actual pipelines. For more information see [Hailo apps infra Repo](https://github.com/hailo-ai/hailo-apps-infra/blob/master/doc/development_guide.md).

By following this guide, makers can efficiently utilize the `basic_pipelines` package to build and customize their computer vision applications without getting overwhelmed by complexity.

### Debugging Tips
#### Print Statements
The simplest tool for debugging is to use the `print` function. You can print the data you are interested in, such as the frame number, the number of detected objects, or the detected objects' coordinates. This can help you understand the data flow and identify any issues.
#### ipdb Debugger
The `ipdb` debugger is a powerful tool for debugging Python code. You can insert breakpoints in your code and inspect variables, step through the code, and evaluate expressions. To use `ipdb`, add the following line to your code where you want to set a breakpoint:
    ```python
    import ipdb; ipdb.set_trace()
    ```
```python
import ipdb; ipdb.set_trace()
```
When the code reaches this line, it will pause execution, and you can interact with the debugger. You can then step through the code, inspect variables, and evaluate expressions to identify issues. This tool is useful for discovering available options and methods for a given object or variable. Due to `ipdb` auto-complete feature, you can type the object name and press `Tab` to see the available options and methods.

Note that you need to install the `ipdb` package to use this debugger. You can install it using the following command:
```bash
pip install ipdb
```
#### Choppy Video Playback

If you experience choppy video playback, it might be caused due to too long processing time in the callback function or in another place in the pipeline.
In the callback function, ensure that the processing time is minimal to avoid blocking the pipeline. If you need to perform heavy processing, consider sending the data to another process for processing in the background.
Run the `htop` command in a terminal to monitor the CPU and memory usage.
If the CPU usage is close to 100%, it might be the bottleneck.

The bottleneck could also be the model running on Hailo.
In this case, consider using a smaller model or using larger batch size.

#### Hailo monitor
To run the Hailo monitor, run the following command in a different terminal:
```bash
hailortcli monitor
```
In the terminal you run your code set the `HAILO_MONITOR` environment variable to `1` to enable the monitor.
```bash
export HAILO_MONITOR=1
```
#### Pipeline debugging
See Hailo Apps Infra Developer Guide for more information on how to debug the pipeline.


# Scripts Overview

### Environment Configuration  (Required for Each New Terminal Session)
Ensure your environment is set up correctly by sourcing the provided script. This script sets the required environment variables and activates the Hailo virtual environment. If the virtual environment does not exist, it will be created automatically.
```bash
source setup_env.sh
```

### Requirements Installation
Within the activated virtual environment, install the necessary Python packages:
```bash
pip install -r requirements.txt
```

**Note:** The `rapidjson-dev` package is typically installed by default on Raspberry Pi OS. If it's missing, install it using:
```bash
sudo apt install -y rapidjson-dev
```

### Resources Download
Download the required resources by running:
```bash
./download_resources.sh
```
To download all models , You should use the `--all` with the ./download_resources.sh
