"""Display MPU6050 and MLX90614 measurements on an SSD1306 OLED.

Raspberry Pi header connections: VCC pin 2, ground pin 6, SCL pin 5,
and SDA pin 3.
"""

from __future__ import annotations

import time

import Adafruit_SSD1306
from mlx90614 import MLX90614
from mpu6050 import mpu6050
from PIL import Image, ImageDraw, ImageFont
from smbus import SMBus


def main() -> int:
    bus = SMBus(1)
    temperature_sensor = MLX90614(bus, address=0x5A)
    motion_sensor = mpu6050(0x68)

    display = Adafruit_SSD1306.SSD1306_128_32(rst=None)
    display.begin()
    display.clear()
    display.display()

    image = Image.new("1", (display.width, display.height))
    drawing = ImageDraw.Draw(image)
    font = ImageFont.load_default()

    try:
        while True:
            acceleration = motion_sensor.get_accel_data()
            angular_velocity = motion_sensor.get_gyro_data()
            ambient_temperature = temperature_sensor.get_ambient()
            object_temperature = temperature_sensor.get_object_1()

            drawing.rectangle((0, 0, display.width, display.height), outline=0, fill=0)
            drawing.text(
                (0, -2), f"Ambient: {ambient_temperature:.2f}", font=font, fill=255
            )
            drawing.text((0, 6), f"Object:  {object_temperature:.2f}", font=font, fill=255)
            drawing.text(
                (0, 14),
                f"Acc: x{acceleration['x']:.1f} y{acceleration['y']:.1f} "
                f"z{acceleration['z']:.1f}",
                font=font,
                fill=255,
            )
            drawing.text(
                (0, 22),
                f"Gyr: x{angular_velocity['x']:.1f} y{angular_velocity['y']:.1f} "
                f"z{angular_velocity['z']:.1f}",
                font=font,
                fill=255,
            )

            display.image(image)
            display.display()
            print(
                f"acc=({acceleration['x']:+.3f}, {acceleration['y']:+.3f}, "
                f"{acceleration['z']:+.3f}) g  "
                f"gyro=({angular_velocity['x']:+.2f}, {angular_velocity['y']:+.2f}, "
                f"{angular_velocity['z']:+.2f}) dps  "
                f"ambient={ambient_temperature:.2f} C  object={object_temperature:.2f} C"
            )
            time.sleep(0.1)
    except KeyboardInterrupt:
        return 0
    finally:
        bus.close()


if __name__ == "__main__":
    raise SystemExit(main())
