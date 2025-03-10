# Image Folder to Movie Generator

![Screenshot](https://files.catbox.moe/mkeo48.JPG)

## Description

A Python script that converts a folder of images into a video, with options for customizing the duration of each image, the number of loops, and whether images should be shuffled per loop. The script utilizes MoviePy for video generation and PySimpleGUI for user interaction.

## Table of Contents

1. [Features](#features)
2. [Installation and Usage](#installation-and-usage)
3. [Using the Application](#using-the-application)
4. [Requirements](#requirements-package_managerpy-should-handle-this-for-you)
5. [Contributing](#contributing)
6. [License](#license)

## Features

- **Customizable Duration**: Set the display duration of each image in seconds.
- **Loops**: Specify the number of times the video should loop.
- **Shuffle**: Randomize the order of images in each loop.
- **Aspect Ratio Maintenance**: Resizes images to maintain aspect ratio while fitting them to an average dimension.
- **Bordered Images**: Creates bordered images if necessary to match the average dimensions.

---

## Installation and Usage
- For Windows users, you can simply run the `start.bat` file to start the application, at the first run it will install the required dependencies on a venv (isolated environment) and then ask you to press any key to continue before starting the application.
- For Linux and macOS users, be sure to make the script executable before running:
```bash
chmod +x install.sh
chmod +x start.sh
```

- Then you can run the `start.sh` script to install dependencies and start the application.

## Using the Application

1. **Select Your Image Folder**: Choose the folder that contains the images you want to turn into a video.

2. **Set Your Preferences**:
   - **Duration**: Decide how long each image should be displayed.
   - **Loops**: Specify how many times the video should repeat.
   - **Shuffle**: Choose whether to randomize the image order in each loop.

3. **Generate Your Video**: Click the "Generate Video" button.

4. **Save Your Video**:
   - Choose where you want to save the video file.
   - Give your video a name (or use the default name based on the folder name).

That's it! Your images are now a video.

---

## Requirements (package_manager.py should handle this for you)

- Python 3.x
- MoviePy
- PySimpleGUI (version 4.60.4 recommended as 5.x is paid)
- Pillow (PIL)
- ffmpeg (required by MoviePy)

## Contributing
- Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.