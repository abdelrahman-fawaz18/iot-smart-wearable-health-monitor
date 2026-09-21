from __future__ import annotations

import argparse
from contextlib import ExitStack
from datetime import datetime
from pathlib import Path

from wearable_monitor.collector import Collector, CsvSink, Sampler
from wearable_monitor.hardware import (
    Max30100RawSensor,
    Mlx90614Sensor,
    Mpu6050Sensor,
    Mpu9250Sensor,
    open_smbus,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Record wearable prototype sensor readings to CSV."
    )
    default_name = datetime.now().strftime("device-%Y%m%d-%H%M%S.csv")
    parser.add_argument("--output", type=Path, default=Path("recordings") / default_name)
    parser.add_argument("--imu", choices=("mpu6050", "mpu9250"), default="mpu6050")
    parser.add_argument("--bus", type=int, default=1, help="Linux I2C bus number")
    parser.add_argument("--interval-ms", type=float, default=100.0)
    parser.add_argument("--average-window", type=int, default=3)
    parser.add_argument("--no-temperature", action="store_true")
    parser.add_argument(
        "--max30100",
        action="store_true",
        help="Record raw red and infrared FIFO values",
    )
    parser.add_argument("--limit", type=int, help="Stop after this many samples")
    parser.add_argument("--quiet", action="store_true", help="Do not print each sample")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.interval_ms <= 0:
        raise SystemExit("--interval-ms must be positive")
    if args.average_window < 1:
        raise SystemExit("--average-window must be at least 1")
    if args.limit is not None and args.limit < 1:
        raise SystemExit("--limit must be at least 1")

    with ExitStack() as stack:
        bus = None
        if args.imu == "mpu6050" or not args.no_temperature or args.max30100:
            bus = open_smbus(args.bus)
            stack.callback(bus.close)

        motion_sensor = (
            Mpu6050Sensor(bus) if args.imu == "mpu6050" else Mpu9250Sensor(args.bus)
        )
        temperature_sensor = None if args.no_temperature else Mlx90614Sensor(bus)
        pulse_oximeter = Max30100RawSensor(bus) if args.max30100 else None

        sampler = Sampler(
            motion_sensor=motion_sensor,
            temperature_sensor=temperature_sensor,
            pulse_oximeter=pulse_oximeter,
            average_window=args.average_window,
        )
        with CsvSink(args.output) as sink:
            collector = Collector(
                sampler,
                sink,
                interval_seconds=args.interval_ms / 1000.0,
                print_samples=not args.quiet,
            )
            try:
                rows = collector.run(args.limit)
            except KeyboardInterrupt:
                print(f"\nStopped. Data saved to {args.output}")
                return 130

    print(f"Saved {rows} samples to {args.output}")
    return 0
