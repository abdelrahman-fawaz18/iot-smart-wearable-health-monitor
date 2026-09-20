from __future__ import annotations

from dataclasses import dataclass, fields, replace
from datetime import datetime
from typing import Any

CSV_FIELDS = (
    "timestamp_utc",
    "accel_x_g",
    "accel_y_g",
    "accel_z_g",
    "gyro_x_dps",
    "gyro_y_dps",
    "gyro_z_dps",
    "mag_x_ut",
    "mag_y_ut",
    "mag_z_ut",
    "ambient_temp_c",
    "object_temp_c",
    "ppg_ir_raw",
    "ppg_red_raw",
)


@dataclass(frozen=True)
class MotionReading:
    accel_x_g: float
    accel_y_g: float
    accel_z_g: float
    gyro_x_dps: float
    gyro_y_dps: float
    gyro_z_dps: float
    mag_x_ut: float | None = None
    mag_y_ut: float | None = None
    mag_z_ut: float | None = None


@dataclass(frozen=True)
class TemperatureReading:
    ambient_temp_c: float
    object_temp_c: float


@dataclass(frozen=True)
class PulseOximeterReading:
    """Raw photoplethysmography channels from the MAX30100 FIFO."""

    ir_raw: int
    red_raw: int


@dataclass(frozen=True)
class DeviceSample:
    timestamp_utc: datetime
    accel_x_g: float
    accel_y_g: float
    accel_z_g: float
    gyro_x_dps: float
    gyro_y_dps: float
    gyro_z_dps: float
    mag_x_ut: float | None = None
    mag_y_ut: float | None = None
    mag_z_ut: float | None = None
    ambient_temp_c: float | None = None
    object_temp_c: float | None = None
    ppg_ir_raw: int | None = None
    ppg_red_raw: int | None = None

    def csv_row(self) -> dict[str, Any]:
        row = {field.name: getattr(self, field.name) for field in fields(self)}
        row["timestamp_utc"] = self.timestamp_utc.isoformat(timespec="milliseconds")
        return row

    def with_values(self, **values: float | int | None) -> DeviceSample:
        return replace(self, **values)
