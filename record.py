import os
import sys
import shutil
import time
import cv2
from PIL import Image, ImageGrab
from preview import preview_window
from helper import get_input, get_valid_input, get_valid_integer, get_valid_directory


screen_width = -1
screen_height = -1


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
    x, y, x1, y1 = get_valid_coordinates(None, None, None, None)
    while True:
        user_input = get_valid_input(
            "Enter the name of the parameter you want to change (x/x1/y/y1, p to preview, enter to continue): ", ["x", "x1", "y", "y1", "p"], optional=True)
        if user_input is None:
            break
        if user_input == "p":
            print("Previewing:", (x, y, x1, y1))
            print("Close preview window to continue.")
            preview_window(record_image, (x, y, x1, y1))
        else:
            value = get_valid_integer(
                f"Enter a new value for {user_input} (enter to skip): ", optional=True)
            if value is None:
                continue
            if user_input == "x":
                x = value
            elif user_input == "x1":
                x1 = value
            elif user_input == "y":
                y = value
            else:
                y1 = value
            x, y, x1, y1 = get_valid_coordinates(x, y, x1, y1)

    if get_input("Press enter to start recording, Ctrl+C to stop recording, q to quit: ") == "q":
        cancel_recording()

    return (x, y, x1, y1)


def get_valid_coordinates(x, y, x1, y1):
    global screen_width, screen_height
    if screen_width == -1:
        image = ImageGrab.grab()
        screen_width, screen_height = image.size

    if x is None:
        x = 0
    if y is None:
        y = 0
    if x1 is None:
        x1 = screen_width
    if y1 is None:
        y1 = screen_height
    if x > x1:
        x, x1 = x1, x
    if y > y1:
        y, y1 = y1, y
    x = max(x, 0)
    y = max(y, 0)
    x1 = min(x1, screen_width)
    y1 = min(y1, screen_width)
    return (x, y, x1, y1)


def record_image(path, coordinates):

    image = ImageGrab.grab(coordinates)
    image.save(path)


def record_frame(directory, index, coordinates):
    record_image(f"{directory}/{index}.png", coordinates)


def record_frames(directory, coordinates):
    average_time = 0

    index = 1

    while True:
        try:
            start = time.time()
            record_frame(directory, index, coordinates)
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
    else:
        return filename

    return filename + str(increment)


def to_gif(images, filename, start_frame, end_frame, duration):
    start_frame -= 1
    end_frame -= 1

    start_frame = max(0, start_frame)
    end_frame = min(len(images) - 1, end_frame)

    images[start_frame].save(
        f"{filename}.gif",
        save_all=True,
        append_images=images[start_frame:end_frame],
        duration=duration,
        loop=0
    )

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


def save_video(directory, start_frame, end_frame):
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

    if end_frame is None:
        end_frame = len(images)

    start_frame -= 1
    end_frame -= 1

    start_frame = max(0, start_frame)
    end_frame = min(len(images) - 1, end_frame)

    framerate = 1000 / get_average_time(directory)

    filename = get_available_filename(directory, "avi")

    output = cv2.VideoWriter(
        filename + ".avi", cv2.VideoWriter_fourcc(*'MP42'), framerate, size)

    for image in images[start_frame:end_frame]:
        image = cv2.resize(image, size)
        output.write(image)

    output.release()
    print(f"Recording saved to {filename}.avi.")


def save_options(filename):
    extension = get_valid_input("Enter extension (gif/avi): ", ["gif", "avi"])

    start_frame = get_valid_integer(
        "Start at frame (enter to use first frame): ", optional=True, default=1)
    end_frame = get_valid_integer(
        "End at frame (enter to use last frame): ", optional=True, default=None)

    if extension == "gif":
        save_gif(filename, start_frame, end_frame)
    elif extension == "avi":
        save_video(filename, start_frame, end_frame)


def record():
    filename = get_input("Enter filename: ")
    create_directory(filename)

    coordinates = start_options()
    record_frames(filename, coordinates)

    save_options(filename)


def save():
    filename = get_valid_directory("Enter name of recording: ")
    save_options(filename)
