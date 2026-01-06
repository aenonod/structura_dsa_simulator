import tkinter as tk
from tkinter import messagebox
from car_parking_lot import Car, ParkingLot

class StackCar(Car):
    def __init__(self, car, canvas, x, stop_y):
        super().__init__(car, canvas, x, stop_y)

    def move_out(self, callback=None):
        if self.y > -60:
            self.canvas.move(self.id, 0, -self.speed)
            self.y -= self.speed
            self.canvas.after(10, lambda: self.move_out(callback))
        else:
            if callback:
                callback()

class StackParkingLot(ParkingLot):
    def __init__(self, root):
        super().__init__(root)

        self.stack = []
        self.temporary_stack = []

        self.setup_ui("Stack", self.push, self.pop)
        self.create_stack_parking_lot_lines()

    def create_stack_parking_lot_lines(self):
        cx = 200
        top = 190
        bottom = 620

        gap = 80

        x_left = cx - gap // 2
        x_right = cx + gap // 2

        self.parking_lot.create_line(x_left, top, x_left, bottom, fill="#ffffff", width=10)
        self.parking_lot.create_line(x_right, top, x_right, bottom, fill="#ffffff", width=10)

        y = 620

        line_length = 45

        x1_left = cx - line_length
        x2_left = cx

        x1_right = cx
        x2_right = cx + line_length

        self.parking_lot.create_line(x1_left, y, x2_left, y, fill="#ffffff", width=10)
        self.parking_lot.create_line(x1_right, y, x2_right, y, fill="#ffffff", width=10)

    def clear_list(self):
        self.stack.clear()

    def push(self):
        if self.is_animating: return

        car = self.text_box.get().upper()
        if not car: return
        if len(self.stack) == 4:
            messagebox.showwarning("Error", "Parking Garage is full!")
            return
        if car in self.stack:
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

    def spawn_car(self, car, is_refill=False):
        current_index = len(self.stack)
        target_y = 560 - (current_index * 100)

        new_car = StackCar(car, self.parking_lot, x=200, stop_y=target_y)
        self.stack.append(car)
        self.car_map[car] = new_car

        if is_refill:
            next_step = self.reparking_sequence
        else:
            self.update_status(f"Parking {self.text_box.get().upper()}...")
            next_step = self.finish_animation

        def on_parked_wrapper():
            text_id = self.parking_lot.create_text(80, target_y, text=str(current_index), font=(self.font, 20), fill="#000000")
            self.index_ids[car] = text_id

            next_step()

        new_car.move_in(callback=on_parked_wrapper)

    def pop(self):
        if self.is_animating: return

        car = self.text_box.get().upper()
        if not car: return
        if car not in self.stack:
            messagebox.showerror("Error", "Car not parked yet!")
            return

        self.temporary_stack = []

        self.unparking_sequence(car)

        self.is_animating = True
        self.text_box.delete(0, tk.END)

    def unparking_sequence(self, target_car):
        last_car = self.stack[-1]

        if last_car == target_car:
            self.unpark_car(target_car)
        else:
            self.update_status(f"Unparking {last_car}...")

            popped_car = self.stack.pop()
            self.temporary_stack.append(popped_car)

            if popped_car in self.index_ids:
                self.parking_lot.delete(self.index_ids[popped_car])
                del self.index_ids[popped_car]

            idx = self.cars.index(popped_car)
            self.departures[idx] += 1
            self.update_table()

            car_object = self.car_map.pop(popped_car)

            car_object.move_out(callback=lambda: self.cleanup_car_and_unparking_sequence(car_object, target_car))

    def cleanup_car_and_unparking_sequence(self, car_object, target_car):
        self.parking_lot.delete(car_object.id)
        self.unparking_sequence(target_car)

    def unpark_car(self, target_car):
        self.update_status(f"Unparking {target_car}...")

        self.stack.pop()

        if target_car in self.index_ids:
            self.parking_lot.delete(self.index_ids[target_car])
            del self.index_ids[target_car]

        idx = self.cars.index(target_car)
        self.departures[idx] += 1
        self.update_table()

        car_object = self.car_map.pop(target_car)

        car_object.move_out(callback=lambda: self.cleanup_and_reparking_sequence(car_object))

    def cleanup_and_reparking_sequence(self, car_object):
        self.parking_lot.delete(car_object.id)
        self.reparking_sequence()

    def reparking_sequence(self):
        if not self.temporary_stack:
            self.finish_animation()
            return

        car_to_re_park = self.temporary_stack.pop()
        self.update_status(f"Re-parking {car_to_re_park}...")

        idx = self.cars.index(car_to_re_park)
        self.arrivals[idx] += 1
        self.update_table()

        self.spawn_car(car_to_re_park, is_refill=True)