# img folder to movie generator.py
from package_manager import ensure_package

ensure_package('moviepy')
ensure_package('PySimpleGUI', 'PySimpleGUI==4.60.4')
ensure_package('PIL', 'Pillow')

# import all required modules
from moviepy.editor import ImageSequenceClip
import PySimpleGUI as sg
import os,tempfile,random
from PIL import Image
import moviepy.editor as mp
from concurrent.futures import ThreadPoolExecutor
from typing import List, Tuple, Optional
from tkinter import filedialog

def calculate_average_dimensions(images: List[Tuple[int, int]]) -> Tuple[int, int]:
    total_width = total_height = 0
    for width, height in images:
        total_width += width
        total_height += height
    avg_width = total_width // len(images)
    avg_height = total_height // len(images)
    return avg_width, avg_height

def resize_image(image_path: str, avg_width: int, avg_height: int) -> str:
    with Image.open(image_path) as img:
        width, height = img.size

        # Calculate aspect ratios
        aspect_ratio = width / height
        avg_aspect_ratio = avg_width / avg_height

        # Initialize bordered_img to None
        bordered_img = None

        if width == avg_width and height == avg_height:
            # Image exactly matches the target dimensions
            return image_path

        # Determine if image needs to be upscaled or has an aspect ratio difference
        upscale_or_aspect_diff = width < avg_width and height < avg_height or aspect_ratio != avg_aspect_ratio

        if upscale_or_aspect_diff:
            # Determine new dimensions based on various conditions
            if width < avg_width and height < avg_height:
                scale_factor_width = avg_width / width
                scale_factor_height = avg_height / height
                if scale_factor_width < scale_factor_height:
                    new_width = avg_width
                    new_height = int(new_width / aspect_ratio)
                else:
                    new_height = avg_height
                    new_width = int(new_height * aspect_ratio)
            elif aspect_ratio > avg_aspect_ratio:
                new_height = int(avg_width / aspect_ratio)
                new_width = avg_width
            else:  # aspect_ratio <= avg_aspect_ratio
                new_width = int(avg_height * aspect_ratio)
                new_height = avg_height

            # Resize the image
            resized_img = img.resize((new_width, new_height), Image.ANTIALIAS)

            # Create a bordered image if necessary
            if new_width != avg_width or new_height != avg_height:
                border_width = (avg_width - new_width) // 2
                border_height = (avg_height - new_height) // 2
                bordered_img = Image.new('RGB', (avg_width, avg_height), (0, 0, 0))
                bordered_img.paste(resized_img, (border_width, border_height))
            else:
                bordered_img = resized_img

        # Save resized (and possibly bordered) image to a temporary file
        temp_file = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
        bordered_img.save(temp_file.name, 'JPEG')
        return temp_file.name

def get_image_dimensions(image_path: str) -> Tuple[int, int]:
    with Image.open(image_path) as img:
        return img.size

def process_images(images: List[str], avg_width: int, avg_height: int) -> List[str]:
    with ThreadPoolExecutor() as executor:
        return list(executor.map(lambda img: resize_image(img, avg_width, avg_height), images))

def validate_numeric_input(value: str, min_value: float = 0, default: float = None) -> Optional[float]:
    """Validate if the input is a positive number."""
    if not value and default is not None:
        return default
    try:
        num = float(value)
        return num if num >= min_value else default
    except ValueError:
        return default

def validate_integer_input(value: str, min_value: int = 1, default: int = None) -> Optional[int]:
    """Validate if the input is a positive integer."""
    if not value and default is not None:
        return default
    try:
        num = float(value)  # First convert to float to handle decimal inputs
        num = int(num)  # Then convert to int, effectively rounding down
        return num if num >= min_value else default
    except ValueError:
        return default

def create_layout() -> List[List[sg.Element]]:
    """Create the PySimpleGUI layout with default values and tooltips."""
    return [
        [sg.Text("Select a folder with image frames:"), sg.Input(key="-FOLDER-"), sg.FolderBrowse()],
        [sg.Text("Duration of Image Display (seconds):"),
         sg.InputText("0.5", key="-DURATION-", tooltip="Enter a number for how many seconds each image will be displayed before changing to the next image")],
        [sg.Text("Number of Loops:"),
         sg.InputText("1", key="-LOOPS-", tooltip="Enter a number of times all images inside the folder should be displayed, value will be converted to integer")],
        [sg.Checkbox("Shuffle Images per Loop", key="-SHUFFLE-"), sg.OK(button_text='generate video'), sg.Cancel()]
    ]

def process_video(folder_path: str, duration: float, num_loops: int, shuffle_images: bool) -> Optional[mp.VideoFileClip]:
    """Process images and create video clip."""
    supported_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.webp', '.gif')
    images = [os.path.join(root, file) for root, _, files in os.walk(folder_path)
              for file in files if file.lower().endswith(supported_extensions)]

    if not images:
        sg.popup_error("No images found in the selected folder.")
        return None

    dimensions = [get_image_dimensions(img) for img in images]
    avg_width, avg_height = calculate_average_dimensions(dimensions)
    resized_images = process_images(images, avg_width, avg_height)

    durations = [duration] * len(resized_images)
    clips = []

    for _ in range(num_loops):
        if shuffle_images:
            random.shuffle(resized_images)
        clip = ImageSequenceClip(resized_images, durations=durations)
        clips.append(clip)

    return mp.concatenate_videoclips(clips) if len(clips) > 1 else clips[0]

def main():
    sg.theme('DefaultNoMoreNagging')
    layout = create_layout()
    window = sg.Window("Image to Video Converter", layout)

    while True:
        event, values = window.read()
        if event in (sg.WINDOW_CLOSED, 'Cancel'):
            break

        if event == 'OK':
            folder_path = values["-FOLDER-"]
            duration = validate_numeric_input(values["-DURATION-"], min_value=0.1, default=0.5)
            num_loops = validate_integer_input(values["-LOOPS-"], min_value=1, default=1)
            shuffle_images = values["-SHUFFLE-"]

            if not folder_path:
                sg.popup_error("Please select a folder with images.")
                continue

            final_clip = process_video(folder_path, duration, num_loops, shuffle_images)

            if final_clip:
                save_path = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")])
                if save_path:
                    final_clip.write_videofile(save_path, fps=30)
                    sg.popup("Video saved successfully!")
                else:
                    sg.popup("Operation cancelled. No video was saved.")

    window.close()

if __name__ == "__main__":
    main()