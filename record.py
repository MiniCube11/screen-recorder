import os
import sys
import shutil
import time
from PIL import Image, ImageGrab
from helper import get_valid_input, get_valid_integer


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


def start_recording():
    if input("Press enter to start recording, Ctrl+C to stop recording, q to quit: ") == "q":
        cancel_recording()


def record_frame(directory, index):
    image = ImageGrab.grab()
    image.save(f"{directory}/{index}.png")


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


def get_images(directory):
    images = []
    index = 1
    average_time = 70

    try:
        with open(f"{directory}/info.txt", "r") as f:
            average_time = int(f.readline())
    except:
        print(
            f"Using default values, {directory}/info.txt is either missing or corrupted.")

    while True:
        filename = f"{directory}/{index}.png"
        if os.path.isfile(filename):
            with Image.open(filename) as image:
                image.load()
                images.append(image)
        else:
            break
        index += 1

    return images, average_time


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
    print("Saving recording...")

    images, average_time = get_images(filename)

    if end_frame is None:
        end_frame = len(images) + 1

    to_gif(images, filename, start_frame=start_frame,
           end_frame=end_frame, duration=average_time)


def record():
    filename = input("Enter filename: ")
    create_directory(filename)

    start_recording()
    record_frames(filename)

    save_gif(filename)


def save():
    filename = input("Enter name of recording: ")
    start_frame = get_valid_integer(
        "Start at frame (enter to use first frame): ", optional=True, default=1)
    end_frame = get_valid_integer(
        "End at frame (enter to use last frame): ", optional=True, default=None)

    save_gif(filename, start_frame=start_frame, end_frame=end_frame)
