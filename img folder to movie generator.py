from moviepy.editor import ImageSequenceClip
import PySimpleGUI as sg
import os,tempfile,random
from PIL import Image
import moviepy.editor as mp
from concurrent.futures import ThreadPoolExecutor
from typing import List, Tuple, Optional

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

def main():
    layout = [
        [sg.Text("Select a folder with image frames:"), sg.Input(), sg.FolderBrowse()],
        [sg.Text("Customization Options:"), sg.Text("Duration of Image Display (in seconds):"), sg.InputText()],
        [sg.Text("Number of Loops (default is 1):"), sg.InputText()],
        [sg.Checkbox("Shuffle Images per Loop"), sg.OK(), sg.Cancel()]
    ]

    window = sg.Window("Image to Video Converter", layout)
    event, values = window.read()
    window.close()


    if event in (sg.WINDOW_CLOSED, 'Cancel'):
        raise SystemExit("User cancelled or closed the window.")

    folder_path = values[0]
    duration = float(values[1]) if values[1] else 1  # Ensuring default values if not provided
    num_loops = int(values[2]) if values[2] else 1
    shuffle_images = values[3]

    images = [os.path.join(root, file) for root, _, files in os.walk(folder_path)
              for file in files if file.lower().endswith(('.png', '.jpg', '.jpeg'))]

    if not images:
        sg.popup("No images found in the folder.")
        return

    dimensions = [get_image_dimensions(img) for img in images]
    avg_width, avg_height = calculate_average_dimensions(dimensions)
    resized_images = process_images(images, avg_width, avg_height)

        # Define durations for each image frame in the video
    durations = [duration] * len(resized_images)
    clips = []

    # Loop through the number of loops specified by the user
    for _ in range(num_loops):
        if shuffle_images:
            random.shuffle(resized_images)

        # Create a video clip from the resized (and possibly shuffled) images
        clip = ImageSequenceClip(resized_images, durations=durations)
        clips.append(clip)

    # Concatenate clips if more than one loop is specified
    if len(clips) > 1:
        final_clip = mp.concatenate_videoclips(clips)
    else:
        final_clip = clips[0]

    # Prompt the user for a save location and file name for the output video
    save_path = sg.popup_get_file("Save video file", save_as=True, default_extension=".mp4")
    if save_path:
        final_clip.write_videofile(save_path, fps=30)

        # Cleanup: Delete temporary image files
        for img_path in resized_images:
            os.unlink(img_path)
    else:
        sg.popup("Operation cancelled. No video was saved.")

if __name__ == "__main__":
    main()