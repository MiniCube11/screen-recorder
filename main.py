import os
import sys
import shutil
import time
from PIL import ImageGrab

images = []
average_time = 0


def get_valid_input(prompt, valid_inputs):
    while True:
        user_input = input(prompt)
        if user_input in valid_inputs:
            return user_input
        print(f"Please enter a valid input ({'/'.join(valid_inputs)}).")


def cancel_recording():
    print("Cancelling recording...")
    sys.exit()


def start_recording():
    if input("Press enter to start recording, Ctrl+C to stop recording, q to quit: ") == "q":
        cancel_recording()


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


def record_frame(directory, index):
    image = ImageGrab.grab()
    image.save(f"{directory}/{index}.jpg")
    images.append(image)


def record_frames(directory):
    global average_time

    index = 1

    while True:
        try:
            start = time.time()
            record_frame(directory, index)
            elapsed = time.time() - start
            average_time = (average_time * (index - 1) + elapsed) / index
            index += 1
        except KeyboardInterrupt:
            break

    average_time = round(average_time * 1000)


def to_gif(filename, start_frame, end_frame):
    start_frame -= 1
    end_frame -= 1

    images[start_frame].save(
        f"{filename}.gif",
        save_all=True,
        append_images=images[start_frame:end_frame],
        optimize=False,
        duration=average_time,
        loop=0
    )


filename = input("Enter filename: ")
create_directory(filename)

start_recording()
record_frames(filename)
print("Saving recording...")

to_gif(filename, start_frame=1, end_frame=len(images))
print(f"Recording saved to {filename}.gif.")
