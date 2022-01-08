from record import record, save
from helper import get_option, welcome_screen

images = []
average_time = 0

welcome_screen()
while True:
    option = get_option()
    if option == "start":
        record()
    elif option == "save":
        save()
