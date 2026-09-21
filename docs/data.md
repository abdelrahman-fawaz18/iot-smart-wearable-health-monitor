# Data files

## Walking recordings

`data/recordings/walking` contains eight CSV recordings using the original project naming pattern:

```text
Gender-and-subject_Location_Activity_Type.csv
```

For example, `M01_L_Wlk_Mlt.csv` identifies subject `M01`, left-side placement, walking activity, and the `Mlt` acquisition type. `Sgl` and `Mlt` are project-specific acquisition labels.

| File | Samples | Recorded span |
| --- | ---: | ---: |
| `M01_L_Wlk_Mlt.csv` | 1,993 | 92.9 s |
| `M01_L_Wlk_Sgl.csv` | 559 | Crosses an hour boundary |
| `M02_L_Wlk_Mlt.csv` | 1,109 | 64.6 s |
| `M02_L_Wlk_Sgl.csv` | 465 | 265.0 s |
| `M03_L_Wlk_Mlt.csv` | 556 | 86.8 s |
| `M03_L_Wlk_Sgl.csv` | 619 | 35.1 s |
| `M04_L_Wlk_Mlt.csv` | 327 | 45.1 s |
| `M04_L_Wlk_Sgl.csv` | 651 | 98.6 s |

Each walking file contains the following columns:

| Column | Measurement |
| --- | --- |
| `Time` | Wall-clock fragment in `mm:ss.s` form |
| `Acc-X`, `Acc-Y`, `Acc-Z` | Acceleration axes in g |
| `Gyro-X`, `Gyro-Y`, `Gyro-Z` | Angular velocity axes in degrees per second |
| `Ambient Temp` | MLX90614 ambient temperature in degrees Celsius |

`M01_L_Wlk_Mlt.csv` is used for the repository overview figure because it provides the largest continuous recording: 1,993 samples over 92.9 seconds, with a maximum adjacent timestamp interval of 0.5 seconds.

## Temperature capture

`data/recordings/temperature/MLX_test.csv` contains the Node-RED MLX90614 export. Each line stores object and ambient temperature values in a JSON-like two-field CSV format.

## Collector output schema

The command-line collector writes explicit units and UTC timestamps:

```text
timestamp_utc,
accel_x_g,accel_y_g,accel_z_g,
gyro_x_dps,gyro_y_dps,gyro_z_dps,
mag_x_ut,mag_y_ut,mag_z_ut,
ambient_temp_c,object_temp_c,
ppg_ir_raw,ppg_red_raw
```

Columns for disabled sensors remain empty. Moving averages are calculated only from samples already observed.

## Timestamp notes

Subject identifiers are anonymous project codes. `M02_L_Wlk_Sgl.csv` contains a 195.9-second timestamp interval, and `M01_L_Wlk_Sgl.csv` crosses an hour boundary.
