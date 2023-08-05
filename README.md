# Tree tomography

A stab at doing tree tomography with an ESP32. To start with, I'm
using the MPU6050 sensor to detect sound waves.

# Pins

I'm using an ESP32 WeMos LOLIN32 Lite. See
https://mischianti.org/2021/07/30/esp32-wemos-lolin32-lite-high-resolution-pinout-and-specs/
for a pinout diagram.

- Pin 4: touchpad used for arming the timer

For MPU6050:

- Pin 23: to MPU6050 SCL
- Pin 18: to MPU5050 SDA

I'm using a GMG12864-06D display.  Many thanks to
https://www.youtube.com/watch?v=wXDFW6NsDK4 for the magic to get this
to work with the u8g2 library!

- Pin 32: to pin 1 on display (labelled CS)
- Pin 33: to pin 2 (labelled RSE)
- Pin 25: to pin 3 (labelled RS)
- Pin 26: to pin 4 (labelled SCL)
- Pin 27: to pin 5 (labelled SI)

