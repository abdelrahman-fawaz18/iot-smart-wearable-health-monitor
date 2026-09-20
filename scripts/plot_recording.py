#!/usr/bin/env python3
"""Render a recovered walking recording as a self-contained SVG."""

from __future__ import annotations

import argparse
import csv
from html import escape
from pathlib import Path

COLORS = {"X": "#2563EB", "Y": "#F97316", "Z": "#0F766E", "Temp": "#7C3AED"}


def parse_time(value: str) -> float:
    minutes, seconds = value.split(":", maxsplit=1)
    return int(minutes) * 60 + float(seconds)


def load_recording(path: Path) -> dict[str, list[float]]:
    columns = {
        "time": [],
        "Acc-X": [],
        "Acc-Y": [],
        "Acc-Z": [],
        "Gyro-X": [],
        "Gyro-Y": [],
        "Gyro-Z": [],
        "Ambient Temp": [],
    }
    offset = 0.0
    previous = None
    with path.open(encoding="utf-8-sig", newline="") as stream:
        for row in csv.DictReader(stream):
            current = parse_time(row["Time"])
            if previous is not None and current + offset < previous - 1_800:
                offset += 3_600
            elapsed = current + offset
            previous = elapsed
            columns["time"].append(elapsed)
            for name in columns:
                if name != "time":
                    columns[name].append(float(row[name]))

    if not columns["time"]:
        raise ValueError(f"No rows found in {path}")
    start = columns["time"][0]
    columns["time"] = [value - start for value in columns["time"]]
    return columns


def _segments(
    x_values: list[float],
    y_values: list[float],
    left: float,
    top: float,
    width: float,
    height: float,
    y_min: float,
    y_max: float,
) -> list[str]:
    x_max = max(x_values) or 1.0
    span = y_max - y_min or 1.0
    segments: list[list[str]] = [[]]
    previous_x = x_values[0]
    for x, y in zip(x_values, y_values, strict=True):
        if x - previous_x > 2.0:
            segments.append([])
        segments[-1].append(
            f"{left + (x / x_max) * width:.1f},{top + height - ((y - y_min) / span) * height:.1f}"
        )
        previous_x = x
    return [" ".join(segment) for segment in segments if len(segment) > 1]


def _panel(
    data: dict[str, list[float]],
    top: int,
    title: str,
    unit: str,
    series: list[tuple[str, str]],
    show_x_axis: bool,
) -> str:
    left, width, height = 105, 1315, 190
    values = [value for column, _ in series for value in data[column]]
    y_min, y_max = min(values), max(values)
    padding = max((y_max - y_min) * 0.08, 0.1)
    y_min -= padding
    y_max += padding

    elements = [
        f'<rect x="70" y="{top - 45}" width="1380" height="260" rx="16" fill="#ffffff" stroke="#e2e8f0"/>',
        f'<text x="105" y="{top - 12}" class="panel-title">{escape(title)}</text>',
        f'<text transform="translate(32 {top + 115}) rotate(-90)" class="axis-label">{escape(unit)}</text>',
    ]
    for tick in range(5):
        fraction = tick / 4
        y = top + height - fraction * height
        value = y_min + fraction * (y_max - y_min)
        elements.append(
            f'<line x1="{left}" y1="{y:.1f}" x2="{left + width}" y2="{y:.1f}" class="grid"/>'
        )
        elements.append(
            f'<text x="94" y="{y + 5:.1f}" text-anchor="end" class="tick">{value:.1f}</text>'
        )

    for column, label in series:
        for points in _segments(
            data["time"], data[column], left, top, width, height, y_min, y_max
        ):
            elements.append(
                f'<polyline points="{points}" fill="none" stroke="{COLORS[label]}" '
                'stroke-width="2.1" stroke-linejoin="round" stroke-linecap="round"/>'
            )

    if len(series) > 1:
        for index, (_, label) in enumerate(series):
            x = 1250 + index * 58
            elements.extend(
                [
                    f'<line x1="{x}" y1="{top - 20}" x2="{x + 22}" y2="{top - 20}" stroke="{COLORS[label]}" stroke-width="3"/>',
                    f'<text x="{x + 29}" y="{top - 15}" class="legend">{label}</text>',
                ]
            )

    if show_x_axis:
        duration = max(data["time"])
        for tick in range(6):
            fraction = tick / 5
            x = left + fraction * width
            elements.append(
                f'<text x="{x:.1f}" y="{top + 215}" text-anchor="middle" class="tick">{duration * fraction:.0f}</text>'
            )
        elements.append(
            f'<text x="{left + width / 2}" y="{top + 244}" text-anchor="middle" class="axis-label">Elapsed time (seconds)</text>'
        )

    return "\n".join(elements)


def create_plot(data: dict[str, list[float]], output: Path, title: str) -> None:
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1500" height="1010" viewBox="0 0 1500 1010" role="img" aria-labelledby="title description">
  <title id="title">{escape(title)}</title>
  <desc id="description">Acceleration, angular velocity, and ambient temperature from a recovered walking recording.</desc>
  <style>
    text {{ font-family: Inter, "Segoe UI", Arial, sans-serif; fill: #334155; }}
    .heading {{ font-size: 28px; font-weight: 700; fill: #0f172a; }}
    .subheading {{ font-size: 16px; fill: #64748b; }}
    .panel-title {{ font-size: 18px; font-weight: 700; fill: #0f172a; }}
    .axis-label {{ font-size: 14px; font-weight: 600; fill: #475569; }}
    .tick {{ font-size: 12px; fill: #64748b; }}
    .legend {{ font-size: 13px; font-weight: 600; fill: #475569; }}
    .grid {{ stroke: #e2e8f0; stroke-width: 1; }}
  </style>
  <rect width="1500" height="1010" fill="#f8fafc"/>
  <text x="70" y="52" class="heading">{escape(title)}</text>
  <text x="70" y="80" class="subheading">Original sensor values; no filtering or resampling applied</text>
  {_panel(data, 145, "Acceleration", "g", [("Acc-X", "X"), ("Acc-Y", "Y"), ("Acc-Z", "Z")], False)}
  {_panel(data, 430, "Angular velocity", "degrees / second", [("Gyro-X", "X"), ("Gyro-Y", "Y"), ("Gyro-Z", "Z")], False)}
  {_panel(data, 715, "Ambient temperature", "degrees C", [("Ambient Temp", "Temp")], True)}
</svg>
'''
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(svg, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--title", default="Recovered walking recording: M01 / left wrist / Sgl")
    args = parser.parse_args()

    create_plot(load_recording(args.input), args.output, args.title)
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
