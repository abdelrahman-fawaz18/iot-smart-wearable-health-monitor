# Recovery audit

This repository was assembled from the legacy graduation-project folder in September 2026. The publication was treated as the reference for system scope; draft papers and later fall/sleep implementations were not used to inflate the device repository.

## Included

| Repository item | Legacy source | Reason |
| --- | --- | --- |
| Maintained collector | `Sensor Codes/RaspberryPi/DataCollectionTest_1_UPDATED.py` and related tests | Original integrated motion/temperature acquisition behavior |
| MPU9250 adapter settings | `Fall detection/HM` acquisition code | Matches the IMU specified by the device paper; clearly marked as later surviving code |
| Walking recordings | `Data Collection/*.csv` | Raw data shown in the device paper's results section |
| Temperature capture | `Data Collection/MLX test.csv` | Evidence of Node-RED/MLX90614 collection |
| Prototype photograph | Progress Report 04 | Original bench setup photograph |
| Node-RED screenshot | Progress Report 05 | Original flow editor evidence |
| Walking plot | Generated from the preserved CSV | Reproducible visualization, not copied from the paper |

## Preserved under `legacy`

Two team-authored scripts are kept without cleanup so the historical implementation remains inspectable:

- the integrated MPU6050 and MLX90614 CSV logger;
- the MPU6050, MLX90614, and SSD1306 bench display.

The maintained package replaces their global loops, fixed output name, repeated sensor reads, zero-padded smoothing buffer, and lack of shutdown handling.

## Excluded

- All paper PDFs and Word manuscripts
- Presentation files and full project reports
- Manufacturer datasheets and literature-review PDFs
- Downloaded Arduino and Raspberry Pi library archives
- Copied third-party repositories, nested `.git` directories, and build metadata
- RFID, sweat-sensor, and unrelated Arduino experiments
- Duplicate spreadsheets and ZIP archives of the CSV data
- Personal email screenshots and obsolete network addresses

## Not recovered

- PCB source files, Gerbers, schematics, and fabrication notes
- Mechanical enclosure or wristband CAD
- Final bill of materials and exact breakout-board revisions
- Node-RED flow JSON, dashboard source, and broker configuration
- Validated heart-rate and SpO2 algorithm or calibration data
- A complete integrated logger proven to run all three paper-specified sensors simultaneously
- Dependency lockfile or reproducible Raspberry Pi OS image

These gaps remain visible in the documentation. No placeholder artifact is presented as an original project file.
