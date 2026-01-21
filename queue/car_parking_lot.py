import tkinter as tk
from tkinter import ttk, font
from PIL import Image, ImageTk, ImageDraw, ImageFont

class Car:
    def __init__(self, car, canvas, x, stop_y):
        self.car = car
        self.canvas = canvas
        self.x = x
        self.y = -48
        self.speed = 8
        self.stop_y = stop_y
        self.image = self.create_car_image()
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.id = self.canvas.create_image(self.x, self.y, image=self.tk_image)

    def create_car_image(self):
        image = Image.new("RGBA", (48, 80), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        draw.rectangle([8, 0, 40, 72], fill="#17357A")

        draw.rectangle([12, 56, 36, 64], fill="#000000")
        draw.rectangle([12, 8, 36, 16], fill="#000000")

        draw.rectangle([10, 70, 14, 72], fill="#ffde59")
        draw.rectangle([34, 70, 38, 72], fill="#ffde59")
        draw.rectangle([10, 0, 14, 2], fill="#ffde59")
        draw.rectangle([34, 0, 38, 2], fill="#ffde59")

        try:
            font_path = "assets/PressStart2P-vaV7.ttf"
            font = ImageFont.truetype(font_path, 16)
        except OSError:
            font = ImageFont.load_default()

        draw.text((16, 36), self.car, font=font, fill="#ffffff")
        return image

    def move_in(self, callback=None):
        if self.y < self.stop_y:
            self.canvas.move(self.id, 0, self.speed)
            self.y += self.speed
            self.canvas.after(10, lambda: self.move_in(callback))
        else:
            self.canvas.coords(self.id, self.x, self.stop_y)
            if callback:
                callback()

class ParkingLot(tk.Frame):
    def __init__(self, root, master):
        super().__init__(master)
        self.root = root
        self.master = master

        try:
            self.font = "Press Start 2P"
        except OSError:
            self.font = "Arial"

        self.car_map = {}
        self.index_ids = {}

        self.cars = []
        self.arrivals = []
        self.departures = []

        self.is_animating = False

        self.setup_background()
        self.setup_parking_lot()
        self.setup_table()

    def setup_background(self):

        self.canvas = tk.Canvas(self.root, highlightthickness=0)
        self.canvas.place(x=0, y=0, relwidth=1, relheight=1)

        try:
            self.original_background = Image.open("assets/background.png")
            self.background = ImageTk.PhotoImage(self.original_background)
            self.background_id = self.canvas.create_image(0, 0, anchor="nw", image=self.background)

            def resize_background(width, height):
                if width < 1 or height < 1:
                    return
                resized_background = self.original_background.resize((width, height), Image.LANCZOS)
                self.background = ImageTk.PhotoImage(resized_background)
                self.canvas.itemconfig(self.background_id, image=self.background)
                self.canvas.coords(self.background_id, 0, 0)
        except:
            self.root.configure(bg="#808080")

        self.canvas.bind("<Configure>", lambda e: resize_background(e.width, e.height))

        information_frame = tk.Frame(self.root, bg="#000000", bd=8, relief="solid")
        information_frame.place(anchor="center", x=240, y=60, width=320, height=80)
        tk.Label(information_frame, text="Parking Lot", font=(self.font, 16), fg="#ffffff", bg="#000000").place(anchor="center", relx=0.5, rely=0.25)
        self.status_label = tk.Label(information_frame, text="Ready", fg="#6e7bb2", bg="#000000", font=(self.font, 8))
        self.status_label.place(anchor="center", relx=0.5, rely=0.75)

    def setup_parking_lot(self):

        self.parking_lot = tk.Canvas(self.root, width=320, height=648, bg="#6e7bb2", bd=8, relief="solid", highlightthickness=0)
        self.parking_lot.place(anchor="center", x=240, y=440)

    def setup_ui(self, title, park, unpark, back_command):

        title_frame = tk.Frame(self.root, bg="#6e7bb2", bd=8, relief="solid")
        title_frame.place(anchor="ne", relx=0.993, rely=0.01, width=400, height=60)

        tk.Label(title_frame, text=title, font=(self.font, 16), bg="#6e7bb2", fg="#ffffff").place(anchor="center", relx=0.5, rely=0.5)

        control_frame = tk.Frame(self.root, bg="#6e7bb2", bd=8, relief="solid")
        control_frame.place(anchor="center", x=768, y=632, width=480, height=240)

        tk.Label(control_frame, text="Enter Car:", font=(self.font, 16), bg="#6e7bb2", fg="#000000").place(anchor="center", relx=0.5, y=24)

        vcmd = (self.root.register(self.validate_input), "%P")
        self.text_box = tk.Entry(control_frame, validate="key", validatecommand=vcmd, font=(self.font, 16), width=1, bd=8, relief="solid")
        self.text_box.place(anchor="center", relx=0.5, y=72)

        tk.Button(self.root, text="Back", bg="#17357A", fg="#ffffff", font=(self.font, 15, "bold"), bd=8,command=self.go_back).place(anchor="se", relx=0.994, rely=0.99, width=150, height=50)
        tk.Button(control_frame, text="Park", bg="#17357A", fg="#ffffff", font=(self.font, 16), bd=8, relief="solid", command=park).place(anchor="center", relx=0.5, y=124, relwidth=0.4, height=50.4)
        tk.Button(control_frame, text="Unpark", bg="#17357A", fg="#ffffff", font=(self.font, 16), bd=8, relief="solid", command=unpark).place(anchor="center", relx=0.5, y=184, relwidth=0.4, height=50.4)
        tk.Button(self.root, text="Reset", bg="#17357A", fg="#ffffff", font=(self.font, 16), bd=8, relief="solid", command=self.reset).place(anchor="center", x=768, y=312, width=144, height=50.4)

    def validate_input(self, P):
        if len(P) <= 1:
            return True
        return False

    def reset(self):
        if self.is_animating:
            return

        for car in self.car_map.values():
            self.parking_lot.delete(car.id)
        for text_id in self.index_ids.values():
            self.parking_lot.delete(text_id)

        self.clear_list()
        self.car_map.clear()
        self.index_ids.clear()

        self.cars.clear()
        self.arrivals.clear()
        self.departures.clear()

        self.update_table()
        self.text_box.delete(0, tk.END)

    def font_metrics(self, family, size, property):
        text_font = font.Font(family=family, size=size)
        return text_font.metrics(property)

    def font_measure(self, family, size, text):
        text_font = font.Font(family=family, size=size)
        return text_font.measure(text)

    def setup_table(self):

        border_frame = tk.Frame(self.root, bd=8, relief="solid")
        border_frame.place(anchor="center", x=768, y=216, width=547, height=126)

        style = ttk.Style()
        style.configure("Treeview", font=(self.font, 16), rowheight=self.font_metrics(self.font, 16, "linespace"))
        style.configure("Treeview.Heading", font=(self.font, 8))

        columns = ("Car", "Number of Arrivals", "Number of Departures")
        self.tree = ttk.Treeview(border_frame, columns=columns, show="headings", height=4)

        for column in columns:

            self.tree.heading(column, text=column)
            self.tree.column(column, width=self.font_measure(self.font, 8, column) + 32, anchor="center")

        self.tree.place(anchor="center", relx=0.5, rely=0.5, relwidth=1, relheight=1)

    def update_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for i in range(len(self.cars)):
            self.tree.insert("", tk.END, values=[self.cars[i], self.arrivals[i], self.departures[i]])

    def update_status(self, message):
        self.status_label.config(text=message)

    def finish_animation(self):
        self.is_animating = False
        self.update_status("Ready")

    def go_back(self):
        self.master.show_frame(self.master.MainMenuFrame)