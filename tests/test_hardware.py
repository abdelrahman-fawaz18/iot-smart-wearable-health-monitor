import pytest

from wearable_monitor.hardware import Max30100RawSensor, Mlx90614Sensor, Mpu6050Sensor


class FakeBus:
    def __init__(self) -> None:
        self.writes: list[tuple[int, int, int]] = []
        self.blocks: dict[tuple[int, int, int], list[int]] = {}
        self.words: dict[tuple[int, int], int] = {}

    def write_byte_data(self, address: int, register: int, value: int) -> None:
        self.writes.append((address, register, value))

    def read_byte_data(self, address: int, register: int) -> int:
        return 0

    def read_i2c_block_data(self, address: int, register: int, length: int) -> list[int]:
        return self.blocks[(address, register, length)]

    def read_word_data(self, address: int, register: int) -> int:
        return self.words[(address, register)]

    def close(self) -> None:
        pass


def test_mpu6050_converts_default_ranges() -> None:
    bus = FakeBus()
    bus.blocks[(0x68, 0x3B, 14)] = [
        0x40,
        0x00,
        0xC0,
        0x00,
        0x20,
        0x00,
        0x00,
        0x00,
        0x00,
        0x83,
        0xFF,
        0x7D,
        0x01,
        0x06,
    ]

    reading = Mpu6050Sensor(bus).read()

    assert reading.accel_x_g == 1.0
    assert reading.accel_y_g == -1.0
    assert reading.accel_z_g == 0.5
    assert reading.gyro_x_dps == pytest.approx(1.0)
    assert reading.gyro_y_dps == pytest.approx(-1.0)
    assert reading.gyro_z_dps == pytest.approx(2.0)


def test_mlx90614_converts_kelvin_registers_to_celsius() -> None:
    bus = FakeBus()
    bus.words[(0x5A, 0x06)] = round((24.0 + 273.15) / 0.02)
    bus.words[(0x5A, 0x07)] = round((32.5 + 273.15) / 0.02)

    reading = Mlx90614Sensor(bus).read()

    assert reading.ambient_temp_c == pytest.approx(24.0, abs=0.02)
    assert reading.object_temp_c == pytest.approx(32.5, abs=0.02)


def test_max30100_reports_raw_fifo_channels() -> None:
    bus = FakeBus()
    bus.blocks[(0x57, 0x05, 4)] = [0x12, 0x34, 0xAB, 0xCD]

    sensor = Max30100RawSensor(bus)
    reading = sensor.read()

    assert reading.ir_raw == 0x1234
    assert reading.red_raw == 0xABCD
    assert (0x57, 0x06, 0x03) in bus.writes
