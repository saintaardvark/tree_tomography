# Tree tomography

A stab at doing tree tomography with a microcontroller. To start with, I'm
using the MPU6050 sensor to detect sound waves.

Originally I'd used an ESP32 as the microcontroller, but have switched
to using a Pi Pico thanks to [this excellent
thread](https://forums.raspberrypi.com/viewtopic.php?t=306064&start=50&sid=fedd5651d4f778d74f3d9c943db454aa)
and [the code from that thread](https://github.com/jbeale1/pico/blob/main/QuadHoru1.py).

# Pins

## Pico

- Pico GPIO 2 (label: 4) -> MPU 6050 interrupt pin
- Pico GPIO 14 (label: 19) -> MPU 6050 interrupt pin
- Pico GPIO 15 (label: 20) -> LED -> switch -> resistor -> +3V
- Pico I2C 0 SDA (label: 26) -> MPU 6050 SDA
- Pico I2C 0 SCL (label: 27) -> MPU 6050 SCL

