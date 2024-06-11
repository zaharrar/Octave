from OctaveAssignment.apps import MyAppConfig


class BatteryController:
    def __init__(self, battery):
        self.battery = battery

    def charge(self, power):
        real_power = min(
            abs(power), self.battery.get_maximum_power()
        )  # The power cannot exceed the maximum power
        self.run_charging_cycle(real_power, power >= 0)

    def run_charging_cycle(self, power, charging):
        steps = 3600 / ((power / self.battery.get_capacity()) * 100)
        MyAppConfig.task_queue.put((self.battery, steps, charging))
