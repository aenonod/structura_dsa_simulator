import tkinter as tk
from tkinter import *

class TreeGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1920x1080")
        self.title("Structura")

        self.setup_background()

    def setup_background(self):
        self.bg_image = PhotoImage(file="binary_tree/background.png")
        bg_label = Label(self, image=self.bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)


if __name__ == "__main__":
    app = TreeGUI()
    app.mainloop()