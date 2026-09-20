# Hardware and wiring

## Published configuration

The paper describes a three-layer wrist-worn prototype. The upper assembly contains the Raspberry Pi, motion sensor, custom interconnect board, and display. A lower board places the optical and temperature sensors against the inner wrist.

| Device | Function | I2C address |
| --- | --- | --- |
| MPU9250 | Acceleration, angular velocity, and magnetic field | `0x68` |
| MAX30100 | Red and infrared photoplethysmography | `0x57` |
| MLX90614 | Ambient and object temperature | `0x5A` |

The recovered bench prototype used an MPU6050 at `0x68`. It provides acceleration and angular velocity but no magnetometer. The archived walking recordings came from that six-axis configuration.

## Logical I2C connections

| Raspberry Pi signal | Header pin | Connected sensor signal |
| --- | ---: | --- |
| SDA1 / GPIO 2 | 3 | SDA |
| SCL1 / GPIO 3 | 5 | SCL |
| Ground | 6 | Ground |

Power depends on the exact breakout board. Check the board schematic before connecting VCC. A bare MAX30100 uses lower internal supply rails, while some modules add regulation and level shifting.

## Software backends

The command-line collector supports two motion backends:

- `mpu6050`: a small built-in register reader configured for +/-2 g and +/-250 degrees per second.
- `mpu9250`: an adapter for `mpu9250-jmdev`, configured to match the recovered later acquisition script: +/-8 g, +/-1000 degrees per second, 16-bit magnetometer output, and 100 Hz magnetometer mode.

MLX90614 readings are converted from the sensor's Kelvin register format to degrees Celsius. The MAX30100 backend records the FIFO's raw red and infrared values. It deliberately avoids presenting those values as BPM or SpO2.

## Missing construction artifacts

The legacy folder does not contain PCB CAD, schematics, Gerber files, an enclosure model, or a final bill of materials. The raster PCB layouts in the publication are useful evidence, but they are not sufficient to manufacture a board safely. This repository therefore documents the bus topology rather than presenting an unrecoverable board design as complete.
