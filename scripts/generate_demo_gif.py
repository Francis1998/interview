#!/usr/bin/env python3
"""Generate README demo GIF for the handbook preview."""

from __future__ import annotations

from pathlib import Path

try:
    import imageio.v3 as iio
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    raise SystemExit("Install deps: pip install pillow imageio")

OUTPUT = Path(__file__).resolve().parents[1] / "assets" / "demo-handbook.gif"

FRAMES = [
    ("Browse Topics", "9 domains: Python, Go, MySQL, Linux…", "#6d5efc"),
    ("Python", "GIL · memory · coroutines · decorators", "#22d3ee"),
    ("Networking", "TCP handshake · HTTP/2 · TLS · DNS", "#34d399"),
    ("System Design", "CAP · sharding · rate limiting · CDN", "#f472b6"),
    ("Search & Study", "Filter sidebar · rendered markdown · tables", "#fbbf24"),
    ("make serve", "http://127.0.0.1:8080 — local preview server", "#6d5efc"),
]


def draw_frame(title: str, subtitle: str, color: str, idx: int) -> Image.Image:
    img = Image.new("RGB", (900, 506), (7, 11, 20))
    d = ImageDraw.Draw(img)
    try:
        font_lg = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 32)
        font_md = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 18)
        font_sm = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 14)
    except OSError:
        font_lg = font_md = font_sm = ImageFont.load_default()

    d.rounded_rectangle((24, 24, 876, 482), radius=16, outline=(36, 48, 73), width=2)
    d.rounded_rectangle((24, 24, 876, 70), radius=16, fill=(15, 22, 41))
    d.text((44, 38), "📘 Interview Handbook", fill=(232, 237, 247), font=font_md)

    d.rounded_rectangle((44, 100, 260, 462), radius=10, fill=(21, 29, 50), outline=(36, 48, 73))
    topics = ["Python", "Go", "MySQL", "Linux", "Networking", "Redis", "System Design"]
    for i, t in enumerate(topics[:7]):
        highlight = idx < 5 and (
            (idx == 1 and t == "Python")
            or (idx == 2 and t == "Networking")
            or (idx == 3 and t == "System Design")
        )
        fill = (30, 27, 75) if highlight else (21, 29, 50)
        y = 115 + i * 48
        d.rounded_rectangle((54, y, 250, y + 38), radius=6, fill=fill)
        d.text((64, y + 10), t, fill=(201, 212, 234), font=font_sm)

    d.rounded_rectangle((280, 100, 856, 462), radius=10, fill=(15, 22, 41), outline=(36, 48, 73))
    d.text((300, 120), title, fill=color, font=font_lg)
    d.text((300, 170), subtitle, fill=(139, 155, 191), font=font_md)
    d.text((300, 220), "Rendered markdown · tables · code blocks", fill=(100, 116, 139), font=font_sm)
    d.text((300, 420), f"Frame {idx + 1}/{len(FRAMES)}", fill=(100, 116, 139), font=font_sm)

    bar = (idx + 1) / len(FRAMES)
    d.rectangle((300, 440, 856, 452), fill=(36, 48, 73))
    d.rectangle((300, 440, 300 + int(556 * bar), 452), fill=(109, 94, 252))
    return img


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    frames = []
    for i, (title, sub, color) in enumerate(FRAMES):
        f = draw_frame(title, sub, color, i)
        frames.extend([f, f])
    iio.imwrite(OUTPUT, frames, duration=700, loop=0)
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()
