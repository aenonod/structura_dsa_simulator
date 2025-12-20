from tkinter import *

window = Tk()
window.geometry("1920x1080")
window.title("Structura")

bg_image = PhotoImage(file="binary_tree/background.png")

bg_label = Label(window, image=bg_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

window.mainloop()