# Legacy source

This directory preserves selected team-authored scripts from the 2021 prototype. They are historical references, not the supported entry points.

| File | Original purpose |
| --- | --- |
| `integrated_mpu6050_mlx90614_logger.py` | Read MPU6050 and MLX90614 values, apply a three-reading mean, and write `j.csv` |
| `oled_bench_display.py` | Show MPU6050 and MLX90614 readings on an SSD1306 OLED |

The original MAX30100 register library was not copied here because its licensing information was incomplete. The associated experiment also treated scaled raw ADC values as BPM and SpO2, which is not a valid measurement method. The maintained package exposes those channels only as raw PPG samples.

Use `wearable-monitor` from the repository root for maintained collection code.
