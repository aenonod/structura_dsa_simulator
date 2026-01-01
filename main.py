import tkinter as tk
from PIL import Image, ImageTk


class ProgramGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Structura")
        self.attributes("-fullscreen", True)
        self.bind("<Escape>", self.toggle_fullscreen)

        self.canvas = tk.Canvas(self, highlightthickness=0, bg="#1b3c8a")
        self.canvas.pack(fill="both", expand=True)

        self.welcome_page()

        self.canvas.bind("<Configure>", self.on_canvas_resize)
        self.after(100, self.force_redraw)

    def on_canvas_resize(self, event):
        self.redraw(event.width, event.height)

    def toggle_fullscreen(self, event=None):
        self.attributes("-fullscreen", not self.attributes("-fullscreen"))
        self.after(100, self.force_redraw)

    def redraw(self, width, height):
        resized = self.orig_bg.resize((width, height), Image.LANCZOS)
        self.bg_img = ImageTk.PhotoImage(resized)
        self.canvas.itemconfig(self.bg_id, image=self.bg_img)
        self.canvas.coords(self.bg_id, 0, 0)

        self.canvas.coords(self.play_btn_id, width * 0.50, height * 0.64)

    def force_redraw(self):
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w > 1 and h > 1:
            self.redraw(w, h)

    def clear_page(self):
        self.canvas.delete("all")

    def welcome_page(self):
        self.clear_page()
        self.orig_bg = Image.open("assets/welcome_page.png")
        self.bg_img = None
        self.bg_id = self.canvas.create_image(0, 0, anchor="nw")
        self.create_play_button()
        self.force_redraw()

    def create_play_button(self):
        self.play_btn = tk.Button(self.canvas,
            text="PLAY",
            font=("Press Start 2P", 18, "bold"),
            fg="white",
            bg="#17357a",
            activebackground="#1f4bb3",
            relief="solid",
            bd=6,
            padx=10,
            pady=7,
            command=self.main_menu)

        self.play_btn.pack(ipadx=50, ipady=50)
        self.play_btn_id = self.canvas.create_window(0, 0, anchor="center", window=self.play_btn)


if __name__ == "__main__":
    app = ProgramGUI()
    app.mainloop()
