# Tree tomography

A stab at doing tree tomography with a microcontroller. To start with, I'm
using the MPU6050 sensor to detect sound waves.

Originally I'd used an ESP32 as the microcontroller, but have switched
to using a Pi Pico thanks to [this excellent
thread](https://forums.raspberrypi.com/viewtopic.php?t=306064&start=50&sid=fedd5651d4f778d74f3d9c943db454aa)
and [the code from that thread](https://github.com/jbeale1/pico/blob/main/QuadHoru1.py).

# Pins

## Pico

- GPIO 15: vibration sensor #1
- GPIO 14: vibration sensor #2
- GPIO 13: vibration sensor #3
- GPIO 3: debug pin; if high, go into debug mode

## Logging

`make log`

Serial port: 115200
