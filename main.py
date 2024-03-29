from record import record, save
from helper import get_option, welcome_screen, quit_program

images = []
average_time = 0

welcome_screen()
while True:
    try:
        option = get_option()
        if option == "start":
            record()
        elif option == "save":
            save()
        else:
            quit_program()
    except KeyboardInterrupt:
        quit_program()
    except EOFError:
        quit_program()
