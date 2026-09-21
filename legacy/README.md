# Original project scripts

This directory contains two team-authored scripts from the 2021 prototype. Current data collection uses the package under `src/wearable_monitor`.

| File | Original purpose |
| --- | --- |
| `integrated_mpu6050_mlx90614_logger.py` | Read MPU6050 and MLX90614 values, apply a three-reading mean, and write `j.csv` |
| `oled_bench_display.py` | Show MPU6050 and MLX90614 readings on an SSD1306 OLED |

MAX30100 support in `src/wearable_monitor/hardware.py` records red and infrared FIFO values as raw PPG samples.

The `wearable-monitor` command runs the current data-acquisition pipeline.
