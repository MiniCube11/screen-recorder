import os
import sys

welcome_text = """

Welcome to Screen Recorder

 --------------------
|                    |
|        ---         |
|       |   |        |
|        ---         |
|                    |
 --------------------
"""

help_text = """
start       Start recording
save        Save recorded frames into a gif or video
"""

commands = ["start", "save", "help", "quit"]


def welcome_screen():
    print(welcome_text + help_text)


def quit_program():
    print()
    print("Program ended by user.")
    sys.exit()


def get_input(prompt):
    try:
        return input(prompt)
    except EOFError:
        quit_program()
    except KeyboardInterrupt:
        quit_program()


def get_valid_integer(prompt, optional=False, default=None):
    while True:
        user_input = get_input(prompt)
        if user_input.isdigit():
            user_input = int(user_input)
            return user_input
        if optional and not user_input:
            return default
        print(f"Please enter a valid integer.")


def get_valid_input(prompt, valid_inputs, optional=False, default=None):
    while True:
        user_input = get_input(prompt)
        if user_input in valid_inputs:
            return user_input
        if optional and not user_input:
            return default
        print(f"Please enter a valid input ({'/'.join(valid_inputs)}).")


def get_valid_directory(prompt):
    while True:
        user_input = get_input(prompt)
        if os.path.isdir(user_input):
            return user_input
        print(f"Directory '{user_input}' not found.")


def get_option():
    while True:
        option = get_valid_input("Enter a command: ", commands)
        if option == "help":
            print(help_text)
        else:
            return option
