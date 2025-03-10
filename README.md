# Image Folder to Movie Generator

## Description

A Python script that converts a folder of images into a video, with options for customizing the duration of each image, the number of loops, and whether images should be shuffled per loop. The script utilizes MoviePy for video generation and PySimpleGUI for user interaction.

## Features

- **Customizable Duration**: Set the display duration of each image in seconds.
- **Loops**: Specify the number of times the video should loop.
- **Shuffle**: Randomize the order of images in each loop.
- **Aspect Ratio Maintenance**: Resizes images to maintain aspect ratio while fitting them to an average dimension.
- **Bordered Images**: Creates bordered images if necessary to match the average dimensions.

## Installation and Usage
- For Windows users, you can simply run the `start.bat` file to start the application, at the first run it will install the required dependencies on a venv (isolated environment) and then ask you to press any key to continue before starting the application.
- For Linux and macOS users, be sure to make the script executable before running:
```bash
chmod +x install.sh
chmod +x start.sh
```

- Then you can run the `start.sh` script to install dependencies and start the application.

### Using the Application
- Select the folder containing the images.
- Customize the duration, number of loops, and shuffle option.
- Choose a save location and name for the output video.

## Requirements (package_manager.py should handle this for you)

- Python 3.x
- MoviePy
- PySimpleGUI (version 4.60.4 recommended as 5.x is paid)
- Pillow (PIL)

## Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.