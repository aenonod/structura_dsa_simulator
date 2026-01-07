import tkinter as tk
from tkinter import *

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

        self.bg_image = tk.PhotoImage(file="assets/background.png")
        self.bg_id = self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image, tags=("bg",))

        self.setup_prog_label()
        self.setup_values_input()
        self.confirm_button()
        self.back_button()
        self.traversal_frame()

    #for inserting new values in BST (left node= lower number or equal, right node = higher numbers)    
    def insert(self,root,value):
        if root is None:
            return Node(value)
        
        if value < root.value:
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

    def draw_bst(self,node,x,y,dx):
        if not node:
            return
        circle_radius = 15
        v_space = 50

        if node.left:
            next_dx_left = max(dx * 0.5, 20)
            self.canvas.create_line(x, y, x - dx, y + v_space, fill="white", width=2)
            self.draw_bst(node.left, x - dx, y + v_space, next_dx_left)

        if node.right:
            next_dx_right = max(dx * 0.5, 20)
            self.canvas.create_line(x, y, x + dx, y + v_space, fill="white", width=2)
            self.draw_bst(node.right, x + dx, y + v_space, next_dx_right)
        
        self.canvas.create_oval(x-circle_radius, y-circle_radius, x+circle_radius, y+circle_radius, fill="#cab7d9")
        self.canvas.create_text(x, y, text=str(node.value), font=("Arial", 12, "bold"))

    def setup_prog_label(self):
        self.label_frame = Frame(self, bg = "#6e7bb2",
                                 bd = 8, relief = "solid")
        self.label_frame.place(relx=0.993, rely=0.01, width=450, height=60, anchor="ne")

        self.label_text = Label(self.label_frame, text="Binary Search Tree",
                                font=("Press Start 2P", 15, "bold"),
                                fg = "white",
                                bg="#6e7bb2")
        self.label_text.pack(padx=10, pady=10)

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

        self.tip_label = tk.Label(self,
                                text="", font=("Montserrat", 12),
                                bg="black",
                                fg="white")
        self.tip_label.place(relx=0.993, rely=0.152, width=330, anchor="ne")
        self.tip_label.config(text="Input must be minimum of 10, maximum of 30")

        self.error_label = Label(self, text="", font=("Press Start 2P", 13), fg="red", bg="#6e7bb2")
        self.error_label.place(relx=0.98, rely=0.109, anchor="ne")

        #self.number_count_display = Entry(self, font = ("Press Start 2P", 13), relief = "flat", bg="black")
        #self.number_count_display.place(relx= 0.886, rely= 0.195, width= 330, anchor = "center")

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
        
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image)

        self.draw_bst(root,780,170,400)

    def traversal_frame(self):
        self.traversal_container = tk.Frame(self, bg="#b3d9ff",
                                bd = 5, relief = "solid")
        self.traversal_container.place(relx=0.007, rely=0.99, width=1350, height=50, anchor="sw")

        self.traversal_label = tk.Label(self.traversal_container, text="Inorder:",
                                font=("Montserrat", 15, "bold"),
                                fg="black",
                                bg="#b3d9ff",
                                justify="left", anchor="w")
        self.traversal_label.pack(padx=2, pady=2, fill="both")

if __name__ == "__main__":
    app = TreeGUI()
    app.mainloop()