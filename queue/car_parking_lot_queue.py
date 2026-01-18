import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from .car_parking_lot import Car, ParkingLot

class QueueCar(Car):
    def __init__(self, car, canvas, x, stop_y):
        super().__init__(car, canvas, x, stop_y)

    def shift_position(self, new_stop_y, callback=None):
        self.stop_y = new_stop_y

        if self.y < self.stop_y:
            self.canvas.move(self.id, 0, self.speed)
            self.y += self.speed
            self.canvas.after(10, lambda: self.shift_position(new_stop_y, callback))
        else:
            self.canvas.coords(self.id, self.x, self.stop_y)
            if callback:
                callback()

    def move_out(self, callback=None):
        if self.y < 720:
            self.canvas.move(self.id, 0, self.speed)
            self.y += self.speed
            self.canvas.after(10, lambda: self.move_out(callback))
        else:
            if callback:
                callback()


class QueueParkingLot(tk.Frame, ParkingLot):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        ParkingLot.__init__(self, self, master)

        self.queue = []

        self.setup_ui("Queue", self.enqueue, self.dequeue, self.go_back)
        self.create_queue_parking_lot_lines()

    def create_queue_parking_lot_lines(self):
        cx = 160
        top = 152
        bottom = 496

        gap = 64

        x_left = cx - gap // 2
        x_right = cx + gap // 2

        self.parking_lot.create_line(x_left, top, x_left, bottom, fill="#ffffff", width=8)
        self.parking_lot.create_line(x_right, top, x_right, bottom, fill="#ffffff", width=8)

    def clear_list(self):
        self.queue.clear()

    def enqueue(self):
        if self.is_animating: return
        car = self.text_box.get().upper()
        if not car: return
        if len(self.queue) == 4:
            messagebox.showwarning("Error", "Parking Garage is full!")
            return
        if car in self.queue:
            messagebox.showwarning("Error", "Car already parked!")
            return

        if car not in self.cars:
            self.cars.append(car)
            self.arrivals.append(0)
            self.departures.append(0)

        self.arrivals[self.cars.index(car)] += 1
        self.update_table()
        self.spawn_car(car, is_refill=False)
        self.is_animating = True
        self.text_box.delete(0, tk.END)

    def spawn_car(self, car, is_refill=False, on_complete=None):
        target_y = 448 - (len(self.queue) * 80)

        new_car = QueueCar(car, self.parking_lot, x=160, stop_y=target_y)
        self.queue.append(car)
        self.car_map[car] = new_car

        def after_park():
            try:
                idx = self.queue.index(car)
                text_id = self.parking_lot.create_text(64, target_y, text=str(idx), font=(self.font, 16), fill="#000000")
                self.index_ids[car] = text_id
            except ValueError:
                pass

            if on_complete:
                on_complete()
            elif not is_refill:
                self.finish_animation()

        if not is_refill:
            self.update_status(f"Parking {car}...")

        new_car.move_in(callback=after_park)

    def dequeue(self):
        if self.is_animating: return

        car = self.text_box.get().upper()
        if not car: return
        if car not in self.queue:
            messagebox.showerror("Error", "Car not parked yet!")
            return

        self.is_animating = True
        self.text_box.delete(0, tk.END)

        self.process_departure_cycle(car)

    def process_departure_cycle(self, target_car):
        first_car = self.queue[0]

        if first_car == target_car:
            self.unpark_car(target_car)
        else:
            self.unpark_blocker_cars(first_car, target_car)

    def unpark_car(self, target_car):
        self.update_status(f"Unparking {target_car}...")

        self.queue.pop(0)

        if target_car in self.index_ids:
            self.parking_lot.delete(self.index_ids[target_car])
            del self.index_ids[target_car]

        idx = self.cars.index(target_car)
        self.departures[idx] += 1
        self.update_table()

        car_object = self.car_map.pop(target_car)

        self.shift_remaining_cars()

        def on_exit_complete():
            self.cleanup_car(car_object)
            self.finish_animation()

        car_object.move_out(callback=on_exit_complete)

    def unpark_blocker_cars(self, blocker_car, target_car):
        self.update_status(f"Unparking {blocker_car}...")

        self.queue.pop(0)

        if blocker_car in self.index_ids:
            self.parking_lot.delete(self.index_ids[blocker_car])
            del self.index_ids[blocker_car]

        idx = self.cars.index(blocker_car)
        self.departures[idx] += 1
        self.update_table()

        car_object = self.car_map[blocker_car]
        del self.car_map[blocker_car]

        self.shift_remaining_cars()

        def on_departure_complete():
            self.cleanup_car(car_object)
            self.repark_blocker_cars(blocker_car, target_car)

        car_object.move_out(callback=on_departure_complete)

    def shift_remaining_cars(self, on_complete=None):
        if not self.queue:
            if on_complete: on_complete()
            return

        for car in self.queue:
            if car in self.index_ids:
                self.parking_lot.delete(self.index_ids[car])
                del self.index_ids[car]

        cars_moving_count = len(self.queue)

        def check_all_done():
            nonlocal cars_moving_count
            cars_moving_count -= 1

            if cars_moving_count <= 0:
                for i, car in enumerate(self.queue):
                    target_y = 448 - (i * 80)
                    text_id = self.parking_lot.create_text(64, target_y, text=str(i), font=(self.font, 16),
                                                           fill="#000000")
                    self.index_ids[car] = text_id

                if on_complete: on_complete()

        for i, car in enumerate(self.queue):
            car_obj = self.car_map[car]
            correct_y = 448 - (i * 80)
            car_obj.shift_position(correct_y, callback=check_all_done)

    def repark_blocker_cars(self, blocker_car, target_car):
        self.update_status(f"Re-parking {blocker_car}...")

        idx = self.cars.index(blocker_car)
        self.arrivals[idx] += 1
        self.update_table()

        self.spawn_car(blocker_car, is_refill=True, on_complete=lambda: self.process_departure_cycle(target_car))

    def cleanup_car(self, car_object):
        self.parking_lot.delete(car_object.id)