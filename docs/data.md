# Data files

## Walking recordings

`data/recordings/walking` contains eight recovered CSV recordings. The files use the original naming pattern described in the project presentation:

```text
Gender-and-subject_Location_Activity_Type.csv
```

For example, `M01_L_Wlk_Sgl.csv` identifies subject `M01`, left-side placement, walking activity, and the original `Sgl` acquisition type. The surviving notes do not define the `Sgl` and `Mlt` abbreviations beyond identifying them as the recording type, so this repository leaves them unchanged.

| File | Samples |
| --- | ---: |
| `M01_L_Wlk_Mlt.csv` | 1,993 |
| `M01_L_Wlk_Sgl.csv` | 559 |
| `M02_L_Wlk_Mlt.csv` | 1,109 |
| `M02_L_Wlk_Sgl.csv` | 465 |
| `M03_L_Wlk_Mlt.csv` | 556 |
| `M03_L_Wlk_Sgl.csv` | 619 |
| `M04_L_Wlk_Mlt.csv` | 327 |
| `M04_L_Wlk_Sgl.csv` | 651 |

Each file has the following columns:

| Column | Meaning |
| --- | --- |
| `Time` | Original wall-clock fragment in `mm:ss.s` form |
| `Acc-X`, `Acc-Y`, `Acc-Z` | Acceleration axes in g |
| `Gyro-X`, `Gyro-Y`, `Gyro-Z` | Angular velocity axes in degrees per second |
| `Ambient Temp` | MLX90614 ambient temperature in degrees Celsius |

## Temperature capture

`data/recordings/temperature/MLX_test.csv` is the recovered Node-RED temperature export. Each line contains object and ambient temperature values, but the original flow wrote a JSON-like payload into two CSV fields without a header. It is preserved as evidence rather than normalized in place.

## Current collector schema

New recordings use explicit units and UTC timestamps:

```text
timestamp_utc,
accel_x_g,accel_y_g,accel_z_g,
gyro_x_dps,gyro_y_dps,gyro_z_dps,
mag_x_ut,mag_y_ut,mag_z_ut,
ambient_temp_c,object_temp_c,
ppg_ir_raw,ppg_red_raw
```

Sensors that are not enabled produce empty cells. The collector averages only samples already observed. This removes the artificial low-temperature startup values caused by the original three-sample buffers being initialized with zeros.

## Limits on interpretation

The recordings contain anonymized subject codes and sensor values, not clinical records. The original sampling clock, calibration procedure, sensor placement protocol, and subject metadata were not preserved. These files support software demonstrations and historical analysis, but they do not form a validated biomedical dataset.

Some recordings contain discontinuous wall-clock segments. The generated figure leaves those intervals blank rather than drawing lines across periods with no samples.
