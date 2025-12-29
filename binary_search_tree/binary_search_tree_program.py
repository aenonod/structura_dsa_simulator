from tkinter import *
import tkinter as tk


#7
class Node:
    def __init__(self,value):
        self.value = value
        self.right = None
        self.left = None

#1 GUI
class BST(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Structura")
        self.attributes("-fullscreen", True)
        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False))


        self.display_background()
        self.display_get_user_input_frame()
        #17
        self.display_input_back_button()
        #5
        self.display_binary_search_tree()
        self.binary_search_tree_frame() 
        #17
        self.display_bst_back_button()
        
        #5
        self.bst_frame.place_forget()

#8
    def insert(self,root,value):
        if root is None:
            return Node(value)
        
        if value <= root.value:
            root.left = self.insert(root.left,value)
        else:
            root.right = self.insert(root.right,value)

        return root

#10
    def inorder(self,root,result):
        if root is None:
            return
        self.inorder(root.left, result)
        result.append(root.value)
        self.inorder(root.right,result)

#12
    def draw_bst(self,node,x,y,dx):
        if not node:
            return
        circle_radius = 25
        v_space = 65

        if node.left:
            next_dx_left = max(dx * 0.5, 30)
            self.display_canvas_bst.create_line(x, y, x - dx, y + v_space, fill="white", width=2)
            self.draw_bst(node.left, x - dx, y + v_space, next_dx_left)

        if node.right:
            next_dx_right = max(dx * 0.5, 30)
            self.display_canvas_bst.create_line(x, y, x + dx, y + v_space, fill="white", width=2)
            self.draw_bst(node.right, x + dx, y + v_space, next_dx_right)
        
        self.display_canvas_bst.create_oval(x-circle_radius, y-circle_radius, x+circle_radius, y+circle_radius, fill="#cab7d9")
        self.display_canvas_bst.create_text(x, y, text=str(node.value), font=("Arial", 12, "bold"))

#14
    def display_count(self):
        raw_count = self.entry_user.get()
        valid_numbers = []

        for count in raw_count.split(","):
            count = count.strip()

            if count != "":
                valid_numbers.append(int(count))
        
        total_count = len(valid_numbers)


        self.number_count_display.delete(0, END)
        self.number_count_display.insert(0, total_count)

#18
    def back_button(self):
         
        self.bst_frame.place_forget()
        self.input_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.binary_frame.place(relx=0.993, rely=0.01, width=450, height=60, anchor="ne")
#2
    def confirm_input(self):
        raw_number_value = self.entry_user.get()
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

            #6
            self.display_bg.itemconfigure(self.number_limit_text, state="hidden")
            self.input_frame.place_forget()
            self.binary_frame.place_forget()
            self.bst_frame.place(x= 0,y= 0)

            
            self.draw_bst(root,780, 200, 360)

        except:
            self.error_label.config(text="INVALID")
            return

    #11 (for checking only)
        result = []
        self.inorder(root,result)

        print(number_values)
        print("BST root value:", root.value)

        print("Inorder Traversal(LTR):")
        print(result)
            
#1
    def display_background(self):
        self.display_bg = Canvas(self, width=1920, height=1080, highlightthickness=0)
        self.display_bg.place(x=0, y=0)

        self.bg_image = PhotoImage(file="binary_search_tree/background.png")

        self.display_bg.create_image(0, 0, image=self.bg_image, anchor="nw")

#1
    def display_get_user_input_frame(self):
        self.input_frame = Frame(self, bg = "#a3afe0", width=1000, height=300, bd = 4, relief = "solid")
        self.input_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.number_label = Label(self.input_frame,text="Enter any random number:",font=("Press Start 2P", 20, "bold"), fg = "black",bg="#a3afe0")
        self.number_label.place(relx=0.5, rely=0.11, anchor="center")

        self.entry_user = Entry(self.input_frame, font=("Press Start 2P",20), bd= 4, relief = "solid", justify = "left")
        self.entry_user.place(relx=0.5, rely=0.35, anchor="center", width=900, height=60)
        self.entry_user.bind("<Key>", lambda event: self.error_label.config(text=""))
        self.entry_user.bind("<KeyRelease>", lambda e: self.display_count())
    #1
        self.button_confirm = Button(self.input_frame, text = "Confirm", font = ("Press Start 2P",20), fg = "white", bg = "#17357a", bd = 4, relief = "solid", command = self.confirm_input)
        self.button_confirm.place(relx=0.5, rely=0.85, anchor="center", width=400, height=60)

        self.number_limit_text = self.display_bg.create_text(765,int(1080 * 0.62), text="Input must be minimum of 10, maximum of 30",font=("Press Start 2P", 15, "bold"),fill="#fdacac")


    

#13 display the number count when inputting number
        self.number_count = Label(self.input_frame, text = "Number count:", font = ("Press Start 2P", 20), fg = "black",bg = "#a3afe0")
        self.number_count.place(relx= 0.223,rely= 0.55, anchor = "center")

        self.number_count_display = Entry(self.input_frame, font = ("Press Start 2P", 20), relief = "flat", bg="#a3afe0")
        self.number_count_display.place(relx= 0.49, rely= 0.55, width= 156, height= 52, anchor = "center")
        
#3
        self.error_label = Label(self.input_frame, text="", font=("Press Start 2P", 20), fg="red", bg="#a3afe0")
        self.error_label.place(relx=0.86, rely=0.55, anchor="center")

#1 
    def binary_search_tree_frame(self):
        self.binary_frame = Frame(self, bg = "#6e7bb2", bd = 8, relief = "solid")
        self.binary_frame.place(relx=0.993, rely=0.01, width=450, height=60, anchor="ne")

        self.label_binary_text = Label(self.binary_frame,text="Binary Search Tree",font=("Press Start 2P", 15, "bold"), fg = "white",bg="#6e7bb2")
        self.label_binary_text.pack(padx=10, pady=10)

    #16
    def display_input_back_button(self):
        self.input_back_button = Button(self, text = "Back",font = ("Press Start 2P", 15, "bold"), fg = "white", bg ="#17357a", bd = 4, relief = "solid",padx=10, pady=7)
        self.input_back_button.place(relx=0.994, rely=0.99, width=150, height=50, anchor="se")

    def display_bst_back_button(self):
        self.bst_back_button = Button(self, text = "Back",font = ("Press Start 2P", 15, "bold"), fg = "white", bg ="#17357a", bd = 4, relief = "solid",padx=10, pady=7, command = self.back_button)
        self.bst_back_button.place(relx=0.994, rely=0.99, width=150, height=50, anchor="se")
#4
    def display_binary_search_tree(self):
        self.bst_frame = Frame(self, width=1920, height=1080)
        self.bst_frame.place(x=0, y=0)

        self.display_canvas_bst = Canvas(self.bst_frame, width=1920, height=1080, highlightthickness=0)
        self.display_canvas_bst.place(x= 0, y= 0)
        
        self.display_canvas_bst.create_image(0, 0, image=self.bg_image, anchor="nw")

        self.bst_title_frame = Frame(self.display_canvas_bst, bg = "#6e7bb2", width=450, height=60, bd = 8, relief = "solid")
        
        self.bst_title = Label(self.bst_title_frame,text="Binary Search Tree",font=("Press Start 2P", 15, "bold"), fg = "white",bg="#6e7bb2")
        self.bst_title.pack(padx=25, pady=9)

        self.display_canvas_bst.create_window(1075, 10,anchor="nw",window = self.bst_title_frame)

if __name__ == "__main__":
    app = BST()
    app.mainloop()