"""Log MPU6050 motion and MLX90614 temperature measurements to CSV.

Raspberry Pi header connections: VCC pin 2, ground pin 6, SCL pin 5,
and SDA pin 3.
"""

from __future__ import annotations

import csv
import time
from datetime import datetime
from statistics import mean

from mlx90614 import MLX90614
from mpu6050 import mpu6050
from smbus import SMBus

OUTPUT_FILE = "j.csv"
FIELD_NAMES = (
    "Acc-X",
    "Acc-Y",
    "Acc-Z",
    "Gyro-X",
    "Gyro-Y",
    "Gyro-Z",
    "Ambient Temp",
    "Object Temp",
)


def main() -> int:
    bus = SMBus(1)
    temperature_sensor = MLX90614(bus, address=0x5A)
    motion_sensor = mpu6050(0x68)
    buffers = {name: [0.0, 0.0, 0.0] for name in FIELD_NAMES}

    try:
        with open(OUTPUT_FILE, mode="w", encoding="utf-8", newline="") as output:
            writer = csv.writer(output)
            writer.writerow(("Time", *FIELD_NAMES))

            while True:
                acceleration = motion_sensor.get_accel_data()
                angular_velocity = motion_sensor.get_gyro_data()
                ambient_temperature = temperature_sensor.get_ambient()
                object_temperature = temperature_sensor.get_object_1()

                readings = {
                    "Acc-X": acceleration["x"],
                    "Acc-Y": acceleration["y"],
                    "Acc-Z": acceleration["z"],
                    "Gyro-X": angular_velocity["x"],
                    "Gyro-Y": angular_velocity["y"],
                    "Gyro-Z": angular_velocity["z"],
                    "Ambient Temp": ambient_temperature,
                    "Object Temp": object_temperature,
                }

                averages = {}
                for name, value in readings.items():
                    buffers[name].pop(0)
                    buffers[name].append(value)
                    averages[name] = mean(buffers[name])

                writer.writerow((datetime.now(), *(averages[name] for name in FIELD_NAMES)))
                output.flush()

                print(
                    f"acc=({acceleration['x']:+.3f}, {acceleration['y']:+.3f}, "
                    f"{acceleration['z']:+.3f}) g  "
                    f"gyro=({angular_velocity['x']:+.2f}, {angular_velocity['y']:+.2f}, "
                    f"{angular_velocity['z']:+.2f}) dps  "
                    f"ambient={ambient_temperature:.2f} C  object={object_temperature:.2f} C"
                )
                time.sleep(0.02)
    except KeyboardInterrupt:
        return 0
    finally:
        bus.close()


if __name__ == "__main__":
    raise SystemExit(main())
