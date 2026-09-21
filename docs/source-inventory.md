# Source inventory

This repository consolidates the device-focused software, data, and technical figures from the original graduation-project folder. The published device paper defines the system scope; fall-detection and sleep-analysis implementations are maintained as separate projects.

## Included material

| Repository item | Project source | Purpose |
| --- | --- | --- |
| Maintained collector | `Sensor Codes/RaspberryPi/DataCollectionTest_1_UPDATED.py` and related tests | Integrated motion and temperature acquisition |
| MPU9250 adapter settings | `Fall detection/HM` acquisition code | IMU configuration specified by the device paper |
| Walking recordings | `Data Collection/*.csv` | Motion and temperature project data |
| Temperature capture | `Data Collection/MLX test.csv` | Node-RED and MLX90614 output |
| PCB and device figure | Published project figure supplied for the repository | Hardware design and wrist-mounted assembly |
| Node-RED screenshot | Progress Report 05 | Flow editor configuration |
| Walking plot | Generated from `M01_L_Wlk_Mlt.csv` | Reproducible project-data visualization |

## Original scripts

Two team-authored scripts are retained under `legacy/` with their original structure:

- the integrated MPU6050 and MLX90614 CSV logger;
- the MPU6050, MLX90614, and SSD1306 display script.

The maintained package separates sensor access, sampling, data models, and CSV output while preserving the original acquisition scope.

## Repository boundaries

The following material is intentionally excluded:

- paper PDFs, manuscripts, presentations, and full project reports;
- manufacturer datasheets and literature-review material;
- downloaded third-party libraries and nested repositories;
- build output, duplicate archives, and unrelated sensor experiments;
- personal screenshots and temporary network configuration.

PCB CAD, Gerber files, enclosure CAD, Node-RED flow JSON, a fabrication bill of materials, and processed heart-rate or SpO2 algorithms are not part of the source package.
