import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk

class Node:
    def __init__(self, value):
        self.value = value
        self.right = None
        self.left = None

class BinarySearchGUI(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.orig_bg = Image.open("assets/background.png")
        self.bg_img = ImageTk.PhotoImage(self.orig_bg)
        self.bg_id = self.canvas.create_image(0, 0, anchor="nw", image=self.bg_img, tags=("bg",))

        self.tree_frame = tk.Frame(self)
        self.tree_frame.place(relx=0.5, rely=0.55, anchor="center", width=1432, height=600)

        self.tree_frame.grid_rowconfigure(0, weight=1)
        self.tree_frame.grid_columnconfigure(0, weight=1)

        self.tree_canvas = tk.Canvas(self.tree_frame, bg="#1C4D8D", highlightthickness=0)
        self.tree_canvas.grid(row=0, column=0, sticky="nsew")

        self.tree_scrollbar_horizontal = tk.Scrollbar(
        self.tree_frame, orient="horizontal", command=self.tree_canvas.xview)
        self.tree_scrollbar_horizontal.grid(row=1, column=0, sticky="ew")

        self.tree_canvas.configure(xscrollcommand=self.tree_scrollbar_horizontal.set)

        self.tree_scrollbar_vertical = tk.Scrollbar(
        self.tree_frame, orient="vertical", command=self.tree_canvas.yview)
        self.tree_scrollbar_vertical.grid(row=0, column=1, sticky="ns")

        self.tree_canvas.configure(yscrollcommand=self.tree_scrollbar_vertical.set)

        self.setup_prog_label()
        self.setup_values_input()
        self.confirm_button()
        self.back_button()
        self.traversal_frame()

        self.canvas.bind("<Configure>", lambda e: self.resize_bg(e.width, e.height))
        self.after(100, self.force_redraw)

    def resize_bg(self, width, height):
        if width < 1 or height < 1:
            return
        resized = self.orig_bg.resize((width, height), Image.LANCZOS)
        self.bg_img = ImageTk.PhotoImage(resized)
        self.canvas.itemconfig(self.bg_id, image=self.bg_img)
        self.canvas.coords(self.bg_id, 0, 0)

    def force_redraw(self):
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w > 1 and h > 1:
            self.resize_bg(w, h)

    #for inserting new values in BST (left node= lower number or equal, right node = higher numbers)    
    def insert(self,root,value):
        if root is None:
            return Node(value)
        
        if value <= root.value:
            root.left = self.insert(root.left,value)
        else:
            root.right = self.insert(root.right,value)

        return root

    def inorder(self,root,result):
        if root is None:
            return
        self.inorder(root.left, result)
        result.append(root.value)
        self.inorder(root.right,result)

    def compute_subtree_width(self, node):
        if not node:
            return 1
        return self.compute_subtree_width(node.left) + self.compute_subtree_width(node.right)

    def assign_positions(self, node, depth, x_min, x_max):
        if not node:
            return

        mid = (x_min + x_max) // 2
        node.x = mid
        node.y = depth

        if node.left:
            w_left = self.compute_subtree_width(node.left)
            self.assign_positions(node.left, depth + 1,
                              x_min,
                              x_min + w_left * 120)
        if node.right:
            w_right = self.compute_subtree_width(node.right)
            self.assign_positions(node.right, depth + 1,
                              x_max - w_right * 120,
                              x_max)


    def draw_tree_inorder(self, root):
        self.tree_canvas.delete("all")

        # compute total width based on subtree sizes
        total_width = self.compute_subtree_width(root) * 120

        # correct call with required parameters
        self.assign_positions(root, depth=0, x_min=0, x_max=total_width)

        r = 20

        def draw(node):
            if not node:
                return

            x = node.x + 100
            y = node.y * 110 + 80

            # save actual root X position
            if node == root:
                self.root_x = x

            # draw left line
            if node.left:
                lx = node.left.x + 100
                ly = node.left.y * 110 + 80
                self.tree_canvas.create_line(
                x, y, lx, ly, fill="white", width=2, tags=("tree",)
            )

            # draw right line
            if node.right:
                rx = node.right.x + 100
                ry = node.right.y * 110 + 80
                self.tree_canvas.create_line(
                x, y, rx, ry, fill="white", width=2, tags=("tree",)
            )

            # draw node
            self.tree_canvas.create_oval(
                x - r, y - r, x + r, y + r,
                fill="#cab7d9",
                tags=("tree",))
            
            self.tree_canvas.create_text(
            x, y, text=str(node.value),
            font=("Arial", 12, "bold"),
            tags=("tree",)
        )

            draw(node.left)
            draw(node.right)

        draw(root)

        # update scrollregion
        self.tree_canvas.update_idletasks()
        self.tree_canvas.configure(scrollregion=self.tree_canvas.bbox("all"))

        canvas_height = self.tree_canvas.winfo_height()
        x1, y1, x2, y2 = self.tree_canvas.bbox("all")

        tree_height = y2 - y1
        if tree_height < canvas_height:
            offset = (canvas_height - tree_height) / 2 - y1
            self.tree_canvas.move("all", 0, offset)

        # center root horizontally
        x1, y1, x2, y2 = self.tree_canvas.bbox("all")
        canvas_width = self.tree_canvas.winfo_width()

        if canvas_width > 1:
            tree_width = x2 - x1
            fraction = (self.root_x - canvas_width/2) / tree_width
            self.tree_canvas.xview_moveto(max(0, min(1, fraction)))

    def setup_prog_label(self):
        self.label_frame = Frame(self, bg = "#6e7bb2",
                                 bd = 8, relief = "solid")
        self.label_frame.place(relx=0.993, rely=0.01, width=450, height=60, anchor="ne")

        self.label_text = Label(self.label_frame, text="Binary Search Tree",
                                font=("Press Start 2P", 15, "bold"),
                                fg = "white",
                                bg="#6e7bb2")
        self.label_text.pack(padx=10, pady=10)

    def display_count(self):
        raw_count = self.values_input.get()
        valid_numbers = []

        for count in raw_count.split(","):
            count = count.strip()

            if count != "":
                valid_numbers.append(int(count))
        
        total_count = len(valid_numbers)

        self.number_count_display.config(state="normal")
        self.number_count_display.delete(0, END)
        self.number_count_display.insert(0, total_count)

    def setup_values_input(self):
        self.values_frame = tk.Frame(self, bg="#6e7bb2",
                                     bd = 5, relief = "solid")
        self.values_frame.place(relx=0.007, rely=0.09, width=1513, height=50, anchor="nw")

        self.values_label = tk.Label(self.values_frame, text="Input number of values:",
                                font=("Montserrat", 15, "bold"),
                                fg="black",
                                bg="#6e7bb2")
        self.values_label.grid(row=0, column=0, padx=10, pady=7)

        self.values_input = tk.Entry(self.values_frame,
                                font=("Montserrat", 15), width=100,
                                fg="#000000", bg="#FFFFFF")
        self.values_input.grid(row=0, column=1, padx=0.9, sticky="e")
        self.values_input.bind("<Key>", lambda event: self.error_label.config(text=""))
        self.values_input.bind("<KeyRelease>", lambda e: self.display_count(), add = "+")
        self.values_input.bind("<KeyRelease>", self.auto_clear_canvas, add = "+")

        self.tip_label = tk.Label(self,
                                text="", font=("Montserrat", 12),
                                bg="black",
                                fg="white")
        self.tip_label.place(relx=0.992, rely=0.157, width=330, anchor="ne")
        self.tip_label.config(text="Input must be minimum of 10, maximum of 30")

        self.error_label = Label(self, text="", font=("Press Start 2P", 13), fg="red", bg="#6e7bb2")
        self.error_label.place(relx=0.98, rely=0.109, anchor="ne")

        self.number_count_label = Label(self, text=" Number count:", font=("Montserrat",13), width = 17, fg="white", bg="black", anchor ="w")
        self.number_count_label.place(relx=0.1112, rely=0.157, anchor="ne")

        self.number_count_display = Entry(self, font = ("Montserrat", 13), fg = "white", relief = "flat", bg="black", justify = "left")
        self.number_count_display.place(relx= 0.092, rely= 0.173, width= 20, anchor = "center")

    def auto_clear_canvas(self, event=None):
        text = self.values_input.get().strip()

        if text == "":
            self.tree_canvas.delete("all")
            self.traversal_label.config(text="Inorder:")

            self.error_label.config(text="")

    def confirm_button(self):
        self.tree_btn = tk.Button(self, text="Generate Tree",
                                font=("Montserrat", 15, "bold"), bd=8,
                                fg="black",
                                bg="#b3d9ff",
                                padx=10, pady=7)
        self.tree_btn.config(command=lambda: self.confirm_input())
        self.tree_btn.place(relx=0.007, rely=0.01, width=180, height=60, anchor="nw")

    def back_button(self):
        self.back_btn = tk.Button(self, text="Back",
                                font=("Press Start 2P", 15, "bold"), bd=8,
                                fg="white",
                                bg="#17357a",
                                padx=10, pady=7)
        self.back_btn.config(command=lambda: self.go_back())
        self.back_btn.place(relx=0.994, rely=0.99, width=150, height=50, anchor="se")

    def go_back(self):
        self.master.show_frame(self.master.MainMenuFrame)

    def confirm_input(self):
        raw_number_value = self.values_input.get()
        number_values = []

        try:
            self.error_label.config(text="")

            for num in raw_number_value.split(","):
                num = num.strip()
                if num == "":
                    raise ValueError("Empty Value")
                
                if not num.isdigit():
                    raise ValueError("Not a number")
            
                number_values.append(int(num))
            if not (10 <= len(number_values) <= 30):
                raise ValueError("Invalid Count")

            root = None
            for number in number_values:
                root = self.insert(root,number)   
       
        except:
            self.error_label.config(text="INVALID")
            return

        result = []
        self.inorder(root, result)
        self.traversal_label.config(text="Inorder: " + " ".join(map(str, result)))

        self.tree_canvas.delete("all")                                          
        
        self.draw_tree_inorder(root)
        

    def traversal_frame(self):
        self.traversal_container = tk.Frame(self, bg="#b3d9ff",
                                bd = 5, relief = "solid")
        self.traversal_container.place(relx=0.007, rely=0.99, width=1350, height=50, anchor="sw")

        self.traversal_label = tk.Label(self.traversal_container, text=" Inorder:",
                                font=("Montserrat", 15, "bold"),
                                fg="black",
                                bg="#b3d9ff",
                                justify="left", anchor="w")
        self.traversal_label.pack(padx=2, pady=2, fill="both")