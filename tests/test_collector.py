from datetime import datetime, timezone

import pytest

from wearable_monitor.collector import Sampler
from wearable_monitor.models import MotionReading, PulseOximeterReading, TemperatureReading


class SequenceMotionSensor:
    def __init__(self) -> None:
        self.value = 0.0

    def read(self) -> MotionReading:
        self.value += 1.0
        return MotionReading(
            self.value,
            self.value + 1,
            self.value + 2,
            self.value + 3,
            self.value + 4,
            self.value + 5,
        )


class FixedTemperatureSensor:
    def read(self) -> TemperatureReading:
        return TemperatureReading(ambient_temp_c=24.5, object_temp_c=33.0)


class FixedPulseOximeter:
    def read(self) -> PulseOximeterReading:
        return PulseOximeterReading(ir_raw=12_000, red_raw=8_000)


def test_average_uses_only_samples_collected_so_far() -> None:
    timestamp = datetime(2021, 6, 1, tzinfo=timezone.utc)
    sampler = Sampler(
        SequenceMotionSensor(),
        FixedTemperatureSensor(),
        FixedPulseOximeter(),
        average_window=3,
        clock=lambda: timestamp,
    )

    first = sampler.read()
    second = sampler.read()

    assert first.accel_x_g == 1.0
    assert first.ambient_temp_c == 24.5
    assert second.accel_x_g == pytest.approx(1.5)
    assert second.ppg_ir_raw == 12_000


def test_invalid_average_window_is_rejected() -> None:
    with pytest.raises(ValueError, match="average_window"):
        Sampler(SequenceMotionSensor(), average_window=0)
