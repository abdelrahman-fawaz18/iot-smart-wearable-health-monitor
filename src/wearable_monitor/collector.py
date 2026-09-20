from __future__ import annotations

import csv
import time
from collections import defaultdict, deque
from collections.abc import Callable
from contextlib import AbstractContextManager
from dataclasses import fields
from datetime import datetime, timezone
from pathlib import Path
from typing import TextIO

from wearable_monitor.models import CSV_FIELDS, DeviceSample
from wearable_monitor.sensors import MotionSensor, PulseOximeter, TemperatureSensor


class Sampler:
    def __init__(
        self,
        motion_sensor: MotionSensor,
        temperature_sensor: TemperatureSensor | None = None,
        pulse_oximeter: PulseOximeter | None = None,
        average_window: int = 1,
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        if average_window < 1:
            raise ValueError("average_window must be at least 1")
        self.motion_sensor = motion_sensor
        self.temperature_sensor = temperature_sensor
        self.pulse_oximeter = pulse_oximeter
        self.average_window = average_window
        self.clock = clock or (lambda: datetime.now(timezone.utc))
        self._history: dict[str, deque[float]] = defaultdict(
            lambda: deque(maxlen=self.average_window)
        )

    def read(self) -> DeviceSample:
        motion = self.motion_sensor.read()
        temperature = self.temperature_sensor.read() if self.temperature_sensor else None
        ppg = self.pulse_oximeter.read() if self.pulse_oximeter else None

        sample = DeviceSample(
            timestamp_utc=self.clock(),
            accel_x_g=motion.accel_x_g,
            accel_y_g=motion.accel_y_g,
            accel_z_g=motion.accel_z_g,
            gyro_x_dps=motion.gyro_x_dps,
            gyro_y_dps=motion.gyro_y_dps,
            gyro_z_dps=motion.gyro_z_dps,
            mag_x_ut=motion.mag_x_ut,
            mag_y_ut=motion.mag_y_ut,
            mag_z_ut=motion.mag_z_ut,
            ambient_temp_c=temperature.ambient_temp_c if temperature else None,
            object_temp_c=temperature.object_temp_c if temperature else None,
            ppg_ir_raw=ppg.ir_raw if ppg else None,
            ppg_red_raw=ppg.red_raw if ppg else None,
        )
        return self._average(sample) if self.average_window > 1 else sample

    def _average(self, sample: DeviceSample) -> DeviceSample:
        updates: dict[str, float | int | None] = {}
        for field in fields(sample):
            if field.name == "timestamp_utc":
                continue
            value = getattr(sample, field.name)
            if value is None:
                updates[field.name] = None
                continue
            values = self._history[field.name]
            values.append(float(value))
            mean = sum(values) / len(values)
            updates[field.name] = round(mean) if field.name.endswith("_raw") else mean
        return sample.with_values(**updates)


class CsvSink(AbstractContextManager["CsvSink"]):
    def __init__(self, path: str | Path, flush_every: int = 10) -> None:
        if flush_every < 1:
            raise ValueError("flush_every must be at least 1")
        self.path = Path(path)
        self.flush_every = flush_every
        self._stream: TextIO | None = None
        self._writer: csv.DictWriter[str] | None = None
        self._rows_since_flush = 0

    def __enter__(self) -> CsvSink:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._stream = self.path.open("w", encoding="utf-8", newline="")
        self._writer = csv.DictWriter(self._stream, fieldnames=CSV_FIELDS)
        self._writer.writeheader()
        return self

    def write(self, sample: DeviceSample) -> None:
        if not self._writer or not self._stream:
            raise RuntimeError("CsvSink must be opened with a with statement")
        self._writer.writerow(sample.csv_row())
        self._rows_since_flush += 1
        if self._rows_since_flush >= self.flush_every:
            self._stream.flush()
            self._rows_since_flush = 0

    def __exit__(self, *args: object) -> None:
        if self._stream:
            self._stream.close()
        self._stream = None
        self._writer = None


class Collector:
    def __init__(
        self,
        sampler: Sampler,
        sink: CsvSink,
        interval_seconds: float,
        print_samples: bool = True,
    ) -> None:
        if interval_seconds <= 0:
            raise ValueError("interval_seconds must be positive")
        self.sampler = sampler
        self.sink = sink
        self.interval_seconds = interval_seconds
        self.print_samples = print_samples

    def run(self, limit: int | None = None) -> int:
        count = 0
        next_sample_at = time.monotonic()
        while limit is None or count < limit:
            sample = self.sampler.read()
            self.sink.write(sample)
            if self.print_samples:
                print(format_sample(sample))
            count += 1
            next_sample_at += self.interval_seconds
            delay = next_sample_at - time.monotonic()
            if delay > 0:
                time.sleep(delay)
        return count


def format_sample(sample: DeviceSample) -> str:
    motion = (
        f"acc=({sample.accel_x_g:+.3f}, {sample.accel_y_g:+.3f}, "
        f"{sample.accel_z_g:+.3f}) g  "
        f"gyro=({sample.gyro_x_dps:+.2f}, {sample.gyro_y_dps:+.2f}, "
        f"{sample.gyro_z_dps:+.2f}) dps"
    )
    extras: list[str] = []
    if sample.object_temp_c is not None:
        extras.append(f"object={sample.object_temp_c:.2f} C")
    if sample.ppg_ir_raw is not None:
        extras.append(f"ppg_ir={sample.ppg_ir_raw}")
    return "  ".join([sample.timestamp_utc.isoformat(timespec="seconds"), motion, *extras])
