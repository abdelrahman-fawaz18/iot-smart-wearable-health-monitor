# Hardware and wiring

## Device configuration

The wrist-worn prototype uses a Raspberry Pi Zero W with three sensing modules on a shared I2C bus. The upper assembly contains the Raspberry Pi, motion sensor, interconnect board, and display. The optical and infrared temperature sensors are positioned toward the inner wrist.

![Two-layer PCB layout and wrist-mounted device](assets/device-and-pcb.png)

| Device | Function | I2C address |
| --- | --- | --- |
| MPU9250 | Acceleration, angular velocity, and magnetic field | `0x68` |
| MAX30100 | Red and infrared photoplethysmography | `0x57` |
| MLX90614 | Ambient and object temperature | `0x5A` |

The project recordings also use an MPU6050 at `0x68`. This configuration provides acceleration and angular velocity without a magnetometer.

## Logical I2C connections

| Raspberry Pi signal | Header pin | Sensor signal |
| --- | ---: | --- |
| SDA1 / GPIO 2 | 3 | SDA |
| SCL1 / GPIO 3 | 5 | SCL |
| Ground | 6 | Ground |

The supply voltage depends on the exact breakout board. Raspberry Pi GPIO uses 3.3 V logic and is not 5 V tolerant.

## Software backends

The command-line collector provides two motion backends:

- `mpu6050`: register-level reader configured for +/-2 g acceleration and +/-250 degrees per second angular velocity.
- `mpu9250`: `mpu9250-jmdev` adapter configured for +/-8 g acceleration, +/-1000 degrees per second angular velocity, 16-bit magnetometer output, and 100 Hz magnetometer mode.

MLX90614 readings are converted from the sensor's Kelvin register format to degrees Celsius. The MAX30100 backend stores the FIFO's raw red and infrared samples.

## PCB layout

The two-layer interconnect board measures 65 mm by 30 mm. The upper and lower copper layouts route the Raspberry Pi header to the MPU, MLX90614, and MAX30100 connections.
