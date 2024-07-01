# Image Folder to Movie Generator

## Description

A Python script that converts a folder of images into a video, with options for customizing the duration of each image, the number of loops, and whether images should be shuffled per loop. The script utilizes MoviePy for video generation and PySimpleGUI for user interaction.

## Features

- **Customizable Duration**: Set the display duration of each image in seconds.
- **Loops**: Specify the number of times the video should loop.
- **Shuffle**: Randomize the order of images in each loop.
- **Aspect Ratio Maintenance**: Resizes images to maintain aspect ratio while fitting them to an average dimension.
- **Bordered Images**: Creates bordered images if necessary to match the average dimensions.

## Usage

1. Run the script.
2. Select the folder containing the images.
3. Customize the duration, number of loops, and shuffle option.
4. Choose a save location and name for the output video.

## Requirements

- Python 3.x
- MoviePy
- PySimpleGUI (version 4.60.4 recommended)
- Pillow (PIL)

## Installation

To install the required dependencies, run:

```bash
pip install moviepy pillow
pip install PySimpleGUI==4.60.4
```