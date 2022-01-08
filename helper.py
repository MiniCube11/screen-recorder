welcome_text = """

Welcome to Screen to GIF

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
save        Save recorded frames into a gif
"""

commands = ["start", "save", "help"]


def welcome_screen():
    print(welcome_text + help_text)


def get_valid_integer(prompt, optional=False, default=None):
    while True:
        user_input = input(prompt)
        if user_input.isdigit():
            user_input = int(user_input)
            return user_input
        if optional and not user_input:
            return default
        print(f"Please enter a valid input ({'/'.join(valid_inputs)}).")


def get_valid_input(prompt, valid_inputs, optional=False, default=None):
    while True:
        user_input = input(prompt)
        if user_input in valid_inputs:
            return user_input
        if optional and not user_input:
            return default
        print(f"Please enter a valid input ({'/'.join(valid_inputs)}).")


def get_option():
    while True:
        option = get_valid_input("Enter a command: ", commands)
        if option == "help":
            print(help_text)
        else:
            return option
