#!/usr/bin/env python3
"""
Generate a libinput "custom" pointer-acceleration curve that approximates
Windows' built-in acceleration curve (the one driven by "Enhance pointer
precision" + the Mouse Pointer Speed slider).

Credit / background:
  - Curve reverse-engineering: http://www.esreality.com/index.php?a=post&id=1945096
  - Original conversion script: https://gist.github.com/yinonburgansky/7be4d0489a0df8c06a923240b8eb0191
  - Hyprland adaptation this was based on: https://gist.github.com/fufexan/de2099bc3086f3a6c83d61fc1fcc06c9
This version prints raw `xinput` commands (X11 / xf86-input-libinput) instead
of hyprctl commands, since it's meant for X11 + i3, not a Wayland compositor.

Requires libinput >= 1.23 and xf86-input-libinput >= 1.3 (custom accel profile).
Check with: pacman -Q libinput xf86-input-libinput
"""

import struct
import sys

# ===== PARAMETERS — set these for your setup =====
device_dpi = 600          # <-- YOUR mouse/trackball's sensor DPI (check Solaar/Logi Options)
screen_dpi = 96               # Windows' internal baseline logical DPI (almost always 96 — see note below)
screen_scaling_factor = 2.75     # Your Windows DISPLAY SCALING %, as a factor (100% -> 1, 125% -> 1.25, 150% -> 1.5)
sample_point_count = 40       # more points = smoother curve
sensitivity_factor = 6        # Windows "Mouse Pointer Speed" slider mapping, see table below:
# 1=0.1 | 2=0.2 | 3=0.4 | 4=0.6 | 5=0.8 | 6=1.0 (Windows DEFAULT, slider=10) | 7=1.2 | 8=1.4 | 9=1.6 | 10=1.8 | 11=2.0
# ===== END PARAMETERS =====

def float16x16(num):
    return struct.unpack('<i', num[:-4])[0] / int(0xffff)

# Windows' default SmoothMouseXCurve / SmoothMouseYCurve registry points
X = [
    bytes.fromhex("00 00 00 00 00 00 00 00"),
    bytes.fromhex("15 6e 00 00 00 00 00 00"),
    bytes.fromhex("00 40 01 00 00 00 00 00"),
    bytes.fromhex("29 dc 03 00 00 00 00 00"),
    bytes.fromhex("00 00 28 00 00 00 00 00"),
]
Y = [
    bytes.fromhex("00 00 00 00 00 00 00 00"),
    bytes.fromhex("fd 11 01 00 00 00 00 00"),
    bytes.fromhex("00 24 04 00 00 00 00 00"),
    bytes.fromhex("00 fc 12 00 00 00 00 00"),
    bytes.fromhex("00 c0 bb 01 00 00 00 00"),
]

scale_x = device_dpi / 1e3
scale_y = screen_dpi / 1e3 / screen_scaling_factor * sensitivity_factor

windows_points = [[float16x16(x), float16x16(y)] for x, y in zip(X, Y)]
points = [[x * scale_x, y * scale_y] for x, y in windows_points]

def find2points(x):
    i = 0
    while i < len(points) - 2 and x >= points[i + 1][0]:
        i += 1
    return points[i], points[i + 1]

def interpolate(x):
    (x0, y0), (x1, y1) = find2points(x)
    return ((x - x0) * y1 + (x1 - x) * y0) / (x1 - x0)

def sample_points(count):
    max_x = points[-2][0]
    step = max_x / (count - 2)
    xs = [i * step for i in range(count)]
    ys = [interpolate(x) for x in xs]
    return xs, ys, step

xs, ys, step = sample_points(sample_point_count)
points_str = " ".join("%.6f" % y for y in ys)

print("# Generated curve — sanity check a few values:")
print(f"#   step size: {step:.10f} device-units/ms")
print(f"#   {sample_point_count} points, first few: {' '.join('%.3f' % y for y in ys[:5])} ...")
print()
print("# Find your device name first:")
print('xinput list --name-only')
print()
print('DEVICE="Your Device Name Here"')
print(f'xinput set-prop "$DEVICE" "libinput Accel Custom Motion Step" {step:.10f}')
print(f'xinput set-prop "$DEVICE" "libinput Accel Custom Motion Points" {points_str}')
print('xinput set-prop "$DEVICE" "libinput Accel Profile Enabled" 0 0 1')
