# import gui library 
import tkinter as tk
# import image processing library
from PIL import Image, ImageTk
# import time delay library                                                                                             
import time                                                                                                                 

# define class tower of hanoi
class TowerOfHanoi:
    def __init__(self, root):  
        # initialize main window                                                                                            
        self.root = root
        self.root.title("Tower of Hanoi") 
        # color of disk per size
        self.disk_colors = [
    "#FF595E",  # red
    "#FFCA3A",  # yellow
    "#8AC926",  # green
    "#1982C4",  # blue
    "#6A4C93",  # purple
    "#FF924C",  # orange
    "#4D96FF",  # sky blue
    "#2EC4B6",  # teal
    "#B5179E" ]  # pink

        self.is_running = False
        self.is_paused = False
        self.move_list = []
        self.move_index = 0

        # initialize number of disks and pegs                                                                                  
        self.num_disks = 0                                                                                                  
        self.pegs = [[], [], []]                                                                                            

        # create canvas with fixed dimensions
        self.canvas = tk.Canvas(root, width=800, height=600, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # load and display background image
        self.bg_img_orig = Image.open("assets/background.png")                                                                    
        self.bg_image = ImageTk.PhotoImage(self.bg_img_orig)                                                               
        self.bg_id = self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image)
        # title Banner
        self.title_bg = self.canvas.create_rectangle(0, 0, 0, 0, fill="#6e7bb2", outline="black", width=3)
        self.title_text = self.canvas.create_text(0, 0, text="Recursion – Tower of Hanoi", fill="white", font=("Press Start 2P", 8, "bold"))                   

        # bind window resize event
        self.canvas.bind("<Configure>", self.on_resize) 
                                                        
        # initialize move counter
        self.moves = 0                                                                                                     
        self.move_label = tk.Label(root, text="Moves: 0", font=("Press Start 2P", 14, "bold"), fg="white", bg= "#17357a")                              
        self.move_label.place(relx=0.5, rely=0.02, anchor="n")

        # create Start button
        self.start_button = tk.Button(self.canvas, text="Start Hanoi", font=("Press Start 2P", 16, "bold"), fg="white", bg= "#17357a", command=self.start_hanoi)              
                                                             
        self.start_button.place(relx=0.5, rely=0.95, anchor="center")
        self.pause_button = tk.Button(
        self.canvas, text="Pause", font=("Press Start 2P", 14, "bold"), command=self.toggle_pause, fg="white", bg= "#17357a")
        self.pause_button.place(relx=0.10, rely=.95, anchor="center")
        
        # create Back button
        self.back_button = tk.Button(self.canvas, text="Back", font=("Press Start 2P", 16, "bold"), fg="white", bg="#17357a", command=self.go_back)
        self.back_button.place(relx=0.9, rely=0.95, anchor="center")

        # create popup window for disk input
        self.create_popup()
    
    # reset function
    def reset_hanoi(self):
        self.is_running = False
        self.is_paused = False
        self.move_list = []
        self.move_index = 0

        self.moves = 0
        self.move_label.config(text="Moves: 0")

        self.pegs = [list(range(self.num_disks, 0, -1)), [], []]
        self.draw_disks()

    def generate_moves(self, n, from_peg, to_peg, aux_peg):
        if n == 1:
            self.move_list.append((from_peg, to_peg))
        else:
            self.generate_moves(n-1, from_peg, aux_peg, to_peg)
            self.move_list.append((from_peg, to_peg))
            self.generate_moves(n-1, aux_peg, to_peg, from_peg)

    def animate_moves(self):
        if not self.is_running or self.is_paused:
            return

        if self.move_index < len(self.move_list):
            from_peg, to_peg = self.move_list[self.move_index]
            self.move_disk(from_peg, to_peg)
            self.move_index += 1
            self.root.after(500, self.animate_moves)
        else:
            self.is_running = False

    # resize background image when window size changes
    def on_resize(self, event):                                                                                            
        width = event.width
        height = event.height
        bg_resized = self.bg_img_orig.resize((width, height), Image.Resampling.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(bg_resized)
        self.canvas.itemconfig(self.bg_id, image=self.bg_image)

        # redraw pegs and disks if disks are already set
        if self.num_disks > 0:
            self.draw_pegs()
            self.draw_disks()

        # position title at upper-right
        padding = 20
        box_width = 330
        box_height = 45

        x2 = event.width - padding
        y1 = padding
        x1 = x2 - box_width
        y2 = y1 + box_height

        self.canvas.coords(self.title_bg, x1, y1, x2, y2)
        self.canvas.coords(self.title_text, (x1 + x2) / 2, (y1 + y2) / 2)

        self.canvas.tag_raise(self.title_bg)
        self.canvas.tag_raise(self.title_text)

   # create popup window for disk input
    def create_popup(self):
        self.popup_frame = tk.Frame(self.canvas, bg="#a3afe0", bd=2, relief="ridge")
        self.popup_frame.place(relx=0.5, rely=0.5, anchor="center")

        # display prompt text
        tk.Label(self.popup_frame, text="Number of disks?", font=("Press Start 2P", 14, "bold"), bg="#a3afe0").pack(padx=15, pady=10)

        # input field for number of disks
        self.disk_entry = tk.Entry(self.popup_frame, width=5, font=("Press Start 2P", 14))
        self.disk_entry.pack(padx=10, pady=5)
        tk.Button(self.popup_frame, text="Set", font=("Press Start 2P", 14, "bold"), fg="white", bg= "#17357a", command=self.set_disks).pack(pady=10)

    # validate and set number of disks
    def set_disks(self):
        try:
            value = int(self.disk_entry.get())
            # check if input is within allowed range
            if 1 <= value <= 9:
                self.num_disks = value

                # initialize disks on the first peg
                self.pegs = [list(range(self.num_disks, 0, -1)), [], []]

                # hide popup and enable Start button
                self.popup_frame.place_forget()
                self.start_button.config(state="normal")
                
                # draw pegs and disks
                self.draw_pegs()
                self.draw_disks()
            else:
                # clear input if value is invalid
                self.disk_entry.delete(0, tk.END)
        except ValueError:
            # clear input if input is not a number
            self.disk_entry.delete(0, tk.END)

    # draw the three pegs
    def draw_pegs(self):
        self.canvas.delete("peg")
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        num_pegs = 3

        # calculate x-positions of pegs
        self.peg_x_positions = [width*(i+1)/(num_pegs+1) for i in range(num_pegs)]
        self.peg_height = height * 0.8
        self.peg_width = max(10, width//80)

        # draw vertical pegs and base
        for i in self.peg_x_positions:
            self.canvas.create_line(i, height*0.1, i, height*0.1 + self.peg_height, width=self.peg_width, fill='black', tags="peg")
            self.canvas.create_line(i - self.peg_width*5, height*0.1 + self.peg_height,
                                    i + self.peg_width*5, height*0.1 + self.peg_height, width=5, fill='black', tags="peg")
        self.canvas.tag_raise(self.title_bg)
        self.canvas.tag_raise(self.title_text)

    # draw all disks on the pegs
    def draw_disks(self):
        self.canvas.delete("disk")

        # exit if no disks are set
        if self.num_disks == 0:
            return
        height = self.canvas.winfo_height()
        width = self.canvas.winfo_width()
        # height of each disk
        disk_height = self.peg_height / (self.num_disks + 2)

        # disk width limits to avoid overlapping pegs
        spacing = min(self.peg_x_positions[1]-self.peg_x_positions[0], self.peg_x_positions[2]-self.peg_x_positions[1])
        max_disk_width = spacing * 0.6
        min_disk_width = max_disk_width * 0.4

        # draw disks for each peg
        for peg_idx, peg in enumerate(self.pegs):
            x = self.peg_x_positions[peg_idx]
            for disk_idx, disk_size in enumerate(peg):
                y = height*0.1 + self.peg_height - (disk_idx+1)*disk_height

                # scale disk width proportionally
                if self.num_disks == 1:
                    w = max_disk_width
                else:
                    w = min_disk_width + (disk_size - 1) / (self.num_disks - 1) * (max_disk_width - min_disk_width)
                color = self.disk_colors[disk_size - 1]
                self.canvas.create_rectangle(
                x - w/2, y, x + w/2, y + disk_height, fill=color, outline="black", width=2, tags="disk")

        # ensure background stays behind all objects
        self.canvas.tag_lower(self.bg_id)

    # move a single disk from one peg to another
    def move_disk(self, from_peg, to_peg):
        # remove disk from source peg
        if self.pegs[from_peg]:
            disk = self.pegs[from_peg].pop()
            # place disk on destination peg
            self.pegs[to_peg].append(disk)
            # update move counter   
            self.moves += 1
            self.move_label.config(text=f"Moves: {self.moves}")
            # redraw disks and update display
            self.draw_disks()
            self.root.update()  

    def wait_with_pause(self, seconds):
        interval = 0.05
        elapsed = 0
        while elapsed < seconds:
            if not self.is_paused:
                self.root.update()
                time.sleep(interval)
                elapsed += interval
            else:
                self.root.update()
                time.sleep(interval)

    # recursive Tower of Hanoi algorithm
    def hanoi_recursive(self, n, from_peg, to_peg, aux_peg):
        if not self.is_running:  
            return

        if n == 1:
            self.move_disk(from_peg, to_peg)
            self.wait_with_pause(0.5)  
        else:
            self.hanoi_recursive(n-1, from_peg, aux_peg, to_peg)
            self.move_disk(from_peg, to_peg)
            self.wait_with_pause(0.5)
            self.hanoi_recursive(n-1, aux_peg, to_peg, from_peg)

    # start the Tower of Hanoi process
    def start_hanoi(self):
        self.reset_hanoi()
        self.generate_moves(self.num_disks, 0, 2, 1)
        self.is_running = True
        self.animate_moves()

    def toggle_pause(self):
        if not self.is_running:
            return

        self.is_paused = not self.is_paused
        self.pause_button.config(
        text="Resume" if self.is_paused else "Pause")

        if not self.is_paused:
            self.animate_moves()

    # go back to disk input popup
    def go_back(self):
        self.is_running = False
        self.is_paused = False
        self.move_list = []
        self.move_index = 0
        self.moves = 0
        self.move_label.config(text="Moves: 0")
        self.pegs = [[], [], []]
        self.canvas.delete("peg")
        self.canvas.delete("disk")
        self.popup_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.start_button.config(state="disabled")

# main program
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    app = TowerOfHanoi(root)
    root.mainloop()