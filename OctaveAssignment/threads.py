import queue
import threading
import time


class ChargingThread(threading.Thread):
    def __init__(self, battery, steps, charging):
        super().__init__()
        self.battery = battery
        self.steps = steps
        self.charging = charging
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def run(self):
        print(f"Start charging battery with id {self.battery.id}")
        threshold = 1 if self.charging else 0
        while self.battery.get_state_of_charge() != threshold:
            time.sleep(self.steps)
            if self._stop_event.is_set():
                break
            self.battery.increase_battery_level(self.charging)
            print(f"Battery {self.battery.id} now {self.battery.get_state_of_charge()}")
        print(f"Charging stopped at {self.battery.get_state_of_charge()}")
        if not self.charging:
            print(f"Cycles at {self.battery.get_cycles()}")


class ManagerThread(threading.Thread):
    def __init__(self, task_queue):
        super().__init__()
        self.task_queue = task_queue
        self.daemon = True  # Ensure this thread exits when the main program does
        self.charging_batteries = {}

    def run(self):
        while True:
            try:
                task = self.task_queue.get(timeout=1)  # Wait for a task
                if task is None:
                    break  # Exit if a None task is received

                battery, steps, charging = task
                if battery.id in self.charging_batteries:
                    self.charging_batteries[battery.id].stop()
                worker = ChargingThread(battery, steps, charging)
                self.charging_batteries[battery.id] = worker
                worker.start()
                self.task_queue.task_done()
            except queue.Empty:
                continue  # No task, continue looping
