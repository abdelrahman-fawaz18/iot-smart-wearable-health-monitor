from __future__ import annotations

from wearable_monitor.models import MotionReading, PulseOximeterReading, TemperatureReading
from wearable_monitor.sensors import SMBusLike


def open_smbus(bus_number: int = 1) -> SMBusLike:
    try:
        from smbus2 import SMBus
    except ImportError as exc:
        raise RuntimeError(
            "The hardware extras are not installed. Run: pip install -e '.[hardware]'"
        ) from exc
    return SMBus(bus_number)


def _signed_int16(msb: int, lsb: int) -> int:
    value = (msb << 8) | lsb
    return value - 65536 if value & 0x8000 else value


class Mpu6050Sensor:
    """Minimal MPU6050 reader using its default +/-2 g and +/-250 dps ranges."""

    ADDRESS = 0x68
    PWR_MGMT_1 = 0x6B
    ACCEL_CONFIG = 0x1C
    GYRO_CONFIG = 0x1B
    DATA_START = 0x3B

    def __init__(self, bus: SMBusLike, address: int = ADDRESS) -> None:
        self.bus = bus
        self.address = address
        self.bus.write_byte_data(address, self.PWR_MGMT_1, 0x00)
        self.bus.write_byte_data(address, self.ACCEL_CONFIG, 0x00)
        self.bus.write_byte_data(address, self.GYRO_CONFIG, 0x00)

    def read(self) -> MotionReading:
        data = self.bus.read_i2c_block_data(self.address, self.DATA_START, 14)
        if len(data) != 14:
            raise OSError(f"MPU6050 returned {len(data)} bytes; expected 14")

        accel = [_signed_int16(data[i], data[i + 1]) / 16384.0 for i in (0, 2, 4)]
        gyro = [_signed_int16(data[i], data[i + 1]) / 131.0 for i in (8, 10, 12)]
        return MotionReading(*accel, *gyro)


class Mpu9250Sensor:
    """Adapter for the mpu9250-jmdev package used in the later project code."""

    def __init__(self, bus_number: int = 1) -> None:
        try:
            from mpu9250_jmdev.mpu_9250 import MPU9250
            from mpu9250_jmdev.registers import (
                AFS_8G,
                AK8963_ADDRESS,
                AK8963_BIT_16,
                AK8963_MODE_C100HZ,
                GFS_1000,
                MPU9050_ADDRESS_68,
            )
        except ImportError as exc:
            raise RuntimeError(
                "MPU9250 support requires mpu9250-jmdev. "
                "Run: pip install -e '.[hardware]'"
            ) from exc

        self.device = MPU9250(
            address_ak=AK8963_ADDRESS,
            address_mpu_master=MPU9050_ADDRESS_68,
            address_mpu_slave=None,
            bus=bus_number,
            gfs=GFS_1000,
            afs=AFS_8G,
            mfs=AK8963_BIT_16,
            mode=AK8963_MODE_C100HZ,
        )
        self.device.configure()

    def read(self) -> MotionReading:
        accel = self.device.readAccelerometerMaster()
        gyro = self.device.readGyroscopeMaster()
        magnetometer = self.device.readMagnetometerMaster()
        return MotionReading(*accel, *gyro, *magnetometer)


class Mlx90614Sensor:
    ADDRESS = 0x5A
    AMBIENT_REGISTER = 0x06
    OBJECT_REGISTER = 0x07

    def __init__(self, bus: SMBusLike, address: int = ADDRESS) -> None:
        self.bus = bus
        self.address = address

    def _temperature_c(self, register: int) -> float:
        raw = self.bus.read_word_data(self.address, register)
        if raw & 0x8000:
            raise OSError(f"MLX90614 reported an error for register 0x{register:02x}")
        return (raw & 0x7FFF) * 0.02 - 273.15

    def read(self) -> TemperatureReading:
        return TemperatureReading(
            ambient_temp_c=self._temperature_c(self.AMBIENT_REGISTER),
            object_temp_c=self._temperature_c(self.OBJECT_REGISTER),
        )


class Max30100RawSensor:
    """Read raw red and infrared samples without claiming medical measurements."""

    ADDRESS = 0x57
    FIFO_WRITE_POINTER = 0x02
    OVERFLOW_COUNTER = 0x03
    FIFO_READ_POINTER = 0x04
    FIFO_DATA = 0x05
    MODE_CONFIG = 0x06
    SPO2_CONFIG = 0x07
    LED_CONFIG = 0x09

    def __init__(self, bus: SMBusLike, address: int = ADDRESS) -> None:
        self.bus = bus
        self.address = address
        self.bus.write_byte_data(address, self.MODE_CONFIG, 0x03)
        self.bus.write_byte_data(address, self.SPO2_CONFIG, (1 << 2) | 0x03)
        self.bus.write_byte_data(address, self.LED_CONFIG, 0x33)
        self.bus.write_byte_data(address, self.FIFO_WRITE_POINTER, 0)
        self.bus.write_byte_data(address, self.OVERFLOW_COUNTER, 0)
        self.bus.write_byte_data(address, self.FIFO_READ_POINTER, 0)

    def read(self) -> PulseOximeterReading:
        data = self.bus.read_i2c_block_data(self.address, self.FIFO_DATA, 4)
        if len(data) != 4:
            raise OSError(f"MAX30100 returned {len(data)} bytes; expected 4")
        ir_raw = (data[0] << 8) | data[1]
        red_raw = (data[2] << 8) | data[3]
        return PulseOximeterReading(ir_raw=ir_raw, red_raw=red_raw)
