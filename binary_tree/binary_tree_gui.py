import tkinter as tk
from tkinter import *

class TreeGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Structura")
        self.attributes("-fullscreen", True)
        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False))

        self.setup_background()
        self.setup_prog_label()
        self.setup_height_input()
        self.setup_values_input()
        self.generate_tree_button()

    def setup_background(self):
        self.bg_image = PhotoImage(file="binary_tree/background.png")
        bg_label = Label(self, image=self.bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    def setup_prog_label(self):
        self.label_frame = Frame(self, bg = "#6e7bb2",
                                 bd = 8, relief = "solid")
        self.label_frame.place(relx=0.993, rely=0.01, width=400, height=60, anchor="ne")

        self.label_text = Label(self.label_frame, text="Binary Tree",
                                font=("Press Start 2P", 15, "bold"),
                                fg = "white",
                                bg="#6e7bb2")
        self.label_text.pack(padx=10, pady=10)

    def setup_height_input(self):
        self.height_frame = tk.Frame(self, bg="#6e7bb2",
                                     bd = 5, relief = "solid")
        self.height_frame.place(relx=0.007, rely=0.09, width=445, height=50, anchor="nw")

        self.height_label = tk.Label(self.height_frame, text="Tree height (2-5):",
                                font=("Montserrat", 15, "bold"),
                                fg="black",
                                bg="#6e7bb2")
        self.height_label.grid(row=0, column=0, padx=10, pady=7)

        self.height_input = tk.Entry(self.height_frame,
                                font=("Montserrat", 15), width=20,
                                fg="#000000", bg="#FFFFFF")
        self.height_input.grid(row=0, column=1, padx=10, sticky="e")

    def setup_values_input(self):
        self.values_frame = tk.Frame(self, bg="#6e7bb2",
                                     bd = 5, relief = "solid")
        self.values_frame.place(relx=0.30, rely=0.09, width=1065, height=50, anchor="nw")

        self.values_label = tk.Label(self.values_frame, text="Node values (comma-separated):",
                                font=("Montserrat", 15, "bold"),
                                fg="black",
                                bg="#6e7bb2")
        self.values_label.grid(row=0, column=0, padx=10, pady=7)

        self.values_input = tk.Entry(self.values_frame,
                                font=("Montserrat", 15), width=63,
                                fg="#000000", bg="#FFFFFF")
        self.values_input.grid(row=0, column=1, padx=10, sticky="e")

        self.tip_label = tk.Label(self,
                                text="", font=("Montserrat", 12),
                                bg="black",
                                fg="white")
        self.tip_label.place(relx=0.993, rely=0.152, width=210, anchor="ne")
        self.tip_label.config(text="Tip: type n/a to skip a node.")

    def generate_tree_button(self):
        self.generate_frame = tk.Frame(self, bg="#fcf6d9",
                                     bd = 8, relief = "solid")
        self.generate_frame.place(relx=0.007, rely=0.01, width=180, height=60, anchor="nw")

        self.generate_label = tk.Label(self.generate_frame, text="Generate Tree",
                                font=("Montserrat", 15, "bold"),
                                fg="black",
                                bg="#fcf6d9")
        self.generate_label.grid(row=0, column=0, padx=10, pady=7)


if __name__ == "__main__":
    app = TreeGUI()
    app.mainloop()