"""Minimal SVG bar chart for PHI vs declared threshold (no matplotlib)."""

from __future__ import annotations

from typing import Any


def phi_backtest_svg(report: dict[str, Any]) -> str:
    units = report["units"]
    threshold = float(report["phi_hit_threshold"])
    width = 720
    height = 280
    left, right, top, bottom = 160, 40, 40, 50
    plot_w = width - left - right
    plot_h = height - top - bottom
    bars = []
    n = max(len(units), 1)
    bar_h = plot_h / n * 0.6
    for i, unit in enumerate(units):
        y = top + (i + 0.5) * (plot_h / n) - bar_h / 2
        phi = float(unit["phi"])
        bar_w = max(1.0, phi * plot_w)
        color = "#2b8cbe" if unit["outcome"] == "hit" else "#e31a1c"
        label = unit["spatial_unit_id"]
        bars.append(
            f'<rect x="{left}" y="{y:.1f}" width="{bar_w:.1f}" '
            f'height="{bar_h:.1f}" fill="{color}" />'
            f'<text x="{left - 8}" y="{y + bar_h * 0.7:.1f}" text-anchor="end" '
            f'font-size="11" font-family="sans-serif">{label}</text>'
            f'<text x="{left + bar_w + 6:.1f}" y="{y + bar_h * 0.7:.1f}" '
            f'font-size="11" font-family="sans-serif">{phi:.2f} {unit["outcome"]}</text>'
        )
    thresh_x = left + threshold * plot_w
    title = (
        f"{report['scenario_id']} · PHI vs threshold {threshold} · "
        f"evidence {report['evidence']}"
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">\n'
        f'<rect width="{width}" height="{height}" fill="#fff" />\n'
        f'<text x="{left}" y="24" font-size="14" font-family="sans-serif">{title}</text>\n'
        f'<line x1="{left}" y1="{top}" x2="{left}" y2="{height - bottom}" stroke="#333" />\n'
        f'<line x1="{left}" y1="{height - bottom}" '
        f'x2="{width - right}" y2="{height - bottom}" stroke="#333" />\n'
        f'<line x1="{thresh_x:.1f}" y1="{top}" x2="{thresh_x:.1f}" y2="{height - bottom}" '
        f'stroke="#666" stroke-dasharray="4 3" />\n'
        f'<text x="{thresh_x:.1f}" y="{height - 18}" text-anchor="middle" font-size="11" '
        f'font-family="sans-serif">threshold {threshold}</text>\n'
        + "\n".join(bars)
        + "\n</svg>\n"
    )
