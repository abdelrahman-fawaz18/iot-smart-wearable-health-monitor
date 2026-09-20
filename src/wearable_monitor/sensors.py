from __future__ import annotations

from typing import Protocol

from wearable_monitor.models import MotionReading, PulseOximeterReading, TemperatureReading


class MotionSensor(Protocol):
    def read(self) -> MotionReading: ...


class TemperatureSensor(Protocol):
    def read(self) -> TemperatureReading: ...


class PulseOximeter(Protocol):
    def read(self) -> PulseOximeterReading: ...


class SMBusLike(Protocol):
    def read_byte_data(self, address: int, register: int) -> int: ...

    def write_byte_data(self, address: int, register: int, value: int) -> None: ...

    def read_word_data(self, address: int, register: int) -> int: ...

    def read_i2c_block_data(self, address: int, register: int, length: int) -> list[int]: ...

    def close(self) -> None: ...
