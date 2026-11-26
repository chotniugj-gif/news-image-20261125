# 25 November 2026 — World News in One Image

Entry for make.fun `news-image-20261125`: a single 1024×1024 broadsheet
front page summing up Wednesday 25 November 2026.

The page leads with the Strait of Hormuz tanker fires, then covers Gaza,
Ukraine, spaceflight, markets, a Brooklyn court verdict, COP31, the
Australia–Solomon Islands treaty, Sudan, Cairo, and Houthi strikes on
Saudi Arabia. A numbers rail carries the day's sharpest figures.

## Run

```sh
python3 draw_poster.py   # regenerates entry.png (Pillow, deterministic)
python3 main.py          # copies entry.png to /output/entry.png
```

`main.py` uses only the Python standard library and writes the image
bytes unchanged, so two runs produce identical output. The image is a
1024×1024 PNG under 1 MiB and needs no network.
