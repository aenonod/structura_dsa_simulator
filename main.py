import tkinter as tk
from PIL import Image, ImageTk
from stack.car_parking_lot_stack import StackParkingLot
from queue.car_parking_lot_queue import QueueParkingLot
from binary_tree.binary_tree_gui import TreeGUI
from binary_search_tree.binary_search_tree_program import BinarySearchGUI
from recursion.recursion_program import TowerOfHanoi

class WelcomePageFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        # Canvas
        self.canvas = tk.Canvas(self, highlightthickness=0, bg="#1b3c8a")
        self.canvas.pack(fill="both", expand=True)

        # Background
        self.orig_bg = Image.open("assets/welcome_page.png")
        self.bg_img = ImageTk.PhotoImage(self.orig_bg)
        self.bg_id = self.canvas.create_image(0, 0, anchor="nw", image=self.bg_img)

        # Play button
        self.play_btn = tk.Button(
            self.canvas,
            text="PLAY",
            font=("Press Start 2P", 18, "bold"),
            fg="white",
            bg="#17357a",
            activebackground="#1f4bb3",
            relief="solid",
            bd=6,
            padx=10,
            pady=7,
            command=lambda: self.master.show_frame(MainMenuFrame))
        self.play_btn_id = self.canvas.create_window(0, 0, anchor="center", window=self.play_btn)

        # Bind resize and force redraw
        self.canvas.bind("<Configure>", lambda e: self.resize_bg(e.width, e.height))
        self.after(100, self.force_redraw)

    def resize_bg(self, width, height):
        if width < 1 or height < 1:
            return
        resized = self.orig_bg.resize((width, height), Image.LANCZOS)
        self.bg_img = ImageTk.PhotoImage(resized)
        self.canvas.itemconfig(self.bg_id, image=self.bg_img)
        self.canvas.coords(self.bg_id, 0, 0)
        self.canvas.coords(self.play_btn_id, width*0.5, height*0.64)

    def force_redraw(self):
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w > 1 and h > 1:
            self.resize_bg(w, h)


class MeetTheDevsFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        # Canvas
        self.canvas = tk.Canvas(self, highlightthickness=0, bg="#1b3c8a")
        self.canvas.pack(fill="both", expand=True)

        # Background
        self.orig_bg = Image.open("assets/devs_page.png")
        self.bg_img = ImageTk.PhotoImage(self.orig_bg)
        self.bg_id = self.canvas.create_image(0, 0, anchor="nw", image=self.bg_img)

        # Back button
        self.back_btn = tk.Button(
            self.canvas,
            text="BACK",
            width=15, height=1,
            font=("Press Start 2P", 15, "bold"),
            fg="white",
            bg="#17357a",
            activebackground="#1f4bb3",
            relief="raised",
            bd=6,
            command=lambda: self.master.show_frame(MainMenuFrame))
        self.back_btn_id = self.canvas.create_window(0, 0, anchor="center", window=self.back_btn)

        # Bind resize and force redraw
        self.canvas.bind("<Configure>", self.resize_bg)
        self.after(100, self.force_redraw)

    def resize_bg(self, event):
        if event.width < 1 or event.height < 1:
            return
        resized = self.orig_bg.resize((event.width, event.height), Image.LANCZOS)
        self.bg_img = ImageTk.PhotoImage(resized)
        self.canvas.itemconfig(self.bg_id, image=self.bg_img)
        self.canvas.coords(self.bg_id, 0, 0)
        self.canvas.coords(self.back_btn_id, event.width*0.15, event.height*0.92)

    def force_redraw(self):
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w > 1 and h > 1:
            self.resize_bg(tk.Event(width=w, height=h))
    

class MainMenuFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        # Canvas
        self.canvas = tk.Canvas(self, highlightthickness=0, bg="#1b3c8a")
        self.canvas.pack(fill="both", expand=True)

        # Background
        self.orig_bg = Image.open("assets/main_menu_page.png")
        self.bg_img = ImageTk.PhotoImage(self.orig_bg)
        self.bg_id = self.canvas.create_image(0, 0, anchor="nw", image=self.bg_img)

        # Buttons
        self.stack_btn = tk.Button(self.canvas, text="STACK", width=20, height=1, font=("Press Start 2P", 18, "bold"),
                                fg="white", bg="#6e7bb2", activebackground="#1f4bb3",
                                relief="solid", bd=6,
                                command=self.master.run_stack)
        self.stack_btn_id = self.canvas.create_window(0, 0, anchor="center", window=self.stack_btn)

        self.queue_btn = tk.Button(self.canvas, text="QUEUE", width=20, height=1, font=("Press Start 2P", 18, "bold"),
                                fg="white", bg="#6e7bb2", activebackground="#1f4bb3",
                                relief="solid", bd=6,
                                command=self.master.run_queue)
        self.queue_btn_id = self.canvas.create_window(0, 0, anchor="center", window=self.queue_btn)
        
        self.bt_btn = tk.Button(self.canvas, text="BINARY TREE", width=20, height=1, font=("Press Start 2P",18,"bold"),
                                fg="white", bg="#6e7bb2", activebackground="#1f4bb3",
                                relief="solid", bd=6,
                                command=self.master.run_bt)
        self.bt_btn_id = self.canvas.create_window(0, 0, anchor="center", window=self.bt_btn)

        self.bst_btn = tk.Button(self.canvas, text="BINARY SEARCH TREE", width=20, height=1, font=("Press Start 2P",18,"bold"),
                                fg="white", bg="#6e7bb2", activebackground="#1f4bb3",
                                relief="solid", bd=6,
                                command=self.master.run_bst)
        self.bst_btn_id = self.canvas.create_window(0, 0, anchor="center", window=self.bst_btn)

        self.recursion_btn = tk.Button(self.canvas, text="RECURSION", width=20, height=1, font=("Press Start 2P",18,"bold"),
                                fg="white", bg="#6e7bb2", activebackground="#1f4bb3",
                                relief="solid", bd=6,
                                command=self.master.run_recursion)
        self.recursion_btn_id = self.canvas.create_window(0, 0, anchor="center", window=self.recursion_btn)

        self.back_btn = tk.Button(self.canvas, text="BACK", width=15, height=1, font=("Press Start 2P",15,"bold"),
                                  fg="white", bg="#17357a", activebackground="#1f4bb3",
                                  relief="raised", bd=6,
                                  command=lambda: self.master.show_frame(WelcomePageFrame))
        self.back_btn_id = self.canvas.create_window(0, 0, anchor="center", window=self.back_btn)

        self.devs_btn = tk.Button(self.canvas, text="MEET THE DEVS", width=15, height=1, font=("Press Start 2P",15,"bold"),
                                  fg="white", bg="#17357a", activebackground="#1f4bb3",
                                  relief="raised", bd=6,
                                  command=lambda: self.master.show_frame(MeetTheDevsFrame))
        self.devs_btn_id = self.canvas.create_window(0, 0, anchor="center", window=self.devs_btn)

        # Bind resize and force redraw
        self.canvas.bind("<Configure>", lambda e: self.resize_bg(e.width, e.height))
        self.after(100, self.force_redraw)

    def resize_bg(self, width, height):
        if width < 1 or height < 1:
            return
        resized = self.orig_bg.resize((width, height), Image.LANCZOS)
        self.bg_img = ImageTk.PhotoImage(resized)
        self.canvas.itemconfig(self.bg_id, image=self.bg_img)
        self.canvas.coords(self.bg_id, 0, 0)
        # reposition buttons
        self.canvas.coords(self.stack_btn_id, width * 0.50, height * 0.50)
        self.canvas.coords(self.queue_btn_id, width * 0.50, height * 0.58)
        self.canvas.coords(self.bt_btn_id, width*0.5, height*0.66)
        self.canvas.coords(self.bst_btn_id, width * 0.50, height * 0.74)
        self.canvas.coords(self.recursion_btn_id, width * 0.50, height * 0.82)
        self.canvas.coords(self.back_btn_id, width*0.15, height*0.92)
        self.canvas.coords(self.devs_btn_id, width * 0.85, height * 0.92)

    def force_redraw(self):
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w > 1 and h > 1:
            self.resize_bg(w, h)


class ProgramGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Structura")
        self.attributes("-fullscreen", True)
        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", not self.attributes("-fullscreen")))
        self.current_frame = None
        self.show_frame(WelcomePageFrame)

        self.MainMenuFrame = MainMenuFrame

    def show_frame(self, frame_class):
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = frame_class(self)
        self.current_frame.pack(fill="both", expand=True)

    def run_stack(self):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = StackParkingLot(self)
        self.current_frame.pack(fill="both", expand=True)

    def run_queue(self):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = QueueParkingLot(self)
        self.current_frame.pack(fill="both", expand=True)

    def run_bt(self):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = TreeGUI(self)
        self.current_frame.pack(fill="both", expand=True)

    def run_bst(self):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = BinarySearchGUI(self)
        self.current_frame.pack(fill="both", expand=True)

    def run_recursion(self):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = TowerOfHanoi(self)
        self.current_frame.pack(fill="both", expand=True)


if __name__ == "__main__":
    app = ProgramGUI()
    app.mainloop()