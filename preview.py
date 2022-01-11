import tkinter as tk
from PIL import Image, ImageTk


class Application(tk.Frame):
    def __init__(self, parent, record_image, coordinates, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.coordinates = coordinates
        self.record_image = record_image

        self.record_image("demo.png", self.coordinates)

        image = Image.open("demo.png")
        image.thumbnail((500, 500), Image.ANTIALIAS)
        tkimage = ImageTk.PhotoImage(image)

        self.label = tk.Label(self.parent, image=tkimage)
        self.label.pack()
        self.callback()

    def callback(self):
        self.record_image("demo.png", self.coordinates)

        image = Image.open("demo.png")
        image.thumbnail((500, 500), Image.ANTIALIAS)
        tkimage = ImageTk.PhotoImage(image)

        self.label.configure(image=tkimage)
        self.label.image = tkimage
        self.after_id = self.label.after(500, self.callback)


def preview_window(record_image, coordinates):
    root = tk.Tk()
    root.title("Preview - Close window to continue")
    Application(root, record_image, coordinates).pack()
    root.mainloop()
