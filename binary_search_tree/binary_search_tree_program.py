import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk

class Node:
    def __init__(self,value):
        self.value = value
        self.right = None
        self.left = None

class TreeGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Structura")
        self.attributes("-fullscreen", True)
        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False))


        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.orig_bg = Image.open("assets/background.png")
        self.bg_img = ImageTk.PhotoImage(self.orig_bg)
        self.bg_id = self.canvas.create_image(0, 0, anchor="nw", image=self.bg_img, tags=("bg",))

        self.tree_frame = tk.Frame(self)
        self.tree_frame.place(x=80, y=180, width=1400, height=600)

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

        self.canvas.bind("<Configure>", self.resize_bg)
        self.after(100, self.force_redraw)

    def resize_bg(self, event):
        if event.width < 1 or event.height < 1:
            return
        resized = self.orig_bg.resize((event.width, event.height), Image.LANCZOS)
        self.bg_img = ImageTk.PhotoImage(resized)
        self.canvas.itemconfig(self.bg_id, image=self.bg_img)
        self.canvas.coords(self.bg_id, 0, 0)

    def force_redraw(self):
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w > 1 and h > 1:
            self.resize_bg(tk.Event(width=w, height=h))

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

    def draw_bst(self, node, x, y, dx, depth=0):
        if not node:
            return

        circle_radius = 20
        v_space = 60  

        if node.left:
            next_dx = max(dx * 0.5, 40)
            self.tree_canvas.create_line(x, y, x - dx, y + v_space, fill="white", width=2, tags="tree")
            self.draw_bst(node.left, x - dx, y + v_space, next_dx, depth + 1)

        if node.right:
            next_dx = max(dx * 0.5, 40)
            self.tree_canvas.create_line(x, y, x + dx, y + v_space, fill="white", width=2, tags="tree")
            self.draw_bst(node.right, x + dx, y + v_space, next_dx, depth + 1)
        
        self.tree_canvas.create_oval(x-circle_radius, y-circle_radius, x+circle_radius, y+circle_radius, fill="#cab7d9", tags = "tree")
        self.tree_canvas.create_text(x, y, text=str(node.value), font=("Arial", 12, "bold"), tags = "tree")

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
        self.back_btn.config(command=lambda: self.main_menu())
        self.back_btn.place(relx=0.994, rely=0.99, width=150, height=50, anchor="se")

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
        #9
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
        
        self.draw_bst(root,700,130,440)
        
        self.tree_canvas.update_idletasks()
        self.tree_canvas.configure(scrollregion=self.tree_canvas.bbox("all"))
        self.tree_canvas.xview_moveto(0.5)

        bstbox = self.tree_canvas.bbox("tree")
        if bstbox:
            x1, y1, x2, y2 = bstbox

            self.tree_canvas.configure(scrollregion=(x1-50, y1-50, x2+50, y2+50))

        self.tree_canvas.yview_moveto(0)

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

if __name__ == "__main__":
    app = TreeGUI()
    app.mainloop()