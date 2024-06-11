import json
import warnings
import datetime

from django.db import models

from OctaveAssignment.mqtt import client, TOPIC, QOS


class OctaveBattery(models.Model):
    capacity = models.IntegerField()
    maximum_power = models.IntegerField()
    state_of_charge = models.FloatField(default=0.5)
    charging = models.BooleanField(default=False)
    cycles = models.FloatField(default=0)

    def get_capacity(self):
        return self.capacity

    def get_maximum_power(self):
        return self.maximum_power

    def get_state_of_charge(self):
        return self.state_of_charge

    def get_cycles(self):
        return self.cycles

    def get_charging(self):
        return self.charging

    def increase_battery_level(self, charging):
        if charging:
            self.state_of_charge = round(self.state_of_charge + 0.01, 2)

        else:
            self.state_of_charge = round(self.state_of_charge - 0.01, 2)
            self.cycles = round(self.cycles + 0.01, 2)
        self.save()
        if (charging and self.state_of_charge == 0.9) or (
            not charging and self.state_of_charge == 0.1
        ):
            warnings.warn(
                f"{str(datetime.datetime.now())}: Battery with id {self.id}: Battery level limit"
            )
            try:
                client.publish(
                    f"/{TOPIC}/{self.id}",
                    json.dumps(
                        {
                            "warning": "battery level limit",
                            "timestamp": str(datetime.datetime.now()),
                        }
                    ),
                    qos=QOS,
                )
            except Exception as e:
                warnings.warn(f"Could not publish warning to mqtt. Error: {e}")
