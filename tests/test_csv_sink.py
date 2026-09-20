import csv
from datetime import datetime, timezone

from wearable_monitor.collector import CsvSink
from wearable_monitor.models import CSV_FIELDS, DeviceSample


def test_csv_sink_writes_stable_schema(tmp_path) -> None:
    sample = DeviceSample(
        timestamp_utc=datetime(2021, 6, 1, 12, 30, tzinfo=timezone.utc),
        accel_x_g=1.0,
        accel_y_g=2.0,
        accel_z_g=3.0,
        gyro_x_dps=4.0,
        gyro_y_dps=5.0,
        gyro_z_dps=6.0,
        ambient_temp_c=23.5,
    )
    output = tmp_path / "sample.csv"

    with CsvSink(output, flush_every=1) as sink:
        sink.write(sample)

    with output.open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))

    assert tuple(rows[0]) == CSV_FIELDS
    assert rows[0]["timestamp_utc"] == "2021-06-01T12:30:00.000+00:00"
    assert rows[0]["ambient_temp_c"] == "23.5"
    assert rows[0]["ppg_red_raw"] == ""
