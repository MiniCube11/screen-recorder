import os
import sys
import shutil
import time
import cv2
from PIL import Image, ImageGrab
from preview import preview_window
from helper import get_input, get_valid_input, get_valid_integer, get_valid_directory


def create_directory(directory):
    if os.path.exists(directory):
        if get_valid_input(
            f"The directory/file {directory} already exists. Overwrite? (y/n) ",
                ["y", "n"]).lower() == "n":
            cancel_recording()
        else:
            if os.path.isdir(directory):
                shutil.rmtree(directory)

    os.mkdir(directory)


def cancel_recording():
    print("Cancelling recording...")
    sys.exit()


def start_options():
    if input("See preview: ") == "y":
        print("Close preview window to continue.")
        preview_window(record_image)
        print("window closed.")
        time.sleep(1)
    if get_input("Press enter to start recording, Ctrl+C to stop recording, q to quit: ") == "q":
        cancel_recording()


def record_image(path):
    image = ImageGrab.grab()
    image.save(path)


def record_frame(directory, index):
    record_image(f"{directory}/{index}.png")


def record_frames(directory):
    average_time = 0

    index = 1

    while True:
        try:
            start = time.time()
            record_frame(directory, index)
            elapsed = time.time() - start
            average_time = (average_time * (index - 1) + elapsed) / index
            index += 1
        except KeyboardInterrupt:
            filename = f"{directory}/{index}.png"
            if os.path.isfile(filename):
                os.remove(filename)
            print("Recording stopped.")
            break

    average_time = round(average_time * 1000)

    with open(f"{directory}/info.txt", "w") as f:
        f.write(str(average_time))


def get_average_time(directory):
    average_time = 70

    try:
        with open(f"{directory}/info.txt", "r") as f:
            average_time = int(f.readline())
    except:
        print(
            f"Using default values, {directory}/info.txt is either missing or corrupted.")

    return average_time


def get_images(directory):
    images = []
    index = 1

    while True:
        filename = f"{directory}/{index}.png"
        if os.path.isfile(filename):
            with Image.open(filename) as image:
                image.load()
                images.append(image)
        else:
            break
        index += 1

    return images


def get_available_filename(filename, extension):
    extension = "." + extension
    increment = 1

    if os.path.isfile(filename + extension):
        while os.path.isfile(filename + str(increment) + extension):
            increment += 1

    return filename + str(increment)


def to_gif(images, filename, start_frame, end_frame, duration):
    start_frame -= 1
    end_frame -= 1

    images[start_frame].save(
        f"{filename}.gif",
        save_all=True,
        append_images=images[start_frame:end_frame],
        duration=duration,
        loop=0
    )
    # TODO

    print(f"Recording saved to {filename}.gif.")


def save_gif(filename, start_frame=1, end_frame=None):
    if not os.path.isdir(filename):
        print(f"Directory '{filename}' not found.")
        return

    print("Saving recording...")

    images = get_images(filename)
    average_time = get_average_time(filename)

    if len(images) == 0:
        print(f"No images found in directory '{filename}'.")
        return

    if end_frame is None:
        end_frame = len(images) + 1

    filename = get_available_filename(filename, "gif")

    to_gif(images, filename, start_frame=start_frame,
           end_frame=end_frame, duration=average_time)


def save_video(directory):
    print("Saving recording...")

    size = (600, 400)
    index = 1
    images = []

    while True:
        filename = f"{directory}/{index}.png"
        if os.path.isfile(filename):
            image = cv2.imread(filename)
            height, width, _ = image.shape
            size = (width, height)
            images.append(image)
        else:
            break
        index += 1

    if len(images) == 0:
        print(f"No images found in directory '{directory}'.")
        return

    framerate = 1000 / get_average_time(directory)

    filename = get_available_filename(directory, "avi")

    output = cv2.VideoWriter(
        filename + ".avi", cv2.VideoWriter_fourcc(*'MP42'), framerate, size)

    for image in images:
        image = cv2.resize(image, size)
        output.write(image)

    output.release()
    print(f"Recording saved to {filename}.avi.")


def save_options(filename):
    extension = get_valid_input("Enter extension (gif/avi): ", ["gif", "avi"])

    if extension == "gif":
        start_frame = get_valid_integer(
            "Start at frame (enter to use first frame): ", optional=True, default=1)
        end_frame = get_valid_integer(
            "End at frame (enter to use last frame): ", optional=True, default=None)

        save_gif(filename, start_frame=start_frame, end_frame=end_frame)

    elif extension == "avi":
        save_video(filename)


def record():
    filename = get_input("Enter filename: ")
    create_directory(filename)

    start_options()
    record_frames(filename)

    save_options(filename)


def save():
    filename = get_valid_directory("Enter name of recording: ")
    save_options(filename)
