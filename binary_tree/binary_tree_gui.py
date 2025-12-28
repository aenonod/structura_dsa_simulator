import tkinter as tk
from tkinter import *
from tkinter import messagebox
from binary_tree_program import BinaryTree

class TreeGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Structura")
        self.attributes("-fullscreen", True)
        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False))

        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.bg_image = tk.PhotoImage(file="binary_tree/background.png")
        self.bg_id = self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image, tags=("bg",))

        self.bind("<Configure>", self.resize_bg)
        
        self.tree = BinaryTree()
        self.setup_prog_label()
        self.setup_height_input()
        self.setup_values_input()
        self.generate_tree_button()

    def resize_bg(self, event):
        self.canvas.coords(self.bg_id, 0, 0)

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
        self.height_frame = tk.Label(self, bg="#6e7bb2",
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
        self.tree_btn = tk.Button(self, text="Generate Tree",
                                font=("Montserrat", 15, "bold"), bd=8,
                                fg="black",
                                bg="#fcf6d9",
                                padx=10, pady=7)
        self.tree_btn.config(command=lambda: self.generate_tree())
        self.tree_btn.place(relx=0.007, rely=0.01, width=180, height=60, anchor="nw")

    def draw_tree(self, node, x, y, dx):
        if not node:
            return

        r = 28
        self.canvas.create_oval(x-r, y-r, x+r, y+r, fill="lightblue", tags=("tree",))
        self.canvas.create_text(x, y, text=str(node.data), font=("Montserrat", 13, "bold"), tags=("tree",))

        if node.left:
            self.canvas.create_line(x, y+r, x-dx, y+100-r, width=3)
            self.draw_tree(node.left, x-dx, y+80, dx//2)

        if node.right:
            self.canvas.create_line(x, y+r, x+dx, y+100-r, width=3)
            self.draw_tree(node.right, x+dx, y+80, dx//2)

    def generate_tree(self):
        self.canvas.delete("tree")

        height_str = self.height_input.get()
        try:
            self.height_int = int(height_str)
            if not (2 <= self.height_int <= 5):
                messagebox.showerror("Error", "Input must be an integer between 2-5.")
                return
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid integer.")
            return
        
        self.max_nodes = (2 ** self.height_int) - 1
        self.values = [val.strip() for val in self.values_input.get().split(",")]
        self.tree.build_bt(self.height_int, self.values)

        if len(self.values) != self.max_nodes:
            messagebox.showerror("Error", f"Please enter exactly {self.max_nodes} values (comma-separated).")
            return
        
        if self.tree.root:
            self.draw_tree(self.tree.root, 780, 200, 360)


if __name__ == "__main__":
    app = TreeGUI()
    app.mainloop()