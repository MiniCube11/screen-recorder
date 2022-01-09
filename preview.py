import tkinter as tk
from PIL import Image, ImageTk


def preview_window(record_image):
    window = tk.Tk()
    window.title("Preview - Close window to continue")

    record_image("demo.png")

    image = Image.open("demo.png")
    image.thumbnail((500, 500), Image.ANTIALIAS)

    tkimage = ImageTk.PhotoImage(image)
    label = tk.Label(window, image=tkimage)
    label.pack()

    def update():
        record_image("demo.png")

        image = Image.open("demo.png")
        image.thumbnail((500, 500), Image.ANTIALIAS)
        tkimage = ImageTk.PhotoImage(image)

        label.configure(image=tkimage)
        label.image = tkimage
        label.after(500, update)

    update()
    window.mainloop()
