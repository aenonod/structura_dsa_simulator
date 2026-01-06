import tkinter as tk
from tkinter import ttk, font
from PIL import Image, ImageTk, ImageDraw, ImageFont

class Car:
    def __init__(self, car, canvas, x, stop_y):
        self.car = car
        self.canvas = canvas
        self.x = x
        self.y = -60
        self.speed = 10
        self.stop_y = stop_y
        self.image = self.create_car_image()
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.id = self.canvas.create_image(self.x, self.y, image=self.tk_image)

    def create_car_image(self):
        image = Image.new("RGBA", (60, 100), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        draw.rectangle([10, 0, 50, 90], fill="#17357A")

        draw.rectangle([15, 70, 45, 80], fill="#000000")
        draw.rectangle([15, 10, 45, 20], fill="#000000")

        draw.rectangle([12.5, 87.5, 17.5, 90], fill="#ffde59")
        draw.rectangle([42.5, 87.5, 47.5, 90], fill="#ffde59")
        draw.rectangle([12.5, 0, 17.5, 2.5], fill="#ffde59")
        draw.rectangle([42.5, 0, 47.5, 2.5], fill="#ffde59")

        try:
            font_path = "assets/PressStart2P-vaV7.ttf"
            font = ImageFont.truetype(font_path, 20)
        except OSError:
            font = ImageFont.load_default()

        draw.text((20, 45), self.car, font=font, fill="#ffffff")
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

class ParkingLot:
    def __init__(self, root):

        self.root = root
        self.root.title("Structura: Parking Lot")
        self.root.geometry("1920x1080")

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

        try:
            background_image = tk.PhotoImage(file="assets/background.png")
            background_label = tk.Label(self.root, image=background_image)
            background_label.image = background_image
            background_label.place(x=0, y=0)
        except:
            self.root.configure(bg="#808080")

        information_frame = tk.Frame(self.root, bg="#000000", bd=10, relief="solid")
        information_frame.place(anchor="center", x=300, y=75, width=400, height=100)
        tk.Label(information_frame, text="Parking Lot", font=(self.font, 20), fg="#ffffff", bg="#000000").place(anchor="center", relx=0.5, rely=0.25)
        self.status_label = tk.Label(information_frame, text="Ready", fg="#6e7bb2", bg="#000000", font=(self.font, 10))
        self.status_label.place(anchor="center", relx=0.5, rely=0.75)

    def setup_parking_lot(self):

        self.parking_lot = tk.Canvas(self.root, width=400, height=810, bg="#6e7bb2", bd=10, relief="solid")
        self.parking_lot.place(anchor="center", x=300, y=550)

    def setup_ui(self, title, park, unpark):

        title_frame = tk.Frame(self.root, bg="#6e7bb2", bd=10, relief="solid")
        title_frame.place(anchor="center", x=1620, y=63, width=540, height=63)

        tk.Label(title_frame, text=title, font=(self.font, 20), bg="#6e7bb2", fg="#ffffff").place(anchor="center", relx=0.5, rely=0.5)

        control_frame = tk.Frame(self.root, bg="#6e7bb2", bd=10, relief="solid")
        control_frame.place(anchor="center", x=960, y=790, width=600, height=300)

        tk.Label(control_frame, text="Enter Car:", font=(self.font, 20), bg="#6e7bb2", fg="#000000").place(anchor="center", relx=0.5, y=30)

        vcmd = (self.root.register(self.validate_input), "%P")
        self.text_box = tk.Entry(control_frame, validate="key", validatecommand=vcmd, font=(self.font, 20), width=1, bd=10, relief="solid")
        self.text_box.place(anchor="center", relx=0.5, y=90)

        tk.Button(self.root, text="Back", bg="#17357A", fg="#ffffff", font=(self.font, 20), bd=10, relief="solid",command=lambda: None).place(anchor="center", x=1800, y=963, width=180, height=63)
        tk.Button(control_frame, text="Park", bg="#17357A", fg="#ffffff", font=(self.font, 20), bd=10, relief="solid", command=park).place(anchor="center", relx=0.5, y=155, relwidth=0.4, height=63)
        tk.Button(control_frame, text="Unpark", bg="#17357A", fg="#ffffff", font=(self.font, 20), bd=10, relief="solid", command=unpark).place(anchor="center", relx=0.5, y=230, relwidth=0.4, height=63)
        tk.Button(self.root, text="Reset", bg="#17357A", fg="#ffffff", font=(self.font, 20), bd=10, relief="solid", command=self.reset).place(anchor="center", x=960, y=390, width=180, height=63)

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

        border_frame = tk.Frame(self.root, bd=10, relief="solid")
        border_frame.place(anchor="center", x=960, y=270, width=653, height=154)

        style = ttk.Style()
        style.configure("Treeview", font=(self.font, 20), rowheight=self.font_metrics(self.font, 20, "linespace"))
        style.configure("Treeview.Heading", font=(self.font, 10))

        columns = ("Car", "Number of Arrivals", "Number of Departures")
        self.tree = ttk.Treeview(border_frame, columns=columns, show="headings", height=4)

        for column in columns:

            self.tree.heading(column, text=column)
            self.tree.column(column, width=self.font_measure(self.font, 10, column) + 40, anchor="center")

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