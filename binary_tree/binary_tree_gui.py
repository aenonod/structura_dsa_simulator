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

        self.bg_image = tk.PhotoImage(file="assets/background.png")
        self.bg_id = self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image, tags=("bg",))

        self.bind("<Configure>", self.resize_bg)
        
        self.tree = BinaryTree()
        self.setup_prog_label()
        self.setup_height_input()
        self.setup_values_input()
        self.generate_tree_button()
        self.traversal_frame()
        self.back_button()

        self.values_input.bind("<Key>", lambda e: self.error_label.config(text=""))
        self.values_input.bind("<KeyRelease>", lambda e: self.display_count())

        self.number_count = Label(
            self.canvas,
            text="  Number count:                  ",
            font=("Montserrat", 12),
            fg="white",
            bg="black")
        self.number_count.place(relx=0.977, rely=0.184, anchor="ne")

        self.number_count_display = tk.Entry(
            self.canvas,
            font=("Montserrat", 12),
            relief="flat",
            fg="white", 
            bg="black")
        self.number_count_display.place(relx=0.983, rely=0.198, width=30, height=24, anchor="center")

        self.display_count()

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
        self.tip_label.config(text="Tip: type 'n/a' to skip a node.")

    def display_count(self):
        raw_count = self.values_input.get()
        valid_inputs = []

        for count in raw_count.split(","):
            count = count.strip()
            if count != "":
                valid_inputs.append(count)

        total_count = len(valid_inputs)

        self.number_count_display.delete(0, END)
        self.number_count_display.insert(0, total_count)

    def generate_tree_button(self):
        self.tree_btn = tk.Button(self, text="Generate Tree",
                                font=("Montserrat", 15, "bold"), bd=8,
                                fg="black",
                                bg="#b3d9ff",
                                padx=10, pady=7)
        self.tree_btn.config(command=lambda: self.generate_tree())
        self.tree_btn.place(relx=0.007, rely=0.01, width=180, height=60, anchor="nw")

    def draw_tree(self, node, x, y, dx):
        if not node:
            return

        r = 28
        self.canvas.create_oval(x-r, y-r, x+r, y+r, fill="lightblue", outline="black", tags=("tree",))
        self.canvas.create_text(x, y, text=str(node.data), font=("Montserrat", 13, "bold"), tags=("tree",))

        if node.left:
            self.canvas.create_line(x, y+r, x-dx, y+100-r, width=3, tags="tree")
            self.draw_tree(node.left, x-dx, y+80, dx//2)

        if node.right:
            self.canvas.create_line(x, y+r, x+dx, y+100-r, width=3, tags="tree")
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
        raw_values = self.values_input.get().split(",")

        if len(raw_values) < self.max_nodes or len(raw_values) > self.max_nodes:
            messagebox.showerror("Error", f"You must enter exactly {self.max_nodes} values.\n" f"Use 'n/a' for empty nodes.")
            return

        self.values = []
        for i, val in enumerate(raw_values):
            val = val.strip()
            if val == "":
                messagebox.showerror("Error", f"Invalid input at position {i+1}. Please remove empty or invalid values.")
                return
            else:
                self.values.append(val)

        self.tree.build_bt(self.height_int, self.values)
        
        if self.tree.root:
            self.draw_tree(self.tree.root, 780, 200, 360)

        self.traversal()

    def traversal_frame(self):
        self.traversal_frame = tk.Frame(self, bg="#b3d9ff",
                                bd = 5, relief = "solid")
        self.traversal_frame.place(relx=0.007, rely=0.99, width=1350, height=130, anchor="sw")

        self.traversal_label = tk.Label(self.traversal_frame, text="Inorder:\nPreorder:\nPostorder: ",
                                font=("Montserrat", 15, "bold"),
                                fg="black",
                                bg="#b3d9ff",
                                justify="left", anchor="w")
        self.traversal_label.pack(padx=20, pady=20, fill="both")

    def traversal(self):
        inorder = "  ".join(map(str, self.tree.get_inorder()))
        preorder = "  ".join(map(str, self.tree.get_preorder()))
        postorder = "  ".join(map(str, self.tree.get_postorder()))

        text = f"Inorder: {inorder}\nPreorder: {preorder}\nPostorder: {postorder}"
        self.traversal_label.config(text=text)

    def back_button(self):
        self.back_btn = tk.Button(self, text="Back",
                                font=("Press Start 2P", 15, "bold"), bd=8,
                                fg="white",
                                bg="#17357a",
                                padx=10, pady=7)
        self.back_btn.config(command=lambda: self.main_menu())
        self.back_btn.place(relx=0.994, rely=0.99, width=150, height=50, anchor="se")


if __name__ == "__main__":
    app = TreeGUI()
    app.mainloop()